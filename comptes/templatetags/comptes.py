#-*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag
def valider(user, truc):
    if truc.validable(user):
        return u'<a href="%s">Oui</a> <a href="%s">Non</a>' % truc.get_validate_urls()
    else:
        return ''
