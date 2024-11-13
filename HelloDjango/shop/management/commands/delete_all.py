from django.core.management.base import BaseCommand
from shop.models import ProductPage

class Command(BaseCommand):
    help = 'Удалить все товары из базы данных'

    def handle(self, *args, **kwargs):
        # Получаем все товары (ProductPage) из базы данных
        products = ProductPage.objects.all()

        # Если товары есть, удаляем их
        products.delete()
