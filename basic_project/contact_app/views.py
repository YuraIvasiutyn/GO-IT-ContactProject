from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Contact
from .forms import QueryForm, AddContactForm


# Create your views here.

def main(request):
    q = request.GET.get('q', '')
    contacts = Contact.objects.all()

    if q:
        contacts = contacts.filter(
            Q(full_name__icontains=q) |
            Q(address__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q)
        )
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)

    form = QueryForm(initial={'q': q})
    return render(request, 'contact_app/index.html', {
        'title': 'Main',
        'contacts': contacts,
        'form': form
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
