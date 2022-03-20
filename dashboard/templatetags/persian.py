from django import template
from khayyam import JalaliDate, JalaliDatetime

register = template.Library()


@register.filter
def convert_date_persian(date):
    return JalaliDatetime(date).strftime('%Y-%m-%d %H:%m')
