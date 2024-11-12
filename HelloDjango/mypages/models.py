# mypages/models.py
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    intro = RichTextField(blank=True)  # Поле для текста на главной странице

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "Главная страница"  # Отображаемое имя в админке

class AboutPage(Page):
    intro = RichTextField(blank=True)  # Поле для ввода текста

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
