from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models

# Task 03.

class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        return self.annotate(mission_count=models.Count('missions')).order_by('-mission_count', 'phone_number')


class Astronaut(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    phone_number = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex=r'^\d+$')])
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(blank=True, null=True)
    spacewalks = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)
    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    class MissionChoices(models.TextChoices):
        Planned = 'Planned', 'Planned'
        Ongoing = 'Ongoing', 'Ongoing'
        Completed = 'Completed', 'Completed'

    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=MissionChoices.choices, default=MissionChoices.Planned)
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='used_in_missions')
    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, null=True,
                                  related_name='commanded_missions')
