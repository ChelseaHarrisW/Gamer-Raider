from django.db import models

class Photos(models.Model):
    photo = models.ImageField(upload_to="images/")
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)