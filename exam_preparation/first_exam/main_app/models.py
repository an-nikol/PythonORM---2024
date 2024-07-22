from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Count


# Task 03.
class DirectorCustomManager(models.Manager):
    def get_directors_by_movies_count(self):
        number_of_movies_per_director = self.annotate(
            directors_count=Count('director_movies')
        )
        return number_of_movies_per_director.order_by('-directors_count', 'full_name')


# Task 01.
class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
        ]
    )

    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    objects = DirectorCustomManager()


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
        ],
    )
    birth_date = models.DateField(
        default='1900-01-01'
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )
    is_awarded = models.BooleanField(
        default=False)

    last_updated = models.DateTimeField(
        auto_now=True
    )


class Movie(models.Model):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5)
        ],
    )

    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(
        choices=GenreChoices.choices,
        max_length=6,
        default='Other'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0), MaxValueValidator(10.0)
        ],
        default=0.0
    )
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='director_movies')
    starring_actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, related_name='starring_movies')
    actors = models.ManyToManyField(Actor, related_name='actor_movies')





