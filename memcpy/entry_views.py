# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

def list_entry(request):
    return HttpResponse('List the content of an entry')

def create_entry(request):
    return HttpResponse('Create an entry')

def edit_entry(request):
    return HttpResponse('Edit an entry')

def delete_entry(request):
    return HttpResponse('Delete an entry')