from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),       # Админка Django
    path('cms/', include('wagtail.admin.urls')),  # Админка Wagtail
    path('', include('wagtail.urls')),     # Корневой путь Wagtail
]
