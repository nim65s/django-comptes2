#-*- coding: utf-8 -*-

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import BooleanField, DateTimeField, DecimalField, ForeignKey, IntegerField, Model, Sum, TextField
from django.utils.html import mark_safe


class PortailUser(Model):
    user = ForeignKey(User, unique=True)
    solde = DecimalField(max_digits=8, decimal_places=2, default=0)

    def maj_solde(self):
        dettes = sum([dette.valeur() for dette in self.dette_set.filter(creance__checked=True)])
        debits = self.debits.filter(valide_crediteur=True, valide_credite=True).aggregate(s=Sum('montant'))['s']
        credits = self.credits.filter(valide_crediteur=True, valide_credite=True).aggregate(s=Sum('montant'))['s']
        creances = self.creance_set.filter(checked=True).aggregate(s=Sum('montant'))['s']
        somme = 0
        if dettes:
            somme -= dettes
        if creances:
            somme += creances
        if debits:
            somme += debits
        if credits:
            somme -= credits
        self.solde = somme
        self.save()

    def __unicode__(self):
        return u"%s" % self.user

    class Meta:
        ordering = ["-solde"]


class Creance(Model):
    creancier = ForeignKey(PortailUser, verbose_name=u"Créancier")
    montant = DecimalField(max_digits=8, decimal_places=2)
    description = TextField()
    moment = DateTimeField()
    valide = BooleanField(default=False)  # Validée par le créancier
    checked = BooleanField(default=False)  # Validée par tout le monde

    def save(self, *args, **kwargs):
        self.checked = self.valide and self.dette_set.count() > 0 and all([dette.valide for dette in self.dette_set.all()])

        super(Creance, self).save(*args, **kwargs)

        self.creancier.maj_solde()
        for dette in self.dette_set.all():
            dette.debiteur.maj_solde()

    def debiteurs(self):
        liste = [u'<a href="%s">%s (%i part(s))</a>' % (d.get_absolute_url(), d.debiteur, d.parts) for d in self.dette_set.all()]
        return mark_safe(", ".join(liste))

    def nombre_parts(self):
        return self.dette_set.all().aggregate(s=Sum('parts'))['s']

    def valeur_part(self):
        return self.montant / self.nombre_parts()

    def get_absolute_url(self):
        #return reverse('creance_detail', kwargs={'pk': self.pk})
        return reverse('creance_list')

    def __unicode__(self):
        return u"Créance de %s de %.2f € le %s" % (self.creancier, self.montant, self.moment)

    class Meta:
        ordering = ["moment"]


class Dette(Model):
    creance = ForeignKey(Creance, verbose_name=u"Créance")
    debiteur = ForeignKey(PortailUser, verbose_name=u"Débiteur")
    parts = IntegerField(u"Nombre de parts", default=1)
    valide = BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Dette, self).save(*args, **kwargs)

        self.creance.save()

    def valeur(self):
        return self.parts * self.creance.valeur_part()

    def get_absolute_url(self):
        #return reverse('dette_detail', kwargs={'pk': self.pk})
        return reverse('dette_list')

    def __unicode__(self):
        return u"%s doit %.2f € à %s" % (self.debiteur, self.valeur(), self.creance.creancier)

    class Meta:
        unique_together = ("creance", "debiteur")


class Remboursement(Model):
    crediteur = ForeignKey(PortailUser, verbose_name=u"Créditeur", related_name='debits')
    credite = ForeignKey(PortailUser, verbose_name=u"Crédité", related_name='credits')
    montant = DecimalField(max_digits=8, decimal_places=2)
    moment = DateTimeField()
    valide_crediteur = BooleanField(default=False)
    valide_credite = BooleanField(default=False)

    def validable(self, user):
        crediteur = self.crediteur.user == user and not self.valide_crediteur
        credite = self.credite.user == user and not self.valide_credite
        return crediteur or credite

    def save(self, *args, **kwargs):
        super(Remboursement, self).save(*args, **kwargs)

        self.credite.maj_solde()
        self.crediteur.maj_solde()

    def get_absolute_url(self):
        #return reverse('remboursement_detail', kwargs={'pk': self.pk})
        return reverse('remboursement_list')

    def __unicode__(self):
        return u"%s a remboursé %.2f € à %s" % (self.crediteur, self.montant, self.credite)

    class Meta:
        ordering = ["-moment"]
