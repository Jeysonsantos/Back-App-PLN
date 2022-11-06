from django.db import models

class Portal(models.Model):
    nomePortal = models.CharField(max_length=100)
    filtroTexto = models.CharField(max_length=1000)

    def __str__(self):
        return self.nomePortal
