from django.db import models

class Review(models.Model):
    content = models.CharField(max_length=120)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)