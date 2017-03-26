# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

def list_book(request):
    return HttpResponse('List the content of a book')

def create_book(request):
    return HttpResponse('Create a book')

def edit_book(request):
    return HttpResponse('Edit a book')

def delete_book(request):
    return HttpResponse('Delete a book')