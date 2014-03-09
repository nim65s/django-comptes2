#-*- coding: utf-8 -*-

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, View
from django.views.generic.detail import SingleObjectMixin

from .models import *


class IsPortailUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        return PortailUser.objects.filter(user=user).count() == 1


class PortailUserListView(IsPortailUserMixin, ListView):
    model = PortailUser


class ValidateView(IsPortailUserMixin, SingleObjectMixin, View):
    valide = None

    def get(self, request, *args, **kwargs):
        o = self.get_object()
        self.validate(o)
        o.save()
        return redirect(o.get_absolute_url())


class CreanceListView(IsPortailUserMixin, ListView):
    model = Creance

    def get_queryset(self, **kwargs):
        return Creance.objects.filter(Q(creancier__user=self.request.user) | Q(dette__debiteur__user=self.request.user)).distinct()


class CreanceCreateView(IsPortailUserMixin, CreateView):
    model = Creance
    fields = ["creancier", "montant", "description", "moment"]

    def form_valid(self, form):
        if form.instance.creancier == self.request.user:
            form.instance.valide = True
        return super(CreanceCreateView, self).form_valid(form)


class CreanceValidateView(ValidateView):
    model = Creance

    def validate(self, o):
        if o.creancier.user == self.request.user:
            o.valide = self.valide


class DetteListView(IsPortailUserMixin, ListView):
    model = Dette


class DetteCreateView(IsPortailUserMixin, CreateView):
    model = Dette
    fields = ["creance", "debiteur", "parts"]

    def form_valid(self, form):
        if form.instance.debiteur == self.request.user:
            form.instance.valide = True
        return super(DetteCreateView, self).form_valid(form)


class DetteCreateFromCreanceView(DetteCreateView):
    def get_initial(self):
        init = super(DetteCreateFromCreanceView, self).get_initial()
        init['creance'] = get_object_or_404(Creance, pk=int(self.kwargs['creance']))
        return init


class DetteValidateView(ValidateView):
    model = Dette

    def validate(self, o):
        if o.debiteur.user == self.request.user:
            o.valide = self.valide


class RemboursementListView(IsPortailUserMixin, ListView):
    model = Remboursement


class RemboursementCreateView(IsPortailUserMixin, CreateView):
    model = Remboursement
    fields = ["crediteur", "credite", "montant", "moment"]

    def form_valid(self, form):
        if form.instance.credite == self.request.user:
            form.instance.valide_credite = True
        if form.instance.crediteur == self.request.user:
            form.instance.valide_crediteur = True
        return super(RemboursementCreateView, self).form_valid(form)


class RemboursementValidateView(ValidateView):
    model = Remboursement

    def validate(self, o):
        if o.crediteur.user == self.request.user:
            o.valide_crediteur = self.valide
        if o.credite.user == self.request.user:
            o.valide_credite = self.valide
