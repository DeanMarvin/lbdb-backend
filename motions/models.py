from django.db import models
from staff.models import Staff


class Motions(models.Model):

    m_id = models.AutoField(primary_key=True)
    startdatum = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    enddatum = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    type = models.CharField(max_length=100)
    antragsteller_vorname = models.CharField(max_length=100)
    antragsteller_nachname = models.CharField(max_length=100)
    antragsteller_initialen = models.CharField(max_length=15)
    bearbeiter = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return '{}, {} {}'.format(self.type, self.antragsteller_vorname, self.antragsteller_nachname)

    class Meta:
        verbose_name_plural = 'Anträge'
        ordering = ['antragsteller_nachname']
