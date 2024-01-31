from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    TYPES = [
        ('director', 'Director'),
        ('writer', 'Writer'),
        ('actor', 'Actor'),
    ]
    types = models.CharField(max_length=10, choices=TYPES)


class Movie(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    poster = models.FileField(upload_to='posters/')
    bg_picture = models.FileField(upload_to='backgrounds/')
    release_year = models.IntegerField()
    MPA_RATING_CHOICES = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    ]
    mpa_rating = models.CharField(max_length=5, choices=MPA_RATING_CHOICES)
    imdb_rating = models.FloatField()
    duration = models.IntegerField()

    # Many-to-Many relationships
    genres = models.ManyToManyField(Genre, related_name='movies')
    directors = models.ManyToManyField(Person, related_name='directed_movies')
    writers = models.ManyToManyField(Person, related_name='written_movies')
    stars = models.ManyToManyField(Person, related_name='starred_movies')
