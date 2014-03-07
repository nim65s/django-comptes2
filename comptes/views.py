#-*- coding: utf-8 -*-

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import *


class IsPortailUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self, user):
        return PortailUser.objects.filter(user=user).count() == 1


class PortailUserListView(IsPortailUserMixin, ListView):
    model = PortailUser


#class CreanceDetailView(IsPortailUserMixin, DetailView):
    #model = Creance


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


class CreanceValidateView(IsPortailUserMixin, UpdateView):
    model = Creance
    fields = ["valide"]

    def form_valid(self, form):
        if form.instance.creancier != self.request.user:
            raise SuspiciousOperation("Quelqu’un essaye de valide une créance qui n’est pas à lui")
        return super(CreanceValidateView, self).form_valid(form)


#class DetteDetailView(IsPortailUserMixin, DetailView):
    #model = Dette


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


class DetteValidateView(IsPortailUserMixin, UpdateView):
    model = Dette
    fields = ["valide"]

    def form_valid(self, form):
        if form.instance.debiteur != self.request.user:
            raise SuspiciousOperation("Quelqu’un essaye de valide une dette qui n’est pas à lui")
        return super(DetteValidateView, self).form_valid(form)


#class RemboursementDetailView(IsPortailUserMixin, DetailView):
    #model = Remboursement


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


class RemboursementValidateView(IsPortailUserMixin, DetailView):
    model = Remboursement

    def get(self, request, *args, **kwargs):
        o = self.get_object()
        if o.crediteur.user == request.user:
            o.valide_crediteur = True
            o.save()
        if o.credite.user == request.user:
            o.valide_credite = True
            o.save()
        return redirect(reverse('remboursement_list'))
