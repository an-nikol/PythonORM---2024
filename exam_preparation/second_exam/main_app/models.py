from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db.models import Count


# Task 03.

class ProfileCustomManager(models.Manager):
    def get_regular_customers(self):
        profiles = Profile.objects.annotate(
            num_of_orders=Count('orders')) \
            .filter(num_of_orders__gt=2) \
            .order_by('-num_of_orders')

        return profiles


# Task 01.
class Profile(models.Model):
    full_name = models.CharField(max_length=100,
                                 validators=[MinLengthValidator(2), ])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = ProfileCustomManager()

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      validators=[MinValueValidator(0.01)])
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

