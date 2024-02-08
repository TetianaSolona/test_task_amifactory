from django.test import TestCase
from django.urls import reverse
from .models import Movie, Genre, Person


class GenreListViewTests(TestCase):
    def setUp(self):
        self.genre1 = Genre.objects.create(title='Test_genre_1')
        self.genre2 = Genre.objects.create(title='Test_genre_2')

    def test_genre_list_view_success(self):
        response = self.client.get(reverse('genre-list'))
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {'id': self.genre1.id, 'title': 'Test_genre_1'},
            {'id': self.genre2.id, 'title': 'Test_genre_2'},
        ]
        self.assertJSONEqual(response.content, expected_data)

    def test_genre_list_view_exception(self):
        with self.assertRaises(Exception):
            response = self.client.get(reverse('genre-list'))
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json())


class MovieViewsTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(title='Test_genre')
        self.director = Person.objects.create(first_name='Test_director', last_name='Test_director', types='director')
        self.writer = Person.objects.create(first_name='Test_writer', last_name='Test_writer', types='writer')
        self.star = Person.objects.create(first_name='Test_star', last_name='Test_star', types='actor')
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='A test movie',
            release_year=2023,
            mpa_rating='PG',
            imdb_rating=10,
            duration=90,
            poster=None,
            bg_picture=None,
        )
        self.movie.genres.add(self.genre)
        self.movie.directors.add(self.director)
        self.movie.writers.add(self.writer)
        self.movie.stars.add(self.star)

    def test_movie_detail_view_success(self):
        response = self.client.get(reverse('movie-detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'id': self.movie.id,
            'title': 'Test Movie',
            'description': 'A test movie',
            'release_year': 2023,
            'mpa_rating': 'PG',
            'imdb_rating': 10,
            'duration': 90,
            'poster': None,
            'bg_picture': None,
            'genres': [{'id': self.genre.id, 'title': 'Test_genre'}],
            'directors': [{'id': self.director.id, 'first_name': 'Test_director', 'last_name': 'Test_director'}],
            'writers': [{'id': self.writer.id, 'first_name': 'Test_writer', 'last_name': 'Test_writer'}],
            'stars': [{'id': self.star.id, 'first_name': 'Test_star', 'last_name': 'Test_star'}],
        }
        self.assertJSONEqual(response.content, expected_data)

    def test_movie_detail_view_not_found(self):
        response = self.client.get(reverse('movie-detail', args=[90]))
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Movie not found'})

    def test_movie_list_view_success(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'pages': 1,
            'total': 1,
            'results': [
                {
                    'id': self.movie.id,
                    'title': 'Test Movie',
                    'description': 'A test movie',
                    'release_year': 2023,
                    'mpa_rating': 'PG',
                    'imdb_rating': 10,
                    'duration': 90,
                    'poster': None,
                    'bg_picture': None,
                    'genres': [{'id': self.genre.id, 'title': 'Test_genre'}],
                    'directors': [
                        {'id': self.director.id, 'first_name': 'Test_director', 'last_name': 'Test_director'}],
                    'writers': [{'id': self.writer.id, 'first_name': 'Test_writer', 'last_name': 'Test_writer'}],
                    'stars': [{'id': self.star.id, 'first_name': 'Test_star', 'last_name': 'Test_star'}],
                }
            ],
        }
        self.assertJSONEqual(response.content, expected_data)
