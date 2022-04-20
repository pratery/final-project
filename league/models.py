from django.db import models
from django.contrib.auth.models import User

class Conference(models.Model):
    # A conference is a collection of teams and is part of the League.
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Returns a string representation of the conference
        return self.name

class Team(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "teams"

    def __str__(self):
        # Return a string representation of the team
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "players"

    def __str__(self):
        return self.name
