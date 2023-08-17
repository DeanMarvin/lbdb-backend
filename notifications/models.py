from django.db import models
from staff.models import Staff

class Notifications(models.Model):

    n_id = models.AutoField(primary_key=True)
    s_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    datum = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.datum, self.s_id)

    class Meta:
        verbose_name_plural = 'Mitteilungen'
        ordering = ['datum']