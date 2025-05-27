from uuid import UUID
from datetime import datetime
from typing import Literal
from ninja import Schema


class DocumentoSchema(Schema):
    id: UUID
    credor_id: UUID
    tipo: Literal["identidade", "comprovante_residencia"]
    arquivo_url: str
    enviado_em: datetime
