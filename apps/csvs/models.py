from django.db import models
from apps.bops.models import Bop


class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    bop = models.ForeignKey(Bop, on_delete=models.CASCADE)

    def __str__(self):
        return f'File id: {self.id}'
