from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


# Task 06.
class ReviewMixin(models.Model):
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), ])

    class Meta:
        abstract = True
        ordering = ['-rating']



# Task 01.
class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, message='Name must be at least 2 characters long.'),
                    MaxLengthValidator(100, message='Name cannot exceed 100 characters.')],
    )
    location = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, message='Location must be at least 2 characters long.'),
                    MaxLengthValidator(200, message='Location cannot exceed 200 characters.')],
    )
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.00, message='Rating must be at least 0.00.'),
                    MaxValueValidator(5.00, message='Rating cannot exceed 5.00.')
                    ],
    )


# Task 02.

def validate_menu_categories(value):
    categories = ('Appetizers', 'Main Course', 'Desserts')

    for cat in categories:
        if cat.lower() not in value.lower():
            raise ValidationError(
                'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')


class Menu(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        validators=[validate_menu_categories]
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


# Task 03.

class RestaurantReview(ReviewMixin):
    reviewer_name = models.CharField(
        max_length=100,
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    # review_content = models.TextField()
    # rating = models.PositiveIntegerField(
    #     validators=[MaxValueValidator(5),]
    # )

    class Meta(ReviewMixin.Meta):
        abstract = True
        # ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant', ]


# Task 04.
class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(
        max_length=100,
    )

    class Meta(RestaurantReview.Meta):
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'


# Task 05.

class MenuReview(ReviewMixin):
    reviewer_name = models.CharField(
        max_length=100,
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    # review_content = models.TextField()
    # rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),])
    class Meta(ReviewMixin.Meta):
        # ordering = ['-rating']
        verbose_name = "Menu Review"
        verbose_name_plural = "Menu Reviews"
        unique_together = ['reviewer_name', 'menu']
        indexes = [models.Index(
            fields=["menu"],
            name=
            "main_app_menu_review_menu_id")]
