from django import http
from django.views import View
from django.core.paginator import Paginator

from .forms import MovieForm
from .models import Genre, Movie, Person


class GenreView(View):
    def get(self, request, *args, **kwargs):
        try:
            genres = Genre.objects.all()
            data = [genre.get_json_data() for genre in genres]
            return http.JsonResponse(data, safe=False)
        except Exception as e:
            return http.JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


class MovieDetailView(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                return http.JsonResponse({'error': 'Movie not found'}, status=404)

            response_data = movie.get_json_data()
            return http.JsonResponse(response_data)
        except Exception as e:
            return http.JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


class MovieListView(View):
    def get(self, request, *args, **kwargs):
        try:
            form = MovieForm(request.GET)
            if not form.is_valid():
                errors = form.errors.as_json()
                return http.JsonResponse({'error': f'Invalid parameters: {errors}'}, status=400)

            genre_id = form.cleaned_data.get('genre_id')
            src = form.cleaned_data.get('src')
            page = form.cleaned_data.get('page', 1)

            queryset = Movie.objects.all()

            if genre_id:
                try:
                    genre_id = int(genre_id)
                    queryset = queryset.filter(genres__id=genre_id)
                except ValueError:
                    return http.JsonResponse({'error': 'Invalid genre_id parameter'}, status=400)
            if src:
                if not isinstance(src, str) or len(src.strip()) == 0:
                    return http.JsonResponse({'error': 'Invalid src parameter'}, status=400)

                queryset = queryset.filter(title__startswith=src)

            paginator = Paginator(queryset, per_page=10)

            paginated_results = paginator.page(page)

            serialized_results = [movie.get_json_data() for movie in paginated_results]

            response_data = {
                'pages': paginator.num_pages,
                'total': paginator.count,
                'results': serialized_results,
            }

            return http.JsonResponse(response_data)
        except Exception as e:
            return http.JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
