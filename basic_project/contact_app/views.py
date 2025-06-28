from typing import Union
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, QuerySet
from django.core.paginator import Paginator, Page
from django.http import HttpRequest, HttpResponse
from datetime import date, timedelta
from .models import Contact
from .forms import QueryForm, AddContactForm


@login_required
def main(request: HttpRequest) -> HttpResponse:
    query: str = request.GET.get('query', '')
    days_param: Union[str, int] = request.GET.get('days', '')
    contacts: QuerySet[Contact] = Contact.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(
            Q(full_name__icontains=query) |
            Q(address__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    if days_param:
        days: int = int(days_param)
        today: date = date.today()
        target_date: date = today + timedelta(days=days)

        def birthday_in_days(contact: Contact) -> bool:
            if contact.birthday:
                bday_this_year = contact.birthday.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                return today <= bday_this_year <= target_date
            return False

        contact_ids = [c.id for c in contacts if birthday_in_days(c)]
        contacts = Contact.objects.filter(id__in=contact_ids)

    contacts = contacts.order_by('id')
    paginator: Paginator = Paginator(contacts, 10)
    page_number: Union[str, None] = request.GET.get("page")
    contacts_page: Page = paginator.get_page(page_number)

    query_form: QueryForm = QueryForm(initial={'query': query, 'days': days_param})
    return render(request, 'contact_app/index.html', {
        'title': 'Contacts',
        'contacts': contacts_page,
        'query_form': query_form
    })


@login_required
def add_contact(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form: AddContactForm = AddContactForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(to='contact_app:main')
    else:
        form = AddContactForm()
    return render(request, template_name='contact_app/add_contact.html', context={'title': 'Add contact', 'form': form})


@login_required
def edit_contact(request: HttpRequest, pk: int) -> HttpResponse:
    contact: Contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form: AddContactForm = AddContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_app:main')
    else:
        form = AddContactForm(instance=contact)
    return render(request, 'contact_app/edit_contact.html', {'form': form, 'title': 'Edit Contact'})


@login_required
def delete_contact(request: HttpRequest, pk: int) -> HttpResponse:
    contact: Contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_app:main')
    return render(request, 'contact_app/delete_confirm.html', {'contact': contact})
