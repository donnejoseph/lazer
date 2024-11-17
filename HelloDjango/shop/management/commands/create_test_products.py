import random
import re
import uuid

from django.core.management.base import BaseCommand
from shop.models import ProductPage, ProductImage
from wagtail.images.models import Image  # Импортируем модель Image из Wagtail
from wagtail.models import Page
from shop.models import CategoryPage

# Функция для транслитерации русского текста в латиницу
def transliterate(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu',
        'я': 'ya', 'ь': "'", 'ъ': "'"
    }

    result = ""
    for char in text:
        if char.lower() in translit_dict:
            # Внимание: если символ в верхнем регистре, преобразуем его в верхний
            result += translit_dict[char.lower()].upper() if char.isupper() else translit_dict[char.lower()]
        else:
            result += char
    return result

class Command(BaseCommand):
    help = 'Create 20 new products with random data and existing images.'

    """
    Категория: Менажницы - 1689
    Категория: Пазлы - 1690
    Категория: Панно - 1691
    Категория: Подставки для телефонов - 1692
    Категория: Упаковка - 1693
    Категория: Рукоделие - 1694

    """

    def handle(self, *args, **kwargs):
        parent_page = Page.objects.get(id=random.choice([1689, 1690, 1691, 1692, 1693, 1694]))  # Получаем случайную страницу категории
        categories = CategoryPage.objects.all()



        all_images = list(Image.objects.all())
        print(all_images)

        if not all_images:
            self.stderr.write("Нет изображений для создания продуктов.")
            return

        for i in range(1, 100):  # Создаем 200 новых продуктов
            # Создаем новый продукт
            product_copy = ProductPage(
                title=random.choice(["менажница", "доска", "поднос", "подставка", "подарочный набор", "подарочная коробка"]),  # Случайное название
                description="Описание тестового товара",  # Пример описания
                price=random.randint(1000, 10000),  # Случайная цена от 100 до 10,000
                is_promotional=random.choice([True, False]),  # Случайный флаг акционного товара
                category = CategoryPage.objects.get(id=random.choice([3293]))  # Получаем случайную категорию
            )

            # Генерация slug на английском (транслитерируем название товара)
            # Генерируем уникальный номер
            unique_id = uuid.uuid4().hex[:6]  # Генерируем 6-символьный уникальный идентификатор
            english_slug = transliterate(
                product_copy.title).lower() + f'-{unique_id}'  # Добавляем уникальный идентификатор
            product_copy.slug = re.sub(r'\W+', '-', english_slug)  # Убираем все специальные символы и пробелы

            # Добавляем продукт в родительскую страницу
            if parent_page:
                product_copy = parent_page.add_child(instance=product_copy)  # Добавляем как дочерний элемент

            product_copy.save()  # Сохраняем новый продукт

            # Выбираем случайное изображение для нового товара
            selected_image = random.choice(all_images)  # Выбираем случайное изображение

            # Создаем связь с новым товаром
            product_image = ProductImage(
                product=product_copy,
                image=selected_image.file,  # Важно: используем `selected_image.file`, а не сам объект Image
                is_main=True  # Устанавливаем его основным изображением
            )

            product_image.save()  # Сохраняем изображение для товара

            self.stdout.write(f'Создан товар: {product_copy.title} с slug: {product_copy.slug}')
            print(f'Категория: {product_copy.category}')  # Выводим информацию о созданном товаре

        self.stdout.write(self.style.SUCCESS("200 новых тестовых товаров успешно созданы."))
