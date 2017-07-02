from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
# from django.core.exceptions import ObjectDoesNotExist

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Import our model classes
from socialnetwork.models import *

# Import our form classes
from socialnetwork.forms import *

# Django messages framework
from django.contrib import messages

# Use Python's native JSON package for serialization instead of Django's serailizers
import json

# Handle datetime format and timezone in Python
import pytz

# Avoid hard-coded absolute paths
from django.conf import settings
import os

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail


# Modified from addrbook example
# Create a Profile object when registering a new User
@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Create a bound form from the request POST parameters
    # and makes the form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validate the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.

    data = form.cleaned_data
    print('Registration data\n' + str(data))
    try:
        new_user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        # New username: create a new User
        new_user = User.objects.create_user(username=data['username'],
                                            password=data['password1'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            email=data['email'])
        # Mark the user as inactive to prevent login before email confirmation.
        new_user.is_active = False
        # Also create a new Profile associated with this new User
        new_profile = Profile(user=new_user)
    else:
        # Old username (email not confirmed checked by validation)
        new_user = User.objects.select_for_update().get(username=data['username'])
        new_user.set_password(data['password1'])
        new_user.first_name = data['first_name']
        new_user.last_name = data['last_name']
        new_user.email = data['email']
        # Select old profile for update
        new_profile = Profile.objects.select_for_update().get(user=new_user)

    new_user.save()

    # Handle profile fields
    if data['age']:
        new_profile.age = data['age']
    if data['bio']:
        new_profile.bio = data['bio']

    new_profile.save()

    # Do not log in the user. We need email confirmation
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    # login(request, new_user)

    messages.success(request, 'Verify your email address.')
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
    email_body = """
    Hi %s,

    Thank you for registering at 15-637 Social Network.
    Please click the link below to verify your email address to complete your account registration:

      http://%s%s
    """ % (data['username'], request.get_host(), reverse('verify', args=(new_user.username, token)))

    send_mail(subject='15-637 Social Network: Verify your email address',
              message=email_body,
              from_email='admin@15637.com',
              recipient_list=[new_user.email])

    context['email'] = data['email']
    return render(request, 'socialnetwork/email-verification.html', context)


@transaction.atomic
def verify_email(request, username, token):
    context = {}
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Invalid username "' + username + '"for email verification')
        return render(request, 'socialnetwork/error.html', context)
    context['email'] = user.email

    # Invalid token
    if not default_token_generator.check_token(user, token):
        messages.error(request, 'Invalid email verification token. Did you copy the URL correctly?')
        return render(request, 'socialnetwork/error.html', context)

    # Already verified
    if user.is_active:
        messages.error(request, 'Your email ' + user.email + ' has already been verified. You don\'t need to do this again')
        return render(request, 'socialnetwork/error.html', context)

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'socialnetwork/verified.html', context)


@login_required
def index(request):
    context = {}
    if request.method == 'GET':
        # GET request: Create a PostForm to display to the user
        context['form'] = PostForm()
    else:
        # POST request (error): Get the form from POST data
        context['form'] = request.POST['form']

    # # Query all posts ordered by descending timestamp
    # all_posts = Post.objects.order_by('-timestamp')
    # context['posts'] = all_posts
    return render(request, 'socialnetwork/index.html', context)


@login_required
def following_stream(request):
    context = {}
    if request.method == 'GET':
        # GET request: Create a PostForm to display to the user
        context['form'] = PostForm()
    else:
        # POST request (error): Get the form from POST data
        context['form'] = request.POST['form']

    # # Query all Users (Profiles) followed by the current User (Profile)
    # follows = request.user.profile.following.all()
    # # Query all posts by following users ordered by descending timestamp
    # following_posts = Post.objects.filter(user__profile__in=follows).order_by('-timestamp')
    # context['posts'] = following_posts
    return render(request, 'socialnetwork/following.html', context)


