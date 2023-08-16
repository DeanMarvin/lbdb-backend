from django.db import models

class Desks(models.Model):

    d_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=350, blank=False)
    client = models.CharField(max_length=50, blank=False)
    licence = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Arbeitsplätze'
        ordering = ['d_id']


