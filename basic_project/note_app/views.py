from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

from django.utils.html import format_html
import re
from django.db.models import Q


from .forms import TagForm, NoteForm
from .models import Tag, Note

# ------------------------------------------------------------------------
# лише на час розробки потім прибрати - це мій ІД
from django.contrib.auth import login
from django.contrib.auth import get_user_model


User = get_user_model()
ID = 4

def dev_login(request):
    if not request.user.is_authenticated:
        dev_user = User.objects.get(username="viktor")  # або твій логін
        dev_user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, dev_user)
    return redirect('note_app:main')

# ------------------------------------------------------------------------


def count_top_tags(number_of_tags=10, min_font_size=10, max_font_size=28):
    # Отримуємо топ-10 тегів за кількістю використань
    top_tags = Tag.objects.annotate(cnt=Count('note'))\
        .order_by('-cnt')[:number_of_tags]
    # print(f"top tags: {top_tags}")
    # Визначаємо мінімальне та максимальне значення використання
    if top_tags:
        max_val = max(tag.cnt for tag in top_tags)
        min_val = min(tag.cnt for tag in top_tags)
    else:
        max_val = min_val = 0

    # розраховуємо розмір шрифту до кожного тегу
    for tag in top_tags:
        if max_val > min_val:
            # Масштабуємо розмір шрифту
            scale = (tag.cnt - min_val) / (max_val - min_val)
            tag.font_size = int(min_font_size + (max_font_size - min_font_size) * scale)
        else:
            # Якщо всі теги мають однакову частоту, встановлюємо мінімальний розмір
            tag.font_size = max_font_size

    return top_tags


def get_notes_on_page(request) -> int:
    # Отримуємо кількість notes на сторінку з параметра GET (за замовчуванням 5)
    notes_per_page = request.GET.get('notes_per_page', 5)
    try:
        notes_per_page = int(notes_per_page)
    except (ValueError, TypeError):
        # Якщо значення некоректне, використовуємо 10
        notes_per_page = 10  # Якщо значення некоректне, використовуємо 10
    return notes_per_page


# Create your views here.
def main(request):
    search_query = request.GET.get("search", "")
    notes_on_page = get_notes_on_page(request)
    notes = Note.objects.all()

    if notes and search_query:
        notes = notes.filter(Q(note__icontains=search_query) | Q(note_title__icontains=search_query))

    # Отримуємо топ-10 тегів за кількістю використань
    top_tags = count_top_tags()

    # Отримуємо всі notes, які належать користувачу
    if len(notes) <= notes_on_page:
        return render(
            request,
            'note_app/index.html',
            {
                "page_obj": notes,
                "top_tags": top_tags,
                'notes_per_page': notes_on_page,
            }
        )
    else:
        # Додаємо пагінацію (наприклад, X notes на сторінку)
        paginator = Paginator(notes, notes_on_page)  # 5 notes на сторінку
        page_number = request.GET.get('page')  # Отримуємо номер сторінки з параметра GET
        page_obj = paginator.get_page(page_number)  # Отримуємо об'єкт сторінки

        # Передаємо об'єкт сторінки в шаблон
        return render(
            request,
            'note_app/index.html',
            {
                "page_obj": page_obj,
                "top_tags": top_tags,
                'notes_per_page': notes_on_page,
            }
        )


# @login_required
# створення тегу
def tag(request):
    if not request.user.is_authenticated:
        my_tags = Tag.objects.filter(user=request.user).all()
    else:
        my_tags = Tag.objects.filter(user_id=ID).all()

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='note_app:main')
        else:
            # not valid form --> render again
            return render(
                request,
                'note_app/tag.html',
                {
                    'form': form,
                    'tags': my_tags,
                }
            )

    # get request
    return render(
        request,
        'note_app/tag.html',
        {
            'form': TagForm(),
            'tags': my_tags,
        }
    )


@login_required
def note(request, note_id=None):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        print(f"POST request - {note_id}")
        if note_id:
            # редагування
            note = get_object_or_404(Note, pk=note_id, user=request.user)
            form = NoteForm(request.POST, instance=note)
        else:
            # створення нової note
            form = NoteForm(request.POST)

        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()

            # add tags to notes (many to many --> stored in separate table)
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'),
                user=request.user
            )
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='note_app:main')
        else:
            # якщо форма не валідна, повертаємо її знову а режимі редагування
            return render(
                request,
                'note_app/note.html',
                {
                    "tags": tags,
                    'form': form,
                    'note': note,
                }
            )
    else:
        # Якщо GET-запит, створюємо форму для редагування або створення
        if note_id:
            note = Note.objects.filter(pk=note_id, user=request.user).first()
            form = NoteForm(instance=note)
        else:
            note = None
            form = NoteForm()

        return render(
            request,
            'note_app/note.html',
            {
                "tags": tags,
                'form': form,
                'note': note,
            }
        )

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if not note or note.user != request.user:
        msg = f"Note (id={note_id}) does not belong to the '{request.user}' user --> You can't see details here."
        return redirect(
            to='note_app:error-page',
            message=msg
        )
    return render(request, 'note_app/note_detail.html', {"note": note})


@login_required
def note_delete(request, note_id):
    n = Note.objects.filter(
        pk=note_id,
        user=request.user
    ).first()
    # print(f"note: {q}")

    if n:
        # якщо note належить користувачу, то видаляємо її
        n.delete()
        return redirect(to='note_app:main')
    else:
        msg = f"Note (id={note_id}) does not belong to the '{request.user}' user --> Can't delete it."
        return redirect(
            to='note_app:error-page',
            message=msg
        )


@login_required
def search_by_tag(request, tag_name):
    notes_on_page = get_notes_on_page(request)
    tag = get_object_or_404(Tag, name=tag_name)
    notes = Note.objects.filter(tags=tag).all()

    # Отримуємо топ-10 тегів за кількістю використань
    top_tags = count_top_tags()

    if len(notes) <= notes_on_page:
        return render(
            request,
            'note_app/notes_by_tag.html',
            {
                'tag': tag,
                "page_obj": notes,
                "top_tags": top_tags,
                'notes_per_page': notes_on_page,
            }
        )
    else:
        # Додаємо пагінацію (наприклад, 10 notes на сторінку)
        paginator = Paginator(notes, notes_on_page)
        # Отримуємо номер сторінки з параметра GET
        page_number = request.GET.get('page')
        # Отримуємо об'єкт сторінки
        page_obj = paginator.get_page(page_number)
        # Передаємо notes та тег у шаблон
        return render(
            request,
            'note_app/notes_by_tag.html',
            {
                'tag': tag,
                'page_obj': page_obj,
                "top_tags": top_tags,
                'notes_per_page': notes_on_page,
            }
        )


def error(response, message):
    return render(
        response,
        'note_app/error.html',
        {
            'message': message
        }
    )