@login_required
@transaction.atomic
def post(request):
    context = {}

    # Do nothing (redirect to homepage) with GET requests
    if request.method == 'GET':
        messages.error(request, 'You cannot post a message using GET method')
        return redirect(reverse('index'))

    # Create a Post object and associate it a PostForm with received POST data
    post = Post(user=request.user)
    post_form = PostForm(request.POST, instance=post)

    if not post_form.is_valid():
        context['form'] = post_form
        # # Query all posts ordered by descending timestamp
        # all_posts = Post.objects.order_by('-timestamp')
        # context['posts'] = all_posts
        return render(request, 'socialnetwork/index.html', context)
    # Save the new record
    post_form.save()
    messages.success(request, 'Message posted. Returned to global stream')
    return redirect(reverse('index'))


@login_required
def profile(request, user_id):
    context = {}
    # Query all posts of a specific user ordered by descending timestamp,
    # and raise an HTTP 404 exception if the user does not exist
    user = get_object_or_404(User, id=user_id)
    context['query_user'] = user

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Don't raise 404. Superuser does not have a Profile
        profile = None
    context['query_profile'] = profile

    # all_posts = user.post_set.order_by('-timestamp')
    # context['posts'] = all_posts
    return render(request, 'socialnetwork/profile.html', context)


@login_required
@transaction.atomic
def edit(request, user_id):
    try:
        if request.method == 'GET':
            # User can only edit their own profile. Otherwise, redirect to home page
            user = request.user

            if user.id != int(user_id):
                messages.error(request, 'You cannot update another user\'s profile')
                context = {
                    'form': PostForm(),
                    'posts': Post.objects.order_by('-timestamp')
                }
                return render(request, 'socialnetwork/index.html', context)

            profile = user.profile
            # Create ModelForms for updating User and Profile
            picture_form = EditPictureForm(instance=profile)
            user_form = EditUserForm(instance=user)
            profile_form = EditProfileForm(instance=profile)
            context = {
                'picture_form': picture_form,
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'socialnetwork/edit.html', context)

        # POST method: process EditPictureForm, EditUserForm, and EditProfileForm
        user = User.objects.select_for_update().get(id=user_id)
        profile = Profile.objects.select_for_update().get(user=user)

        picture_form = EditPictureForm(request.POST, request.FILES, instance=profile)
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, instance=profile)

        if not picture_form.is_valid() or not user_form.is_valid() or not profile_form.is_valid():
            context = {
                'picture_form': picture_form,
                'user_form': user_form,
                'profile_form': profile_form
            }
            return render(request, 'socialnetwork/edit.html', context)

        # Now that all forms are valid, save the edit

        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        if len(request.FILES) > 0:
            profile.content_type = picture_form.cleaned_data['picture'].content_type
        picture_form.save()
        user_form.save()
        profile_form.save()

        messages.success(request, 'Profile updated')
        # Create ModelForms for updating User and Profile
        picture_form = EditPictureForm(instance=profile)
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)
        context = {
            'picture_form': picture_form,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'socialnetwork/edit.html', context)
    except Profile.DoesNotExist:
        # This is the case for the superuser, or users created through admin console
        user = request.user
        new_profile = Profile(user=user)
        new_profile.save()
        # Create ModelForms for updating both User and Profile
        picture_form = EditPictureForm(instance=new_profile)
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=new_profile)
        messages.info(request, 'Created your profile on the fly')
        context = {
            'picture_form': picture_form,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'socialnetwork/edit.html', context)


@login_required
def get_picture(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    if not profile.picture:
        # Default profile picture (hard-coded URL since it appears only once)
        # http://stackoverflow.com/questions/3003146/best-way-to-write-an-image-to-a-django-httpresponse
        path = os.path.join(settings.STATIC_ROOT, 'socialnetwork/default_user.svg')
        # print(path)
        return HttpResponse(content=open(path, 'rb').read(),
                            content_type='image/svg+xml')
        # raise Http404
    return HttpResponse(profile.picture, content_type=profile.content_type)


@login_required
@transaction.atomic
def follow(request, user_id):
    # Do nothing (redirect to homepage) with GET requests
    if request.method == 'GET':
        messages.error(request, 'You cannot follow a user using GET method')
        return redirect(reverse('index'))
    else:
        try:
            follower = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'You cannot follow an non-existent user')
            return redirect(reverse('index'))
        request.user.profile.following.add(follower.profile)
        # Don't need to "save" this relationship
        messages.success(request, 'Followed "' + str(follower.username) + '". Returned to global stream')
        return redirect(reverse('index'))


