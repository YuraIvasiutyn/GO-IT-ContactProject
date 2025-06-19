from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date, timedelta
from .models import Contact
from .forms import QueryForm, AddContactForm


# Create your views here.

def main(request):
    query = request.GET.get('query', '')
    days = request.GET.get('days', '')
    print("days", days)
    print("query", query)
    contacts = Contact.objects.all()

    if query:
        contacts = contacts.filter(
            Q(full_name__icontains=query) |
            Q(address__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    if days:
        days = int(days)
        today = date.today()
        target_date = today + timedelta(days=days)

        print(target_date)

        def birthday_in_days(contact):
            if contact.birthday:
                bday_this_year = contact.birthday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                return today <= bday_this_year <= target_date
            return False

        contact_ids = [c.id for c in contacts if birthday_in_days(c)]
        contacts = Contact.objects.filter(id__in=contact_ids)

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)

    query_form = QueryForm(initial={'query': query, 'days': days})
    return render(request, 'contact_app/index.html', {
        'title': 'Contacts',
        'contacts': contacts,
        'query_form': query_form
    })


def add_contact(request):
    form = AddContactForm(instance=Contact())
    if request.method == 'POST':
        form = AddContactForm(request.POST, instance=Contact())
        if form.is_valid():
            form.save()
            return redirect(to='contact_app:main')
    return render(request, template_name='contact_app/add_contact.html', context={'title': 'Add contact', 'form': form})


def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = AddContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_app:main')
    else:
        form = AddContactForm(instance=contact)
    return render(request, 'contact_app/edit_contact.html', {'form': form, 'title': 'Edit Contact'})


def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_app:main')
    return render(request, 'contact_app/delete_confirm.html', {'contact': contact})
