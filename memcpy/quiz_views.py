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

@login_required
def random_quiz(request):
    # Randomly choose one book that has >= 4 entries
    # http://stackoverflow.com/questions/6525771/django-query-related-field-count
    threshold = 4
    valid_books = Book.objects.annotate(num_entries=Count('entry')).filter(num_entries__gte=threshold)
    if len(valid_books) == 0:
        messages.error(request, 'quiz: Cannot start a quiz! There is no book that contains at least %d entries.' % threshold)
        return redirect('books')
    book = random.choice(valid_books)
    # Call quiz() to handle actual quiz
    return redirect('quiz', book_id=book.id)

# Can be called by Random Quiz or a specific Book page
@login_required
def quiz(request, book_id):
    context = {}
    book = Book.objects.get(id=book_id)
    # Randomly order the book entries
    entry_list = list(book.entry_set.all())
    random.shuffle(entry_list)

    # TODO: hard-code entry_index for now. This should be handled by JavaScript
    entry_index = 0
    context['book'] = book
    context['entry_list'] = entry_list
    context['entry'] = entry_list[entry_index]
    context['entry_index'] = entry_index
    context['progress'] = round((entry_index + 1.0) / len(entry_list) * 100)

    return render(request, 'memcpy/quiz-entries.html', context)

# TODO: Consider deleting this function
@login_required
def start_quiz(request):
    context = {}
    book_id = 1
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'book: Invalid book ID.')
        return redirect(reverse('books'))
    entry_list = Entry.objects.all().filter(book=book)
    context = {'entry_list': entry_list, 'book': book}
    return render(request, 'memcpy/quiz-home.html', context)

# TODO: Consider deleting this function
@login_required
def quiz_entries(request, book_id, entry_index):
    # book id should be randomly choosen
    # or the recently learned book
    book_id = 1
    # Check for invalid book id
    try:
            book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'book: Invalid book ID.')
        return redirect(reverse('books'))

    entry_list = Entry.objects.all().filter(book=book)

    entry_index = int(entry_index)
    entry_index += 1
    context = {}
    try:
        context = {'book': book, 'entry_list': entry_list, 'entry': entry_list[entry_index], 'entry_index': entry_index}
    except:
        pass
    answer_candidate_index = []
    answer_candidate_index.append(entry_index)
    for i in range(0, 3):
        ran = -1
        while (ran == -1 or ran in answer_candidate_index):
            ran = random.randint(0, len(entry_list) - 1)
        answer_candidate_index.append(ran)
    print (answer_candidate_index)

    if entry_index + 1 < len(entry_list):
        context['next_entry'] = entry_list[entry_index + 1]
    else:
        context['message'] = "Quiz finished! And this time you got 4/7 correct answers! Cong!"
        return render(request, 'memcpy/quiz-home.html', context)

    answer_candidate_1 = entry_list[answer_candidate_index[0]]
    answer_candidate_2 = entry_list[answer_candidate_index[1]]
    answer_candidate_3 = entry_list[answer_candidate_index[2]]
    answer_candidate_4 = entry_list[answer_candidate_index[3]]
    context["answer_candidate_1"] = answer_candidate_1
    context["answer_candidate_2"] = answer_candidate_2
    context["answer_candidate_3"] = answer_candidate_3
    context["answer_candidate_4"] = answer_candidate_4

    print context
    # print context, len(entry_list)
    return render(request, 'memcpy/quiz-entries.html', context)
