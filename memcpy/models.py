from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User) # associated with User
    bio = models.TextField(blank=True, max_length=300) # a small intro
    picture = models.FileField(null=True, blank=True, upload_to='upload/profile')
    content_type = models.CharField(null=True, blank=True, max_length=20)
    def __unicode__(self):
        return 'id: %s, username: %s' % (self.id, self.user.username)

class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Last modified timestamp: https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.DateField
    timestamp = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    cover_image = models.FileField(null=True, blank=True, upload_to='upload/book')
    content_type = models.CharField(null=True, blank=True, max_length=20)
    question_label = models.CharField(max_length=20)
    answer_label = models.CharField(max_length=20)
    # Answer type should be consistent across the whole book. Use drop-down list to select one type
    # https://docs.djangoproject.com/en/1.8/ref/models/fields/#choices
    answer_type = models.CharField(max_length=5,
                                   default='text',
                                   choices=[('text', 'text'), ('image', 'image')])
    def __unicode__(self):
        return 'id: %s, title: %s' % (self.id, self.title)

class Entry(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Answer is always text
    answer = models.CharField(max_length=50)
    # Question can be either text or image, validated on server side
    question_text = models.TextField(null=True, blank=True, max_length=200)
    question_image = models.FileField(null=True, blank=True, upload_to='upload/entry')
    def __unicode__(self):
        return 'id: %s, answer: %s' % (self.id, self.answer)


class Flashcard(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Last modified timestamp: https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.DateField
    timestamp = models.DateTimeField(auto_now=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    # Can be at least one of text, image, or audio, validated on server side
    text = models.TextField(null=True, blank=True, max_length=100)
    image = models.FileField(null=True, blank=True, upload_to='upload/flashcard_image')
    content_type = models.CharField(null=True, blank=True, max_length=20)
    # Forget about audio for now
    # audio = models.FileField(null=True, blank=True, upload_to='upload/flashcard_audio')
    def __unicode__(self):
        return 'id: %s, entry: %s, author: %s' % (self.id, self.entry, self.author.username)

class UserEntryPair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    # User's chosen flashcard for this entry
    flashcard = models.ForeignKey(Flashcard)
    def __unicode__(self):
        return 'id: %s, username: %s, entry: %s' % (self.id, self.user.username, self.entry.answer)

class FlashcardToday(models.Model):
    #TODO: faking for now
    fctoday = models.ForeignKey(Flashcard, related_name='fctoday')
    updated_time = models.DateField()
    def __unicode__(self):
        return 'id: %s, entry: %s' % (self.id, self.entry)

