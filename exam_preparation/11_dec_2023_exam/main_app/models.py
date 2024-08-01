from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count


# Task 03.
class CustomModelManagerTennisPlayer(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return TennisPlayer.objects.annotate(
            wins_count=Count('matches__winner')
        ).order_by('-wins_count', 'full_name')


# Task 01.
class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(5)
        ])
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ])
    ranking = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)]
    )
    is_active = models.BooleanField(default=True)
    objects = CustomModelManagerTennisPlayer()

class Tournament(models.Model):
    class SufaceTypeChoices(models.TextChoices):
        not_selected = 'Not Selected', 'Not Selected'
        clay = 'Clay', 'Clay'
        grass = 'Grass', 'Grass'
        hard_court = 'Hard Court', 'Hard Court'

    name = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(2)],
        unique=True)
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)
                    ])
    prize_money = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    surface_type = models.CharField(max_length=12, choices=SufaceTypeChoices.choices,
                                    default=SufaceTypeChoices.not_selected)


class Match(models.Model):
    score = models.CharField(max_length=100)
    summary = models.TextField(validators=[MinLengthValidator(5)])
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    players = models.ManyToManyField(TennisPlayer)
    winner = models.ForeignKey(TennisPlayer, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')

    class Meta:
        verbose_name_plural = "Matches"
