from uuid6 import uuid7
from django.db import models
from credores.models import Credor

TIPOS = ["federal", "estadual", "municipal", "trabalhista"]
ORIGENS = ["manual", "api"]
STATUS = ["negativa", "positiva", "invalida", "pendente"]


class Certidao(models.Model):
    id = models.UUIDField(default=uuid7, unique=True, primary_key=True)
    tipo = models.CharField(choices=[(v, v) for v in TIPOS])
    origem = models.CharField(choices=[(v, v) for v in ORIGENS])
    arquivo = models.FileField(upload_to="certidoes/")
    arquivo_url = models.URLField(blank=True, null=True)
    status = models.CharField(choices=[(v, v) for v in STATUS])
    recebida_em = models.DateTimeField(auto_now_add=True)

    credor = models.ForeignKey(
        Credor, related_name="certidoes", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.arquivo and not self.arquivo_url:
            self.arquivo_url = self.arquivo.url
            super().save(update_fields=["arquivo_url"])
