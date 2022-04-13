from django import template
register = template.Library()
from .. import models
from django.contrib.contenttypes.models import ContentType


@register.inclusion_tag('comments/tags/show_comments.html', takes_context=True)
def show_comments(context):
    obj = context.get('object')     #объект для всех DetailView
    content_type = ContentType.objects.get_for_model(obj)
    content_type_id = content_type.pk
    next_step = context.get('request').path     #замудрено для возврата на ткомменченую страницу
    comments = models.Comment.objects.filter(content_type=content_type, object_id=obj.pk)  #универсальный пакетный способ по получению объекта из Contenttype для работы со всеми приложениями
    return {'comments' : comments, 'next_step' : next_step, 'content_type_id' : content_type_id, 'object_id' : obj.pk}