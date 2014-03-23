from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

from .views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', PortailUserListView.as_view(), name="portailuser_list"),

    url(r'^creances$', CreanceListView.as_view(), name="creance_list"),
    #url(r'^creances/(?P<pk>\d+)$', CreanceDetailView.as_view(), name="creance_detail"),
    url(r'^creances/ajouter$', CreanceCreateView.as_view(), name="creance_create"),
    url(r'^creances/ok/(?P<pk>\d+)$', CreanceValidateView.as_view(valide=True), name="creance_ok"),
    url(r'^creances/ko/(?P<pk>\d+)$', CreanceValidateView.as_view(valide=False), name="creance_ko"),

    url(r'^dettes$', DetteListView.as_view(), name="dette_list"),
    #url(r'^dettes/(?P<pk>\d+)$', DetteDetailView.as_view(), name="dette_detail"),
    url(r'^dettes/ajouter$', DetteCreateView.as_view(), name="dette_create"),
    url(r'^dettes/ajouter/(?P<creance>\d+)$', DetteCreateFromCreanceView.as_view(), name="dette_create_from_creance"),
    url(r'^dettes/ok/(?P<pk>\d+)$', DetteValidateView.as_view(valide=True), name="dette_ok"),
    url(r'^dettes/ko/(?P<pk>\d+)$', DetteValidateView.as_view(valide=False), name="dette_ko"),

    url(r'^remboursements$', RemboursementListView.as_view(), name="remboursement_list"),
    #url(r'^remboursements/(?P<pk>\d+)$', RemboursementDetailView.as_view(), name="remboursement_detail"),
    url(r'^remboursements/ajouter$', RemboursementCreateView.as_view(), name="remboursement_create"),
    url(r'^remboursements/ok/(?P<pk>\d+)$', RemboursementValidateView.as_view(valide=True), name="remboursement_ok"),
    url(r'^remboursements/ko/(?P<pk>\d+)$', RemboursementValidateView.as_view(valide=False), name="remboursement_ko"),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
