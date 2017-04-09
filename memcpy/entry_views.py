from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from datetime import datetime
from memcpy.models import *
from .forms import *

def list_all_entries(request, book_id):
    # Check for invalid book id
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'book: Invalid book ID.')
        return redirect(reverse('books'))

    entry_list = Entry.objects.all().filter(book = book)

    context = {'book': book, 'entry_list': entry_list}
    # print context, len(entry_list)
    return render(request, 'memcpy/book.html', context)

def view_entry(request):
    return HttpResponse('View the content of an entry')

@login_required
@transaction.atomic
def create_entry(request, book_id):
    context = {}
    # Check for invalid book id
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'create-entry: Invalid book ID.')
        return redirect(reverse('books'))

    # Only the book author can create entries
    if (book.author_id != request.user.id):
        messages.error(request, 'create-entry: Only the book author can create entries.')
        return redirect(reverse('books'))

    if request.method == 'GET':
        context = {'form': CreateEntryForm(), 'book': book}
        return render(request, 'memcpy/create-entry.html', context)

    # POST method: process CreateEntryForm
    user = request.user
    entry = Entry(book=book)
    create_entry_form = CreateEntryForm(request.POST, request.FILES, instance=entry)
    if not create_entry_form.is_valid():
        context = {'form': create_entry_form, 'book': book}
        return render(request, 'memcpy/create-entry.html', context)

    # Must copy content_type into a new model field because the model
    # FileField will not store this in the database.  (The uploaded file
    # is actually a different object than what's return from a DB read.)
    if len(request.FILES) > 0:
        entry.content_type = create_entry_form.cleaned_data['question_image'].content_type

    # Save the new record
    create_entry_form.save()
    # Also update the book timestamp
    book.timestamp = datetime.now()
    book.save()

    messages.success(request, 'Entry "%s" created' % entry.answer)
    # Return a new CreateEntryForm immediately after success
    context = {'form': CreateEntryForm(), 'book': book}

    return render(request, 'memcpy/create-entry.html', context)

#TODO: @login_required
#TODO: @transaction.atomic
def edit_entry(request):
    return HttpResponse('Edit a entry')

#TODO: @login_required
#TODO: @transaction.atomic
def delete_entry(request):
    return HttpResponse('Delete an entry')

def get_photo(request, id):
    item = get_object_or_404(Entry, id=id)
    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.question_image:
        raise Http404
    return HttpResponse(item.question_image, content_type=item.content_type)
