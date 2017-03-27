# Import Django stuff (refer to HW)
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db import transaction

from memcpy.forms import *


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('home'))

@transaction.atomic
def register(request):

    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'memcpy/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'memcpy/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
    new_user.save()

    new_userprofile = UserProfile(user=new_user,
                                  bio=form.cleaned_data['bio'])
    new_userprofile.save()
    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def update_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(id=user.id)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, user=user, initial={'email': user.email,
                                                    'username': user.username,
                                                    'bio': user_profile.bio})
        if form.is_valid():
            user_profile.bio = request.POST['bio']
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.save()
            user_profile.save()
            return redirect(reverse('home'))
    else:
        form = UpdateProfile()

    context = {
        "form": form,
        "form_image": PictureForm()
    }
    return render(request, 'memcpy/update-profile.html', context)

@login_required
def upload_photo(request, user):
    context = {}
    this_user = User.objects.get(username=user).userprofile
    form = PictureForm(request.POST, request.FILES, instance=this_user)
    if not form.is_valid():
        context['form_image'] = form
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        form.save()
        context['form_image'] = PictureForm()
    form = UpdateProfile()
    context['form'] = form
    return render(request, 'memcpy/update-profile.html', context)


def profile(request):
    return HttpResponse('View profile page')

@login_required
def get_photo(request, id):
    #item = get_object_or_404(Item, id=id)
    user_profile = User.objects.get(username=id).userprofile

    return HttpResponse(user_profile.picture)