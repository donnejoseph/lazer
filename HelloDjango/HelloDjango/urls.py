from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mypages import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('cms/', include('wagtail.admin.urls')),  # Админка Wagtail

    # Пользовательские маршруты для корзины
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),

    # Корневой путь Wagtail (обрабатывает остальные маршруты)
    path('', include('wagtail.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
