from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from memcpy.models import *
from .forms import *


def list_all_books(request):
    all_books = Book.objects.all()
    # all_entries = Entry.objects.all()

    # Ryan: Don't list entry details in books.html
    # entry_total = []
    # for i in range(0, len(all_books)):
    #     entry_list = []
    #     for j in range(0, len(all_entries)):
    #         if all_books[i] == all_entries[j].book:
    #             entry_list.append(all_entries[j])
    #     entry_total.append(entry_list)
    # book_total = []
    # for b in all_books:
    #     book_total.append(b)
    #
    # list = zip(book_total, entry_total)

    context = {'books': all_books}
    return render(request, 'memcpy/books.html', context)

@login_required
@transaction.atomic
def create_book(request):
    if request.method == 'GET':
        context = {'form': CreateBookForm()}
        return render(request, 'memcpy/create-book.html', context)

    # POST method: process CreateBookForm
    user = request.user
    book = Book(author=user)
    create_book_form = CreateBookForm(request.POST, request.FILES, instance=book)
    if not create_book_form.is_valid():
        context = {'form': create_book_form}
        return render(request, 'memcpy/create-book.html', context)

    # Must copy content_type into a new model field because the model
    # FileField will not store this in the database.  (The uploaded file
    # is actually a different object than what's return from a DB read.)
    if len(request.FILES) > 0:
        book.content_type = create_book_form.cleaned_data['cover_image'].content_type

    # Save the new record
    create_book_form.save()

    messages.success(request, 'Book "%s" created' % book.title)

    # Immediately create entries for this book
    return redirect('create-entry', book_id=book.id)

#TODO: @login_required
#TODO: @transaction.atomic
def edit_book(request):
    return HttpResponse('Edit a book')

#TODO: @login_required
#TODO: @transaction.atomic
def delete_book(request):
    return HttpResponse('Delete a book')

def get_photo(request, book_id):
    item = get_object_or_404(Book, id=book_id)
    # Probably don't need this check as form validation requires a picture
    if not item.cover_image:
        raise Http404
    return HttpResponse(item.cover_image, content_type=item.content_type)

