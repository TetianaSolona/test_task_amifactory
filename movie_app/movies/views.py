from django import http
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Genre, Movie, Person


def get_genre_data(genre):
    return {'id': genre.id, 'title': genre.title}


def get_person_data(person):
    return {'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name}


def genre_list(request):
    try:
        genres = Genre.objects.all()
        data = [get_genre_data(genre) for genre in genres]
        return http.JsonResponse(data, safe=False)
    except Exception as e:
        return http.JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return http.JsonResponse({'error': 'Movie not found'}, status=404)

    response_data = {
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'mpa_rating': movie.mpa_rating,
        'imdb_rating': movie.imdb_rating,
        'duration': movie.duration,
        'poster': movie.poster.url if movie.poster else None,
        'bg_picture': movie.bg_picture.url if movie.bg_picture else None,
        'genres': [get_genre_data(genre) for genre in movie.genres.all()],
        'directors': [get_person_data(director) for director in movie.directors.all()],
        'writers': [get_person_data(writer) for writer in movie.writers.all()],
        'stars': [get_person_data(star) for star in movie.stars.all()],
    }

    return http.JsonResponse(response_data)


def movie_list(request):
    try:
        genre_id = request.GET.get('genre')
        src = request.GET.get('src')
        page = request.GET.get('page', 1)

        queryset = Movie.objects.all()

        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        if src:
            queryset = queryset.filter(title__startswith=src)

        paginator = Paginator(queryset, per_page=10)

        try:
            paginated_results = paginator.page(page)
        except PageNotAnInteger:
            paginated_results = paginator.page(1)
        except EmptyPage:
            paginated_results = paginator.page(paginator.num_pages)

        serialized_results = []
        for movie in paginated_results:
            serialized_results.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_year': movie.release_year,
                'mpa_rating': movie.mpa_rating,
                'imdb_rating': movie.imdb_rating,
                'duration': movie.duration,
                'poster': movie.poster.url if movie.poster else None,
                'bg_picture': movie.bg_picture.url if movie.bg_picture else None,
                'genres': [get_genre_data(genre) for genre in movie.genres.all()],
                'directors': [get_person_data(director) for director in movie.directors.all()],
                'writers': [get_person_data(writer) for writer in movie.writers.all()],
                'stars': [get_person_data(star) for star in movie.stars.all()],
            })

        # Construct the response
        response_data = {
            'pages': paginator.num_pages,
            'total': paginator.count,
            'results': serialized_results,
        }

        return http.JsonResponse(response_data)
    except Exception as e:
        return http.JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
