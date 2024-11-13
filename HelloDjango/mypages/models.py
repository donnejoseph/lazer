# mypages/models.py
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from shop.models import ProductPage


class HomePage(Page):
    intro = RichTextField(blank=True)  # Поле для текста на главной странице

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Получаем товары, которые являются хитами продаж (is_promotional=True)
        context['best_sellers'] = ProductPage.objects.filter(is_promotional=True)[:6]
        return context

class AboutPage(Page):
    intro = RichTextField(blank=True)  # Поле для ввода текста

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
