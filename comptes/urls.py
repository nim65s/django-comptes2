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
    url(r'^creances/valider/(?P<pk>\d+)$', CreanceValidateView.as_view(), name="creance_validate"),

    url(r'^dettes$', DetteListView.as_view(), name="dette_list"),
    #url(r'^dettes/(?P<pk>\d+)$', DetteDetailView.as_view(), name="dette_detail"),
    url(r'^dettes/ajouter$', DetteCreateView.as_view(), name="dette_create"),
    url(r'^dettes/ajouter/(?P<creance>\d+)$', DetteCreateFromCreanceView.as_view(), name="dette_create_from_creance"),
    url(r'^dettes/valider/(?P<pk>\d+)$', DetteValidateView.as_view(), name="dette_validate"),

    url(r'^remboursements$', RemboursementListView.as_view(), name="remboursement_list"),
    #url(r'^remboursements/(?P<pk>\d+)$', RemboursementDetailView.as_view(), name="remboursement_detail"),
    url(r'^remboursements/ajouter$', RemboursementCreateView.as_view(), name="remboursement_create"),
    url(r'^remboursements/valider/(?P<pk>\d+)$', RemboursementValidateView.as_view(), name="remboursement_validate"),
)
