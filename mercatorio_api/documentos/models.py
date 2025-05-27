from uuid6 import uuid7
from django.db import models
from credores.models import Credor

TIPOS = ["identidate", "comprovante_residencia"]


class Documento(models.Model):
    id = models.UUIDField(default=uuid7, unique=True, primary_key=True)
    tipo = models.CharField(choices=[(v, v) for v in TIPOS])
    arquivo = models.FileField(upload_to="documentos/")
    arquivo_url = models.URLField(blank=True, null=True)
    enviado_em = models.DateTimeField(auto_now_add=True)

    credor = models.ForeignKey(
        Credor, related_name="documentos", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.arquivo and not self.arquivo_url:
            self.arquivo_url = self.arquivo.url
            super().save(update_fields=["arquivo_url"])
