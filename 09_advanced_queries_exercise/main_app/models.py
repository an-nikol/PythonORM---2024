from datetime import timedelta
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count, QuerySet, Max, Min, Avg, Q, F


# Create your models here.

# Task 01.
class RealEstateListingManager(models.Manager): # IN CUSTOM MANAGER DO NOT USE OBJECT
    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self) -> QuerySet:
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]


class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    objects = RealEstateListingManager()

# Task 02.

class VideoGameManager(models.Manager):

    def games_by_genre(self, genre: str) -> QuerySet:
        return self.filter(genre=genre)

    def recently_released_games(self, year: int) -> QuerySet:
        return self.filter(release_year__gte=year)

    def highest_rated_game(self) -> QuerySet:
        # max_rating = self.aggregate(max_rating=Max('rating'))['max_rating']  # {max_rating: 6} => 6
        # game_with_max_rating = self.filter(rating=max_rating)

        return self.annotate(max_rating=Max('rating')).order_by('-max_rating').first()

    def lowest_rated_game(self) -> QuerySet:
        # min_rating = self.aggregate(min_rating=Min('rating'))['min_rating']  # {max_rating: 6} => 6
        # game_with_min_rating = self.filter(rating=min_rating)

        return self.annotate(min_rating=Min('rating')).order_by('min_rating').first()

    def average_rating(self) -> str:
        avg_rating = self.aggregate(avg_rating=Avg('rating'))['avg_rating']  # {avg_rating: 5.545454}
        return f"{avg_rating:.1f}"

class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1990, message='The release year must be between 1990 and 2023'),
            MaxValueValidator(2023, message='The release year must be between 1990 and 2023')
        ]
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0, message='The rating must be between 0.0 and 10.0'),
            MaxValueValidator(10.0, message='The rating must be between 0.0 and 10.0'),
        ],
    )
    objects = VideoGameManager()

    def __str__(self):
        return self.title


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)
    # Task 03.

    @classmethod
    def get_invoices_with_prefix(cls, prefix: str):
         return cls.objects.filter(invoice_number__startswith=prefix)


    @classmethod
    def get_invoices_sorted_by_number(cls):
        return cls.objects.order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number: str):
        return cls.objects.select_related('billing_info').get(invoice_number=invoice_number)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

# Task 04.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')  # junction table project_technology

    def get_programmers_with_technologies(self):
        return self.programmers.prefetch_related('projects__technologies_used')



class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers') # junction table project_programmers

    def get_projects_with_technologies(self):
        return self.projects.prefetch_related('technologies_used')


# Task 05.
class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()

    @classmethod
    def ongoing_high_priority_tasks(cls):
        return cls.objects.filter(priority='High', is_completed=False, completion_date__gt=F('creation_date'))

    @classmethod
    def completed_mid_priority_tasks(cls):
        return cls.objects.filter(priority='Medium', is_completed=True)

    @classmethod
    def search_tasks(cls, query: str):
        return cls.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    @classmethod
    def recent_completed_tasks(cls, days: int):
        return cls.objects.filter(is_completed=True, completion_date__gte=F('creation_date') - timedelta(days=days))

# Task 06.

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @classmethod
    def get_long_and_hard_exercises(cls):
        return cls.objects.filter(duration_minutes__gt=30, difficulty_level__gte=10)

    @classmethod
    def get_short_and_easy_exercises(cls) :
        return cls.objects.filter(duration_minutes__lt=15, difficulty_level__lt=5)

    @classmethod
    def get_exercises_within_duration(cls, min_duration: int, max_duration: int):
        return cls.objects.filter(duration_minutes__gte=min_duration, duration_minutes__lte=max_duration)

    @classmethod
    def get_exercises_with_difficulty_and_repetitions(cls, min_difficulty: int, min_repetitions: int):
        return cls.objects.filter(difficulty_level__gte=min_difficulty, repetitions__gte=min_repetitions)