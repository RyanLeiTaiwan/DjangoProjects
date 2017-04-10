from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from memcpy.models import *
from .forms import *

@login_required
def list_flashcard(request):
    return HttpResponse('View the content of a flashcard')

@login_required
@transaction.atomic
def create_flashcard(request, entry_id):
    # Check for invalid entry id
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        messages.error(request, 'create-flashcard: Invalid entry ID.')
        return redirect(reverse('books'))

    # Also display current flashcards
    flashcard_list = Flashcard.objects.filter(entry=entry)

    if request.method == 'GET':
        context = {'form': CreateFlashcardForm(), 'entry': entry, 'flashcard_list': flashcard_list}
        return render(request, 'memcpy/create-flashcard.html', context)


    # POST method: process CreateFlashcardForm
    user = request.user
    flashcard = Flashcard(author=user, entry=entry)
    create_flashcard_form = CreateFlashcardForm(request.POST, request.FILES, instance=flashcard)
    if not create_flashcard_form.is_valid():
        # Validation error does not belong to a single field, so we send a Django message
        for error in create_flashcard_form.errors['__all__']:
            messages.error(request, 'create-flashcard: %s' % error)
        context = {'form': create_flashcard_form, 'entry': entry, 'flashcard_list': flashcard_list}
        return render(request, 'memcpy/create-flashcard.html', context)

    # Must copy content_type into a new model field because the model
    # FileField will not store this in the database.  (The uploaded file
    # is actually a different object than what's return from a DB read.)
    if len(request.FILES) > 0:
        flashcard.content_type = create_flashcard_form.cleaned_data['image'].content_type

    # Save the new record
    create_flashcard_form.save()

    messages.success(request, 'Flashcard for entry "%s" created' % entry.answer)

    return redirect('entry', entry_id=entry_id)

# TODO: @login_required
# TODO: @transaction.atomic
def edit_flashcard(request):
    return HttpResponse('Edit a flashcard')

# TODO: @login_required
# TODO: @transaction.atomic
def delete_flashcard(request):
    return HttpResponse('Delete a flashcard')

@login_required
def get_photo(request, flashcard_id):
    item = get_object_or_404(Flashcard, id=flashcard_id)
    # Probably don't need this check as form validation requires a picture
    if not item.image:
        raise Http404
    return HttpResponse(item.image, content_type=item.content_type)
