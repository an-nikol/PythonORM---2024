import os
import django
from django.db.models import Count, Max, Avg, F

from main_app.models import Director, Actor, Movie

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    directors = None

    if (search_name is not None) and (search_nationality is not None):
        directors = Director.objects.filter(full_name__icontains=search_name,
                                            nationality__icontains=search_nationality).order_by('full_name')
    elif search_name is not None:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')
    elif search_nationality is not None:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')

    if not directors:
        return ''

    result = []
    for d in directors:
        result.append(f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}')

    return '\n'.join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.directors_count}."


def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies') \
        .annotate(
        num_of_movies=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')) \
        .order_by('-num_of_movies', 'full_name') \
        .first()

    # no actors or no movies
    if not actor or not actor.num_of_movies:
        return ""

    movies = ", ".join(movie.title for movie in actor.starring_movies.all() if movie)

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, " \
           f"movies average rating: {actor.movies_avg_rating:.1f}"


# Task 05.
def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('actor_movies')) \
                 .order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)

def get_top_rated_awarded_movie():
    top_movie = Movie.objects \
        .filter(is_awarded=True) \
        .order_by('-rating', 'title') \
        .first()

    if not top_movie: # is None
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"

    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ", ".join(participating_actors)

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. " \
           f"Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    updated_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not updated_movies:
        return "No ratings increased."

    num_of_updated_movies = updated_movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {num_of_updated_movies} movies."