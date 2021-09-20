from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User




        

class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    expert = models.BooleanField(default=False)
    courses = ArrayField(models.CharField(max_length=30, unique=False, blank=False), unique=False, blank=True, default=list)
    interests = ArrayField(models.CharField(max_length=20, unique=False, blank=False), blank=False, default=list)
    bio = models.TextField(max_length=1000, unique=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-user']

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name






class Materials(models.Model):
    author = models.CharField(max_length=100, unique=False, blank=False)
    files = ArrayField(models.FileField(upload_to="materials/"), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-author']
        verbose_name_plural = 'Materials'

    def __str__(self) -> str:
        return self.author






class Course(models.Model):
    name = models.CharField(max_length=30, unique=False, blank=False)
    materials = models.ForeignKey(Materials, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, unique=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-name']

    def __str__(self) -> str:
        return self.name




class Test(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=False)
    creator = models.OneToOneField(Account, on_delete=models.DO_NOTHING)
    questions = ArrayField(models.TextField(max_length=1000, blank=False, unique=False), blank=False, default=list)
    answers = ArrayField(models.TextField(max_length=1000, blank=False, unique=False), blank=False, default=list)
    category = models.CharField(max_length=20, unique=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-name']

    def __str__(self) -> str:
        return self.name




class JWT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-user']

    def __str__(self):
        return self.user.username