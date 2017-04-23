from django import forms
import re

from django.contrib.auth.models import User
from .models import *

MAX_UPLOAD_SIZE = 2500000

# Backport Python 3.4's regular expression "fullmatch()" to Python 2
# http://stackoverflow.com/questions/30212413/backport-python-3-4s-regular-expression-fullmatch-to-python-2
def fullmatch(regex, string, flags=0):
    """Emulate python-3.4 re.fullmatch()."""
    return re.match("(?:" + regex + r")\Z", string, flags=flags)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    email = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    password1 = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())
    bio = forms.CharField(max_length=430, widget=forms.Textarea)


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Only accept usernames of letters and digits to match the format in urls.py
        username = self.cleaned_data.get('username')
        if not fullmatch('[a-zA-Z0-9]+', username):
            raise forms.ValidationError('Invalid username format. Please use only letters and digits')
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class PictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', )

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture


class UpdateProfile(forms.ModelForm):
    email = forms.CharField(max_length=50,
                            widget=forms.EmailInput())
    username = forms.CharField(max_length=20)
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'bio', )

    def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super(UpdateProfile, self).__init__(*args, **kwargs)

    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username) and username != self.user.username:
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'description', 'cover_image', 'question_label', 'answer_label', 'answer_type')
        widgets = {
            'question_label': forms.TextInput(attrs={'placeholder': 'Definition'}),
            'answer_label': forms.TextInput(attrs={'placeholder': 'Word'})
        }
    def clean_cover_image(self):
        picture = self.cleaned_data['cover_image']
        # Workaround: Existing pictures DO NOT have the content_type attribute
        if picture and hasattr(picture, 'content_type'):
            if not picture.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            if picture.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File size is too large (%.2f MB)' % (picture.size / 2**20))
        return picture

class CreateEntryForm(forms.ModelForm):
    # answer_label = 'YOUR_ANSWER_LABEL'
    # question_label = 'YOUR_QUESTION_LABEL'
    class Meta:
        model = Entry
        fields = ('answer', 'question_text', 'question_image')
        # TODO: Should be able to use user-defined question/answer labels, perhaps by using an outer function
        labels = {}
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(CreateEntryForm, self).clean()
        # At least one of text or image should not be null
        text = cleaned_data.get('question_text')
        image = cleaned_data.get('question_image')
        if not text and not image:
            raise forms.ValidationError("Text and image cannot be both empty.")
        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_question_image(self):
        picture = self.cleaned_data['question_image']
        # Workaround: Existing pictures DO NOT have the content_type attribute
        if picture and hasattr(picture, 'content_type'):
            if not picture.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            if picture.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File size is too large (%.2f MB)' % (picture.size / 2**20))
        return picture

class CreateFlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['text', 'image']
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(CreateFlashcardForm, self).clean()
        # At least one of text or image should not be null
        text = cleaned_data.get('text')
        image = cleaned_data.get('image')
        if not text and not image:
            raise forms.ValidationError("Text and image cannot be both empty.")
        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_image(self):
        picture = self.cleaned_data['image']
        # Workaround: Existing pictures DO NOT have the content_type attribute
        if picture and hasattr(picture, 'content_type'):
            if not picture.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            if picture.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File size is too large (%.2f MB)' % (picture.size / 2**20))
        return picture
