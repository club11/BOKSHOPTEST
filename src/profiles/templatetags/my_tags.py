from atexit import register
from django import template
register = template.Library()
import requests

USD_ENDPOINT = 'https://www.nbrb.by/api/exrates/rates/431'

@register.simple_tag
def currency_rate():                    #{% currency_rate, obj1, obj2 %}
    res = requests.get(USD_ENDPOINT, verify=False)                                                  ##### ВРЕМЕННАЯ ЗАТЫЧКА  verify=False, ибо ошибка сертификата появилась
    return res.json().get('Cur_OfficialRate')

