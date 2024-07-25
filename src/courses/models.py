from django.db import models
from django.utils import choices
from services.uploadPaths import UploadPaths

class Category(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    objects = models.Manager()

class Course(models.Model):
    class Difficulties(models.TextChoices):
        EASY = 'E', "easy"
        MEDIUM = 'M', "medium",
        HARD = 'H', "hard"

    name = models.CharField(max_length=255)
    text = models.TextField()
    price = models.IntegerField()
    img = models.ImageField(upload_to=UploadPaths.course_img_upload_path)
    difficulty = models.CharField(max_length=6, choices=Difficulties)
    category = models.ManyToManyField(to=Category, through='CourseHasCategory', related_name='courses')
    objects = models.Manager()

class CourseHasCategory(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    objects = models.Manager()

class Section(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    text = models.TextField()
    objects = models.Manager()

class Subsection(models.Model):
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    number = models.PositiveSmallIntegerField(default=1)
    objects = models.Manager()

class ContentSection(models.Model):
    subsection = models.ForeignKey(to=Subsection, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    video = models.ImageField(upload_to=UploadPaths.content_img_upload_path, blank=True)
    objects = models.Manager()

class Question(models.Model):
    content_section = models.ForeignKey(to=ContentSection, on_delete=models.CASCADE)
    text = models.TextField()
    objects = models.Manager()

class Answer(models.Model):
    text = models.CharField()
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()
