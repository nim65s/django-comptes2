#-*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag
def valider(user, truc):
    if truc.validable(user):
        url_ok, url_ko = truc.get_validate_urls()
        try:
            valide = truc.valide
        except AttributeError:  # truc est un Remboursement
            if truc.crediteur.user == user:
                valide = truc.valide_crediteur
            else:
                valide = truc.valide_credite
        lien = ""
        if valide is None or not valide:
            lien += u'<a href="%s">Valider</a>' % url_ok
        if valide is None or valide:
            lien += u'<a href="%s">Invalider</a> ' % url_ko
        return lien
    else:
        return ''
