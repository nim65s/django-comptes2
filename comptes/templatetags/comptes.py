#-*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter
def peut_valider(user, truc):
    return truc.validable(user)
