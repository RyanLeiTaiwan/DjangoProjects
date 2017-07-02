from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.TextField(max_length=160)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Automatically set the field to "now" when the Post object is first created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'post id = ' + str(self.id) + ', user = "' + str(self.user) + '", text = "' + self.text + '"'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(null=True, blank=True, upload_to='images')
    content_type = models.CharField(null=True, blank=True, max_length=50)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=430)
    # People that the current user follows
    following = models.ManyToManyField('Profile', related_name='followers')

    def __str__(self):
        return 'profile id = ' + str(self.id) + ', user = "' + str(self.user) + '", picture = ' + str(self.picture)

class Comment(models.Model):
    # Set the same max_length as that of Post.text
    text = models.TextField(max_length=160)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Automatically set the field to "now" when the Post object is first created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'comment id = ' + str(self.id) + ', post id = ' + str(self.post_id) +\
               ', user = "' + str(self.user) + '", text = "' + self.text + '"'
