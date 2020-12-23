from django.db import models

from django.contrib.auth.models import User


class Highscore(models.Model):
    player = models.ForeignKey(
        User, related_name='player', on_delete=models.CASCADE)
    date = models.DateField()
    score = models.TextField()


class Secretassassin(models.Model):
    user = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE)
    dateOfBirth = models.DateField()
    description = models.TextField()
