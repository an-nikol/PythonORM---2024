import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Order, Product
from django.db.models import Q, Count, F


# Task 04.
def get_profiles(search_string=None):
    if search_string is None:
        return ''

    result = []
    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string)

    profiles = Profile.objects \
        .annotate(num_orders=Count('orders')) \
        .filter(query) \
        .order_by('full_name')

    if not profiles:
        return ''

    for p in profiles:
        result.append(f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, '
                      f'orders: {p.num_orders}')

    return '\n'.join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    result = []

    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, orders: {p.num_of_orders}"
        )

    return '\n'.join(result)


def get_last_sold_products():
    latest_order = Order.objects.last()

    if not latest_order or not latest_order.products:
        return ''

    products = latest_order.products.order_by('name').values_list('name', flat=True)

    result = ', '.join(products)
    return f"Last sold products: {result}"


# Task 05.

def get_top_products():
    top_products = (Product.objects.annotate(
            num_of_orders=Count('orders'))
            .filter(num_of_orders__gt=0)
            .order_by('-num_of_orders', 'name'))[:5]

    if not top_products or not top_products[0].num_of_orders:
        return ''

    result = ['Top products:']

    for p in top_products:
        result.append(f'{p.name}, sold {p.num_of_orders} times')

    return '\n'.join(result)


def apply_discounts():
    discounted_orders = Order.objects.annotate(
        num_of_products=Count('products')) \
        .filter(num_of_products__gt=2, is_completed=False) \
        .update(total_price=F('total_price') * 0.90)


    return f"Discount applied to {discounted_orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ''

    order.is_completed = True
    order.save()

    for p in order.products.all():
        p.in_stock -= 1

        if p.in_stock == 0:
            p.is_available = False
        p.save()
    return 'Order has been completed!'


