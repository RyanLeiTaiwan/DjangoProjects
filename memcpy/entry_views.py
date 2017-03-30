# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from memcpy.models import *

def list_all_entries(request, book_id):
    entry_list = Entry.objects.all().filter(book = int(book_id))

    #entry_list = []

    context = {"entry_list": entry_list}
    print context, len(entry_list)
    messages.debug(request, 'List all entries in this book')
    return render(request, 'memcpy/entries.html', context)

#TODO: @login_required
#TODO: @transaction.atomic
def create_entry(request):
    return HttpResponse('Create an entry')

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
