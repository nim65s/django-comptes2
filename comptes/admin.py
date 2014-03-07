#-*- coding: utf-8 -*-

from django.contrib.admin import site

from .models import *

site.register(PortailUser)
site.register(Creance)
site.register(Dette)
site.register(Remboursement)
