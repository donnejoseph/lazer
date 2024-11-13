import random
from django.core.management.base import BaseCommand
from shop.models import ProductPage, ProductImage
from wagtail.images.models import Image  # Импортируем модель Image из Wagtail
from wagtail.models import Page

from shop.models import CategoryPage


class Command(BaseCommand):
    help = 'Create 20 new products with random data and existing images.'

    def handle(self, *args, **kwargs):
        parent_page = Page.objects.get(id=5)  # Получаем страницу "Каталог"

        all_images = list(Image.objects.all())
        print(all_images)

        if not all_images:
            self.stderr.write("Нет изображений для создания продуктов.")
            return

        for i in range(1, 20):  # Создаем 20 новых продуктов
            # Создаем новый продукт
            product_copy = ProductPage(
                title=random.choice(["менажница", "доска", "поднос", "подставка", "подарочный набор", "подарочная коробка"]),  # Случайное название
                description="Описание тестового товара",  # Пример описания
                price=random.randint(100, 10000),  # Случайная цена от 100 до 10,000
                is_promotional=random.choice([True, False]),  # Случайный флаг акционного товара
                category= random.choice([CategoryPage.objects.first()])
            )

            if parent_page:
                product_copy = parent_page.add_child(instance=product_copy)  # Добавляем как дочерний элемент

            product_copy.save()  # Сохраняем новый продукт

            # Выбираем случайное изображение для нового товара
            selected_image = random.choice(all_images)  # Выбираем случайное изображение

            # Создаем связь с новым товаром
            # Мы должны создать экземпляр ProductImage, передав путь к файлу изображения
            product_image = ProductImage(
                product=product_copy,
                image=selected_image.file,  # Важно: используем `selected_image.file`, а не сам объект Image
                is_main=True           # Устанавливаем его основным изображением
            )

            product_image.save()  # Сохраняем изображение для товара

            self.stdout.write(f'Создан товар: {product_copy.title}')
            print(product_copy.category)
            print(parent_page)# Выводим информацию о созданном товаре

        self.stdout.write(self.style.SUCCESS("20 новых тестовых товаров успешно созданы."))
