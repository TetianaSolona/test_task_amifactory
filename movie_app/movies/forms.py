from django import forms
from .models import Genre, Person, Movie


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['title']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'types']


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'poster', 'bg_picture', 'release_year', 'mpa_rating', 'imdb_rating',
                  'duration', 'genres', 'directors', 'writers', 'stars']
        widgets = {
            'genres': forms.CheckboxSelectMultiple,
            'directors': forms.CheckboxSelectMultiple,
            'writers': forms.CheckboxSelectMultiple,
            'stars': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
