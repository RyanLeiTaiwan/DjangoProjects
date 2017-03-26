# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

def register(request):
    return HttpResponse('Registration page')

def profile(request):
    return HttpResponse('View profile page')