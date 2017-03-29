# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from memcpy.models import *


def list_all_books(request):
    all_books = Book.objects.all()
    all_entries = Entry.objects.all()

    entry_total = []
    for i in range(0, len(all_books)):
        entry_list = []
        for j in range(0, len(all_entries)):
            if all_books[i] == all_entries[j].book:
                entry_list.append(all_entries[j])
        entry_total.append(entry_list)
    book_total = []
    for b in all_books:
        book_total.append(b)

    list = zip(book_total, entry_total)
    context = {"list": list}
    messages.debug(request, 'List all books')
    return render(request, 'memcpy/books.html', context)

#TODO: @login_required
#TODO: @transaction.atomic
def create_book(request):
    return HttpResponse('Create a book')

#TODO: @login_required
#TODO: @transaction.atomic
def edit_book(request):
    return HttpResponse('Edit a book')

#TODO: @login_required
#TODO: @transaction.atomic
def delete_book(request):
    return HttpResponse('Delete a book')