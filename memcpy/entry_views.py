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

    entry_list = Entry.objects.all().filter(book=book)

    context = {'book': book, 'entry_list': entry_list}
    print (context)
    # print context, len(entry_list)
    return render(request, 'memcpy/book.html', context)

@login_required
def view_entry(request, entry_id):
    try:
        entry = Entry.objects.get(id = entry_id)
    except Entry.DoesNotExist:
        messages.error(request, 'entry: Invalid entry ID.')
        return redirect(reverse('books'))

    book_id = entry.book.id
    all_entries = Entry.objects.filter(book = book_id)
    current_idx = -1
    # next_flag = False
    prev_id = 0
    prev_id_tmp = 0
    next_id = 0

    # http://stackoverflow.com/questions/1042596/get-the-index-of-an-element-in-a-queryset
    for idx, ent in enumerate(all_entries):
        # if next_flag:
        #     break
        current_id = ent.id
        if current_id == int(entry_id):
            # Found target entry
            prev_id = prev_id_tmp
            current_idx = idx
            if idx < len(all_entries) - 1:
                next_id = all_entries[idx + 1].id
            # next_flag = True
        prev_id_tmp = current_id

    # Also display current flashcards
    flashcard_list = Flashcard.objects.filter(entry=entry)

    context = {
        'book': entry.book,
        'entry': entry,
        'progress': round((current_idx + 1.0) / len(all_entries) * 100),
        'prev_id': prev_id,
        'current_id': int(entry_id),
        'next_id': int(next_id),
        'flashcard_list': flashcard_list
    }
    # print 'context: %s' % context
    return render(request, 'memcpy/entry.html', context)

@login_required
@transaction.atomic
def create_entry(request, book_id):
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

    # Also display current entries
    entry_list = Entry.objects.filter(book=book)

    if request.method == 'GET':
        context = {'form': CreateEntryForm(), 'book': book, 'entry_list': entry_list}
        return render(request, 'memcpy/create-entry.html', context)

    # POST method: process CreateEntryForm
    entry = Entry(book=book)
    create_entry_form = CreateEntryForm(request.POST, request.FILES, instance=entry)
    if not create_entry_form.is_valid():
        context = {'form': create_entry_form, 'book': book, 'entry_list': entry_list}
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

    # Query again to update entry_list
    entry_list = Entry.objects.filter(book=book)
    messages.success(request, 'Entry "%s" created' % entry.answer)
    # Return a new CreateEntryForm immediately after success
    context = {'form': CreateEntryForm(), 'book': book, 'entry_list': entry_list}

    return render(request, 'memcpy/create-entry.html', context)

#TODO: @login_required
#TODO: @transaction.atomic
def edit_entry(request):
    return HttpResponse('Edit a entry')

#TODO: @login_required
#TODO: @transaction.atomic
def delete_entry(request):
    return HttpResponse('Delete an entry')

def get_photo(request, entry_id):
    item = get_object_or_404(Entry, id=entry_id)
    # Probably don't need this check as form validation requires a picture
    if not item.question_image:
        raise Http404
    return HttpResponse(item.question_image, content_type=item.content_type)
