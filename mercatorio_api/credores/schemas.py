from uuid import UUID
from decimal import Decimal
from datetime import date
from typing import List
from ninja import Schema
from documentos.schemas import DocumentoSchema
from certidoes.schemas import CertidaoSchema


class PrecatorioSchema(Schema):
    id: UUID | None = None
    numero_precatorio: str
    valor_nominal: Decimal
    foro: str
    data_publicacao: date


class CredorPrecatorioSchema(Schema):
    id: UUID | None = None
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str
    precatorio: PrecatorioSchema


class CredorSchema(Schema):
    id: UUID
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str
    precatorio: PrecatorioSchema
    documentos: List[DocumentoSchema]
    certidoes: List[CertidaoSchema]
