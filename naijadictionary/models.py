from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Definition(models.Model):
    word = models.CharField(max_length=20,unique=True)
    meaning = models.CharField(max_length=1000)
    country = models.CharField(max_length=20)
    poster = models.CharField(max_length=20, null=True)
    example = models.CharField(max_length=20, null=True)
    language = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.word.upper()


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_url = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=8, null=True)
    location = models.CharField(max_length=20, null=True)
    profile_pic = models.ImageField(upload_to='profilepic',blank=True)
    

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('dashboard')


class Submited(models.Model):
    post_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="userinfo",null=True)
    user_name = models.CharField(max_length=20,null=True)
    word = models.CharField(max_length=20,unique=True,null=True)
    meaning = models.CharField(max_length=1000)
    language = models.CharField(max_length=20)
    exampe = models.CharField(max_length=200)
    status = models.CharField(max_length=20,null=True)

    def __str__(self):
        return f"{self.user_name} {self.word}"
