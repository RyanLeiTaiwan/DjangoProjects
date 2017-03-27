from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User) # associated with User
    bio = models.CharField(blank = True, max_length = 430) # a small intro
    picture = models.FileField(upload_to="images", blank = True)
    def __unicode__(self):
        return self.user.username