from uuid import UUID
from datetime import datetime
from typing import Literal
from ninja import Schema


class CertidaoSchema(Schema):
    id: UUID
    credor_id: UUID
    tipo: Literal["federal", "estadual", "municipal", "trabalhista"]
    origem: Literal["manual", "api"]
    arquivo_url: str
    status: Literal["negativa", "positiva", "invalida", "pendente"]
    recebida_em: datetime
