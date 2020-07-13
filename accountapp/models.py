from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    introduction = models.TextField(blank=True)
    image = ProcessedImageField(
        blank = True,
        upload_to = 'profile/images',
        processors = [ResizeToFill(300,300)],
        format = 'JPEG',
        options = {'quality': 60},
    )

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')