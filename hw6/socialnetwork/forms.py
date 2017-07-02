from django import forms
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(forms.Form):
    username   = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    password1  = forms.CharField(max_length = 200, label='Password', widget=forms.PasswordInput)
    password2  = forms.CharField(max_length = 200, label='Confirm password', widget=forms.PasswordInput)
    # TODO: optional profile picture
    age        = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput)
    bio        = forms.CharField(required=False, max_length=430, label='Short bio (<= 430 char)', widget=forms.Textarea)

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
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data dictionary
        return username


# Refactor post form to use Django ModelForm
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'What\'s on your mind?'})
        }


# Side note: AJAX + ModelForm: https://realpython.com/blog/python/django-and-ajax-form-submissions/
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class EditUserForm(forms.ModelForm):
    # Explicitly require first_name and last_name (not required in User model)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'bio']
        labels = {'bio': 'Short bio (<= 430 char)'}


class EditPictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']
        labels = {'picture': 'Upload (<= 4 MB)'}
        # # Override the default "currently + clear" fields
        # widgets = {
        #     'picture': forms.FileInput
        # }
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        # Workaround: Existing pictures DO NOT have the content_type attribute
        print('content_type: ' + str(hasattr(picture, 'content_type')))
        if picture and hasattr(picture, 'content_type'):
            if not picture.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            MAX_UPLOAD_SIZE = 4194304
            if picture.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File size is too large (%.2f MB)' % (picture.size / 2**20))
        return picture
