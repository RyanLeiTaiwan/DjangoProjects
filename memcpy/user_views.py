from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
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

    new_profile = Profile(user=new_user,
                              bio=form.cleaned_data['bio'])
    new_profile.save()
    # Logs in the new user and redirects to home
    new_user = auth.authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    auth.login(request, new_user)
    messages.success(request, 'Registration succeeded. Welcome to memcpy().')
    return redirect(reverse('home'))


@login_required
def update_profile(request):
    user_id = request.user.id
    user = get_object_or_404(User, id=user_id)
    try:
        # Do not raise 404 exception if not found
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Create a profile on the fly if not existed. This is the case for
        # superuser, users created through admin console, or when profile is corrupted
        user_profile = Profile(user=user)
        user_profile.save()
        messages.info(request, 'New profile created.')

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
        form = UpdateProfile(user=user,
                             initial={'email': user.email, 'username': user.username, 'bio': user_profile.bio})

    context = {
        "form": form,
        "form_image": PictureForm()
    }
    return render(request, 'memcpy/update-profile.html', context)


@login_required
def upload_photo(request, user_name):
    context = {}
    user = User.objects.get(username=user_name)
    this_user = User.objects.get(username=user_name).profile
    form = PictureForm(request.POST, request.FILES, instance=this_user)
    if not form.is_valid():
        context['form_image'] = PictureForm
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        form.save()
        context['form_image'] = PictureForm()
    form = UpdateProfile(user=user, initial={'email': user.email, 'username': user.username, 'bio': this_user.bio})
    context['form'] = form
    return render(request, 'memcpy/update-profile.html', context)


@login_required
def view_profile(request, user_id):
    context = {}
    errors = []

    if request.method != 'GET':
        errors.append('Views must be done using the GET method')
    else:
        try:
            real_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("No User matches the given query.")

        context = {'user': real_user, 'errors': errors}

    return render(request, 'memcpy/view-profile.html', context)


@login_required
def get_photo(request, id):
    #item = get_object_or_404(Item, id=id)
    user_profile = User.objects.get(username=id).profile

    return HttpResponse(user_profile.picture)