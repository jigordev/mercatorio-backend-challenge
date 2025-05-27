from uuid6 import uuid7
from django.db import models


class Credor(models.Model):
    id = models.UUIDField(default=uuid7, unique=True, primary_key=True)
    nome = models.CharField(max_length=50)
    cpf_cnpj = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    telefone = models.CharField(max_length=20)
