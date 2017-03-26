# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

def list_flashcard(request):
    return HttpResponse('List the content of a flashcard')

def create_flashcard(request):
    return HttpResponse('Create a flashcard')

def edit_flashcard(request):
    return HttpResponse('Edit a flashcard')

def delete_flashcard(request):
    return HttpResponse('Delete a flashcard')
