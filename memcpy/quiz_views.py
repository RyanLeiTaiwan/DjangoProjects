from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from memcpy.models import *
from django.db.models import Count
from .forms import *
import random
import json

### memcpy() parameters
# Minimum number of entries required to start a quiz
QUIZ_MIN_ENTRIES = 4
# Maximum number of entries sampled in a quiz
QUIZ_MAX_ENTRIES = 20

@login_required
def random_quiz(request):
    # Randomly choose one book that has >= 4 entries
    # http://stackoverflow.com/questions/6525771/django-query-related-field-count
    valid_books = Book.objects.annotate(num_entries=Count('entry')).filter(num_entries__gte=QUIZ_MIN_ENTRIES)
    if len(valid_books) == 0:
        messages.error(request, 'quiz: Cannot start a quiz! There is no book that contains at least %d entries.' % QUIZ_MIN_ENTRIES)
        return redirect('books')
    book = random.choice(valid_books)
    # Call quiz() to handle actual quiz
    return redirect('quiz', book_id=book.id)

# Can be called from Random Quiz or a specific Book page
@login_required
def quiz(request, book_id):
    context = {}
    # Check for invalid book id
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'quiz: Invalid book ID.')
        return redirect(reverse('books'))
    entry_list = list(book.entry_set.all())
    # The book should contain at least QUIZ_MIN_ENTRIES
    if len(entry_list) < QUIZ_MIN_ENTRIES:
        messages.error(request, 'quiz: Cannot quiz on this book! It has fewer than %d entries' % QUIZ_MIN_ENTRIES)
        return redirect('book', book_id=book_id)

    # Randomly order the book entries
    random.shuffle(entry_list)
    context['book'] = book
    return render(request, 'memcpy/quiz.html', context)

# Similar to entry_view.list_all_entries(), but with at most 20 entries in random permutation JSON
@login_required
def get_quiz_entries(request, book_id):
    result = {}
    # A quiz can have at most QUIZ_MAX_ENTRIES entries
    # Check for invalid book id
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'quiz: Invalid book ID.')
        return redirect(reverse('books'))
    # Django QuerySet in random order with at most MAX_ENTRIES results
    entry_list = book.entry_set.all().order_by('?')[:QUIZ_MAX_ENTRIES]

    # Serialize all information into JSON
    result['user_id'] = request.user.id
    entries = []
    for entry in entry_list:
        entry_dict = {}
        entry_dict['entry_id'] = entry.id
        entry_dict['answer'] = entry.answer
        # question_text may not exist
        if entry.question_text:
            entry_dict['question_text'] = entry.question_text
        else:
            entry_dict['question_text'] = None
        # Only record "whether" the question image exists
        if entry.question_image:
            entry_dict['question_image'] = True
        else:
            entry_dict['question_image'] = False

        entries.append(entry_dict)
    result['entries'] = entries
    response_text = json.dumps(result)

    return HttpResponse(response_text, content_type='application/json')
