import random
import re

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

    def handle(self, *args, **kwargs):
        pages = Page.objects.all()  # Получаем все страницы
        for page in pages:
            # Получаем русскоязычное название страницы
            russian_name = page.title
            print(f"Original page: {russian_name} (ID: {page.id}, URL: {page.url_path})")

            # Получаем английский аналог с помощью транслитерации
            english_name = transliterate(russian_name)

            # Преобразуем имя для URL (убираем пробелы, специальные символы, делаем в нижнем регистре)
            english_name = re.sub(r'\W+', '-', english_name).lower()

            # Пример создания нового URL для страницы (можно дополнительно обработать URL, если нужно)
            new_url = f'/{english_name}/'

            # Обновляем URL страницы
            # Здесь предполагается, что у вас есть логика для изменения URL
            # В зависимости от вашей структуры данных, возможно, придется обновить поле или обработать путь
            page.url_path = new_url  # Обновляем url_path страницы
            page.save()  # Сохраняем изменения

            print(f"Updated page: {russian_name} -> {english_name} (New URL: {new_url})")



