import os
import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct, ProductManager

# Task 02.


def product_quantity_ordered():
    total_products_ordered = (Product.objects
                              .annotate(total_ordered_quantity=
                                        Sum('orderproduct__quantity'))
                              .exclude(total_ordered_quantity=None)
                              .order_by('-total_ordered_quantity'))

    result = []
    for p in total_products_ordered:
        result.append(f'Quantity ordered of {p.name}: {p.total_ordered_quantity}')

    return '\n'.join(result)

# Task 03.


def ordered_products_per_customer():
    orders = Order.objects.prefetch_related(
        'orderproduct_set__product__category').order_by('id')

    result = []
    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for ordered_product in order.orderproduct_set.all():
            result.append(f'- Product: {ordered_product.product.name}, Category: {ordered_product.product.category.name}')

    return '\n'.join(result)


# Task 04.
def filter_products():
    all_available_products = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).order_by('-price', 'name')
    result = []

    for p in all_available_products:
        result.append(f"{p.name}: {p.price}lv.")

    return '\n'.join(result)


# Task 05.
def give_discount():
    all_available_products_with_price = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00))
    discounted_products = all_available_products_with_price.update(price=F('price') * 0.70)

    result = []

    for p in Product.objects.filter(is_available=True).order_by('-price', 'name'):
        result.append(f"{p.name}: {p.price}lv.")


    return '\n'.join(result)

