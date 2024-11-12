import os
from django.core.wsgi import get_wsgi_application

# Устанавливаем переменную окружения для настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloDjango.settings')

# Получаем WSGI-приложение
application = get_wsgi_application()
