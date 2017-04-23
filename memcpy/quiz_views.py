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


def list_all_books(request):
    all_books = Book.objects.all()
    # Ryan: Don't list details in books.html
    context = {'books': all_books}
    return render(request, 'memcpy/books.html', context)

@login_required
@transaction.atomic
def create_book(request):
    if request.method == 'GET':
        context = {'form': CreateBookForm()}
        return render(request, 'memcpy/create-book.html', context)

    # POST method: process CreateBookForm
    user = request.user
    book = Book(author=user)
    create_book_form = CreateBookForm(request.POST, request.FILES, instance=book)
    if not create_book_form.is_valid():
        context = {'form': create_book_form}
        return render(request, 'memcpy/create-book.html', context)

    # Must copy content_type into a new model field because the model
    # FileField will not store this in the database.  (The uploaded file
    # is actually a different object than what's return from a DB read.)
    if len(request.FILES) > 0:
        book.content_type = create_book_form.cleaned_data['cover_image'].content_type

    # Save the new record
    create_book_form.save()

    messages.success(request, 'Book "%s" created' % book.title)

    # Immediately create entries for this book
    return redirect('create-entry', book_id=book.id)

#TODO: @login_required
#TODO: @transaction.atomic
def edit_book(request):
    return HttpResponse('Edit a book')

#TODO: @login_required
#TODO: @transaction.atomic
def delete_book(request):
    return HttpResponse('Delete a book')

def get_photo(request, book_id):
    item = get_object_or_404(Book, id=book_id)
    # Probably don't need this check as form validation requires a picture
    if not item.cover_image:
        raise Http404
    return HttpResponse(item.cover_image, content_type=item.content_type)

