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
from memcpy.models import *
import datetime
from datetime import date

def home(request):
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

    # messages.info(request, 'Info message test.')
    # messages.success(request, 'Success message test.')
    # messages.warning(request, 'Warning message test.')
    # messages.error(request, 'Error message test.')

    # get the web statistics

    # get the number of users
    users = User.objects.all()

    # get the number of all books
    books = Book.objects.all()

    # get the number of all entries
    entries = Entry.objects.all()

    # get the number of all flashcards
    flashcards = Flashcard.objects.all()

    # pick flashcard
    flashcardtoday = FlashcardToday.objects.all()
    now = date.today()

    # if the set is empty
    if not flashcardtoday:
        random_c = Flashcard.objects.order_by('?').first()
        if random_c:
            new_today = FlashcardToday(fctoday=random_c, updated_time=now)
            new_today.save()
    else:
        # refresh every day
        flashcardtoday = FlashcardToday.objects.all()[0]
        if flashcardtoday.updated_time < now:
            FlashcardToday.objects.all().delete()
            random_c = Flashcard.objects.order_by('?').first()
            new_today = FlashcardToday(fctoday=random_c, updated_time=now)
            new_today.save()

    if FlashcardToday.objects.all():
        flashcardtoday = FlashcardToday.objects.all()[0]
        fc = flashcardtoday.fctoday
        c = Flashcard.objects.get(id=fc.id)
    else:
        c = 0

    context = {'user_num': len(users), 'book_num': len(books), 'entry_num': len(entries),
               'flashcard_num': len(flashcards), 'fc_today': c}
    return render(request, 'memcpy/home.html', context)
