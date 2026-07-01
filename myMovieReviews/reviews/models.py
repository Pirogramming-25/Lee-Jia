from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    runtime = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.title