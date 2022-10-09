
from django.db import models

class Texto(models.Model):
    link = models.URLField()
    resumo = models.TextField(blank=True,null=True)
    

   





