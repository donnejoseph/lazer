from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class CategoryPage(Page):
    description = RichTextField(blank=True, verbose_name="Описание категории")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Изображение категории"
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('image'),
    ]

    subpage_types = ['shop.ProductPage']

    def get_context(self, request):
        context = super().get_context(request)
        if self.pk:
            # Гарантируем, что передаются Page объекты (для тегов Wagtail)
            context['products'] = self.get_children().live().specific()[:50]
        else:
            context['products'] = []
        # Пример дополнительного контекста для других разделов
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        return context

    def get_template(self, request, *args, **kwargs):
        return 'mypages/category_page.html'  # Указываем правильный путь к файлу

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductPage(Page):
    category = models.ForeignKey(
        'shop.CategoryPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name="Категория"
    )
    description = RichTextField(blank=True, verbose_name="Описание товара")
    specifications = RichTextField(blank=True, verbose_name="Характеристики товара")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_promotional = models.BooleanField(default=False, verbose_name="Акционный товар")

    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('description'),
        FieldPanel('specifications'),
        FieldPanel('price'),
        FieldPanel('is_promotional'),
        InlinePanel('images', label="Изображения товара"),
    ]

    parent_page_types = ['shop.CategoryPage']

    def get_template(self, request, *args, **kwargs):
        return 'mypages/product_page.html'  # Указываем правильный путь к файлу

    def get_context(self, request):
        context = super().get_context(request)
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        return context

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = ParentalKey(ProductPage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение товара")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")

    panels = [
        FieldPanel('image'),
        FieldPanel('is_main'),
    ]

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"
