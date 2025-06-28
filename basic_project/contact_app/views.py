
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, QuerySet
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from datetime import date, timedelta
from .models import Contact
from .forms import QueryForm, AddContactForm


def filter_by_birthday(queryset: QuerySet[Contact], days: int) -> QuerySet[Contact]:
    """
    Filter a queryset of contacts by those whose birthday is within the given number of days.

    Args:
        queryset: A queryset of Contact objects to filter.
        days: The number of days to filter by.

    Returns:
        A queryset of Contact objects with an upcoming birthday within the given number of days.
    """
    today = date.today()
    target_date = today + timedelta(days=days)

    def get_upcoming_birthday(contact: Contact) -> bool:
        if not contact.birthday:
            return False
        try:
            bday_this_year = contact.birthday.replace(year=today.year)
        except ValueError:
            bday_this_year = contact.birthday.replace(year=today.year, day=28)
        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)
        return today <= bday_this_year <= target_date

    contact_ids = [c.id for c in queryset if get_upcoming_birthday(c)]
    return Contact.objects.filter(id__in=contact_ids)


@login_required
def main(request: HttpRequest) -> HttpResponse:
    """
    Display a list of the logged-in user's contacts, with the ability to search
    by name, address, email, or phone number, and to filter by upcoming
    birthdays.

    Args:
        request: The current HTTP request.

    Returns:
        An HTTP response containing a rendered HTML page with the list of
        contacts.
    """
    query = request.GET.get('query', '')
    days_param = request.GET.get('days', '')
    contacts = Contact.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(
            Q(full_name__icontains=query) |
            Q(address__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    if days_param.isdigit():
        contacts = filter_by_birthday(contacts, int(days_param))

    paginator = Paginator(contacts.order_by('id'), 10)
    page_number = request.GET.get("page")
    contacts_page = paginator.get_page(page_number)

    query_form = QueryForm(initial={'query': query, 'days': days_param})
    return render(request, 'contact_app/index.html', {
        'title': 'Contacts',
        'contacts': contacts_page,
        'query_form': query_form
    })


@login_required
def add_contact(request: HttpRequest) -> HttpResponse:
    """
    Display a form to add a new contact, or save a new contact if the form is
    submitted.

    Args:
        request: The current HTTP request.

    Returns:
        An HTTP response containing a rendered HTML page with the form to
        add a contact, or a redirect to the main page if a contact is
        successfully added.
    """
    if request.method == 'POST':
        form = AddContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_app:main')
    else:
        form = AddContactForm()
    return render(request, 'contact_app/add_contact.html', {
        'title': 'Add Contact',
        'form': form
    })


@login_required
def edit_contact(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display a form to edit an existing contact, or save changes to the contact if the form is submitted.

    Args:
        request: The current HTTP request.
        pk: The primary key of the contact to edit.

    Returns:
        An HTTP response containing a rendered HTML page with the form to
        edit the contact, or a redirect to the main page if the contact is
        successfully edited. Returns a forbidden response if the user is
        not authorized to edit the contact.
    """

    contact = get_object_or_404(Contact, pk=pk)
    if contact.user != request.user:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        form = AddContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_app:main')
    else:
        form = AddContactForm(instance=contact)
    return render(request, 'contact_app/edit_contact.html', {
        'title': 'Edit Contact',
        'form': form
    })


@login_required
def delete_contact(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Display a confirmation page to delete an existing contact, or delete the contact if the form is submitted.

    Args:
        request: The current HTTP request.
        pk: The primary key of the contact to delete.

    Returns:
        An HTTP response containing a rendered HTML page with the confirmation
        form to delete the contact, or a redirect to the main page if the contact
        is successfully deleted. Returns a forbidden response if the user is
        not authorized to delete the contact.
    """
    contact = get_object_or_404(Contact, pk=pk)
    if contact.user != request.user:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        contact.delete()
        return redirect('contact_app:main')
    return render(request, 'contact_app/delete_confirm.html', {
        'contact': contact
    })