from django.core.management.base import BaseCommand
from shop.models import ProductPage
from django.db import transaction
from time import sleep


class Command(BaseCommand):
    help = 'Удалить все товары из базы данных'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начало удаления товаров из базы данных...")

        batch_size = 100  # Количество объектов для обработки за раз
        products = ProductPage.objects.all()

        while products.exists():
            to_delete = list(products[:batch_size])  # Convert to list to avoid slicing issues
            with transaction.atomic():
                for product in to_delete:
                    product.delete()  # Call delete() individually to maintain tree integrity

            self.stdout.write(f"Удалено {len(to_delete)} товаров...")
            sleep(0.1)  # Optional pause to reduce load

        self.stdout.write("Удаление всех товаров завершено!")
