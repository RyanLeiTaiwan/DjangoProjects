from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
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
    return render(request, 'memcpy/entries.html', context)

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
        context = {'form': create_entry_form}
        return render(request, 'memcpy/create-entry.html', context)

    # Save the new record
    create_entry_form.save()

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

def learn(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    if not entry or not entry.book:
        return Http404
    book_id = entry.book.id
    all_entries = Entry.objects.all().filter(book = book_id)
    entry_list = []
    next_flag = False
    next_id = 0
    for j in range(0, len(all_entries)):
        entry_list.append(all_entries[j])
        if next_flag:
            next_id = all_entries[j].id
            next_flag = False
        if (all_entries[j].id == int(entry_id)):
            next_flag = True
    context = {"entry_list": entry_list, "current_id": int(entry_id), "next_id": int(next_id)}
    print context, len(entry_list)
    return render(request, 'memcpy/learning_mode.html', context)
def get_photo(request, id):
    item = get_object_or_404(Entry, id=id)
    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.question_image:
        raise Http404
    return HttpResponse(item.question_image)
