import os
import django
from django.db.models import Count, Avg, Sum

from main_app.models import Author, Article

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here

# Task 04.
def get_authors(search_name=None, search_email=None):
    query = None

    if (search_name is None) and (search_email is None):
        return ''

    if search_name and search_email:
        query = Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email).order_by(
            '-full_name')
    else:
        if search_name:
            query = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')
        elif search_email:
            query = Author.objects.filter(email__icontains=search_email).order_by('-full_name')

    result = []
    for author in query:
        result.append(
            f'Author: {author.full_name}, email: {author.email}, status: {"Banned" if author.is_banned else "Not Banned"}')

    return '\n'.join(result)


def get_top_publisher():
    top_publisher = Author.objects.get_authors_by_article_count().first()

    if top_publisher is None or top_publisher.articles_count == 0:
        return ''

    return f"Top Author: {top_publisher.full_name} with {top_publisher.articles_count} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(count_of_reviews=Count('reviews')).order_by('-count_of_reviews',
                                                                                       'email').first()

    if top_reviewer is None or top_reviewer.count_of_reviews == 0:
        return ''

    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.count_of_reviews} published reviews.'


# Task 05.

def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if latest_article is None:
        return ""

    authors_names = ', '.join(author.full_name for author in latest_article.authors.all().order_by('full_name'))
    num_reviews = latest_article.reviews.count()
    avg_rating = sum([r.rating for r in latest_article.reviews.all()]) / num_reviews if num_reviews else 0.0

    return f"The latest article is: {latest_article.title}. Authors: {authors_names}. Reviewed: {num_reviews} times." \
           f" Average Rating: {avg_rating:.2f}."



def get_top_rated_article():
    top_rated_article = Article.objects.annotate(count_of_reviews=Count('reviews'), # num_reviews = top_rated_article.reviews.count() if top_rated_article else 0
                                                 avg_rating=Avg('reviews__rating')).order_by('-avg_rating', 'title').first()
    if not top_rated_article or top_rated_article.count_of_reviews == 0:
        return ''

    return (f"The top-rated article is: {top_rated_article.title}, with an average rating of {top_rated_article.avg_rating:.2f},"
            f" reviewed {top_rated_article.count_of_reviews} times.")


def ban_author(email=None):
    author = Author.objects.prefetch_related('reviews').filter(email__exact=email).first()
    if email is None or author is None:
        return "No authors banned."

    num_reviews_deleted = author.reviews.count()

    author.is_banned = True
    author.save()
    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted."
