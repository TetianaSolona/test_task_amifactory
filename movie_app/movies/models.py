from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def get_json_data(self):
        return {'id': self.id, 'title': self.title}


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

    def get_json_data(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_year': self.release_year,
            'mpa_rating': self.mpa_rating,
            'imdb_rating': self.imdb_rating,
            'duration': self.duration,
            'poster': self.poster.url if self.poster else None,
            'bg_picture': self.bg_picture.url if self.bg_picture else None,
            'genres': [{'id': genre.id, 'title': genre.title} for genre in self.genres.all()],
            'directors': [{'id': director.id, 'first_name': director.first_name, 'last_name': director.last_name} for
                          director in self.directors.all()],
            'writers': [{'id': writer.id, 'first_name': writer.first_name, 'last_name': writer.last_name} for writer in
                        self.writers.all()],
            'stars': [{'id': star.id, 'first_name': star.first_name, 'last_name': star.last_name} for star in
                      self.stars.all()],
        }
