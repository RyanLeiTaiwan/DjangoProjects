from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from memcpy.models import *

def list_all_flashcards(request, entry_id):
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
    print 'context: %s' % context
    print 'len(entry_list): %d' % len(entry_list)
    return render(request, 'memcpy/entry.html', context)


def list_flashcard(request):
    return HttpResponse('List the content of a flashcard')

def create_flashcard(request):
    return HttpResponse('Create a flashcard')

def edit_flashcard(request):
    return HttpResponse('Edit a flashcard')

def delete_flashcard(request):
    return HttpResponse('Delete a flashcard')