@login_required
@transaction.atomic
def unfollow(request, user_id):
    # Do nothing (redirect to homepage) with GET requests
    if request.method == 'GET':
        messages.error(request, 'You cannot unfollow a user using GET method')
        return redirect(reverse('index'))
    else:
        try:
            follower = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'You cannot unfollow an non-existent user')
            return redirect(reverse('index'))
        request.user.profile.following.remove(follower.profile)
        # Don't need to "save" this relationship
        messages.success(request, 'Unfollowed "' + str(follower.username) + '". Returned to global stream')
        return redirect(reverse('index'))


@login_required
def get_posts_comments(request, user_id):
    # Serialize everything we want JavaScript to display in result list
    # https://piazza.com/class/iy0qa81i5xl1qz?cid=449
    # Use method 1: Aggregate your models into a list
    result = []

    # @param user_id
    #   0: global stream
    #   -1: following stream
    #   others: get posts of a specific user (in Profile page)
    posts = None
    if user_id == "0":
        # Query all posts ordered by ascending timestamp
        posts = Post.objects.order_by('timestamp')
    elif user_id == "-1":
        # Query all Users (Profiles) followed by the current User (Profile)
        follows = request.user.profile.following.all()
        # Query all posts by following users ordered by ascending timestamp
        posts = Post.objects.filter(user__profile__in=follows).order_by('timestamp')
    else:
        user = get_object_or_404(User, id=user_id)
        posts = user.post_set.order_by('timestamp')

    for post in posts:
        post_fields = {}
        post_fields['post_id'] = post.id
        post_fields['text'] = post.text
        post_fields['user_id'] = post.user_id
        post_fields['username'] = post.user.username
        # Directly convert to a string of desired format to prevent serialization errors
        post_ts = post.timestamp.astimezone(pytz.timezone('America/New_York'))
        post_fields['timestamp'] = post_ts.strftime('%Y-%m-%d %H:%M:%S')
        # Directly compute whether the user can follow the post author
        # -1: show nothing (their own post)
        # 0: show unfollow
        # 1: show follow
        if post.user_id == request.user.id:
            post_fields['follow'] = -1
        elif post.user.profile in request.user.profile.following.all():
            post_fields['follow'] = 0
        else:
            post_fields['follow'] = 1

        # Comments on the post
        comments = []
        # Display comment in ascending timestamp
        for comment in post.comment_set.order_by('timestamp'):
            comment_fields = {}
            comment_fields['comment_id'] = comment.id
            comment_fields['text'] = comment.text
            comment_fields['user_id'] = comment.user_id
            comment_fields['username'] = comment.user.username
            comment_ts = comment.timestamp.astimezone(pytz.timezone('America/New_York'))
            comment_fields['timestamp'] = comment_ts.strftime('%Y-%m-%d %H:%M:%S')
            if comment.user_id == request.user.id:
                comment_fields['follow'] = -1
            elif comment.user.profile in request.user.profile.following.all():
                comment_fields['follow'] = 0
            else:
                comment_fields['follow'] = 1
            comments.append(comment_fields)

        post_fields['comments'] = comments
        result.append(post_fields)

    # print(result)
    response_text = json.dumps(result)
    return HttpResponse(response_text, content_type='application/json')


@login_required
def comment(request, post_id, param_user_id):
    # Do nothing (redirect to homepage) with GET requests
    if request.method == 'GET':
        messages.error(request, 'You cannot add a comment using GET method')
        return redirect(reverse('index'))

    # Check for invalid post_id
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        message = 'You cannot add a comment to an invalid post'
        json_message = '{ "error": "' + message + '" }'
        return HttpResponse(json_message, content_type='application/json')

    # Create a Comment object and associate it a CommentForm with received POST data
    comment = Comment(post=post, user=request.user)
    comment_form = CommentForm(request.POST, instance=comment)

    if not comment_form.is_valid():
        message = 'Empty comment or comment length > 160 characters.'
        json_message = '{ "error": "' + message + '" }'
        return HttpResponse(json_message, content_type='application/json')

    # Save the new record
    comment_form.save()

    # Reuse get_posts_comments() with global param_user_id from JavaScript
    return get_posts_comments(request, param_user_id)