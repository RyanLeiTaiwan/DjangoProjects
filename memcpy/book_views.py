# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

def list_all_books(request):
    context = {}
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