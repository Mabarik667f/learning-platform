from django.db import models
from django.contrib.auth.models import AbstractUser
from services.uploadPaths import UploadPaths

class User(AbstractUser):
    pass

class Profile(models.Model):

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, default=None)
    avatar = models.ImageField(upload_to=UploadPaths.avatar_upload_path)

    objects = models.Manager()
