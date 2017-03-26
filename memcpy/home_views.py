# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib import messages

# TODO: @login_required
def logged_in_home(request):
    context = {}
    # if request.method == 'GET':
    #     # GET request: Create a PostForm to display to the user
    #     context['form'] = PostForm()
    # else:
    #     # POST request (error): Get the form from POST data
    #     context['form'] = request.POST['form']

    # # Query all posts ordered by descending timestamp
    # all_posts = Post.objects.order_by('-timestamp')
    # context['posts'] = all_posts
    messages.success(request, 'You are logged in. Welcome back to memcpy().')
    return render(request, 'memcpy/logged_in_home.html', context)

def non_logged_in_home(request):
    context = {}
    messages.info(request, 'Info message test: Website notifications will appear here.')
    messages.success(request, 'Success message test.')
    messages.warning(request, 'Warning message test.')
    messages.error(request, 'Error message test.')
    return render(request, 'memcpy/non_logged_in_home.html', context)