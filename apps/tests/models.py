from django.db import models


class Test(models.Model):
    interval = models.FloatField()
    coverage = models.FloatField()

    def __str__(self):
        return f'id: {self.id} interval: {self.interval} - coverage: {self.coverage}'
