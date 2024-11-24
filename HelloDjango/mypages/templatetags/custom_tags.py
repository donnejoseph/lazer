import logging
from django import template
from django.core.mail import send_mail
from mypages.models import StocksFormSubmission
from django.http import HttpResponseRedirect


logger = logging.getLogger(__name__)
register = template.Library()

@register.inclusion_tag('mypages/partial/stocks_form.html', takes_context=True)
def render_stocks_form(context):
    """
    Рендерит только форму, без лишних вызовов.
    """
    request = context.get('request')
    if not request:
        logger.error("Request object is missing in the context")
        return {'submitted': False}

    if request.method == 'POST' and 'stocks_form' in request.POST:
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        agreement = request.POST.get('agreement', '') == 'on'

        if name and phone and agreement:
            StocksFormSubmission.objects.create(name=name, phone=phone, agreement=agreement)
            try:
                send_mail(
                    'Новая заявка с сайта',
                    f"Имя: {name}\nТелефон: {phone}",
                    'platforma@dvkgroupp.ru',
                    ['dinar784@gmail.com'],
                    fail_silently=False,
                )
                logger.info("Email sent successfully")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
            return HttpResponseRedirect('/thank-you/')

        logger.warning("Form validation failed")
    return {'submitted': False}



@register.filter
def multiply(value, arg):
    """Умножает значение на аргумент."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
