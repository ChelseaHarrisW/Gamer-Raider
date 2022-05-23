from django.db import models
from .rating import Rating

class Game(models.Model):
    title = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    year_released = models.CharField(max_length=50)
    number_of_players = models.IntegerField()
    age_recomendations = models.IntegerField()
    creator = models.ForeignKey("Player", on_delete=models.CASCADE)
    estimated_time_to_play = models.CharField(max_length=50)
    category = models.ManyToManyField("Category", related_name="categories")