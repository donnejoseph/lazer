from django.utils.text import slugify as django_slugify
from unidecode import unidecode

def custom_slugify(value):
    return django_slugify(unidecode(value))
