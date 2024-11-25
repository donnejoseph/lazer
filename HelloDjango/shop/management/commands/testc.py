from django.core.management.base import BaseCommand
from mypages.models import Review



class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        reviews = Review.objects.all()
        for review in reviews:
            print(review.name,  review.rating)