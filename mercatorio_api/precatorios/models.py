from uuid6 import uuid7
from django.db import models
from credores.models import Credor


class Precatorio(models.Model):
    id = models.UUIDField(default=uuid7, unique=True, primary_key=True)
    numero_precatorio = models.CharField(max_length=50)
    valor_nominal = models.DecimalField(max_digits=10, decimal_places=2)
    foro = models.CharField(max_length=20)
    data_publicacao = models.DateField(auto_now_add=True)

    credor = models.OneToOneField(
        Credor, related_name="precatorio", on_delete=models.CASCADE
    )
