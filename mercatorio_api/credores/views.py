from uuid import UUID
from typing import List
from datetime import datetime
from ninja.errors import HttpError
from ninja import Router, Form, UploadedFile, File
from .schemas import CredorSchema, PrecatorioSchema, CredorPrecatorioSchema
from documentos.schemas import DocumentoSchema
from certidoes.schemas import CertidaoSchema
from .models import Credor
from documentos.models import Documento
from certidoes.models import Certidao
from precatorios.models import Precatorio
from certidoes.services.certidoes_api import get_certidoes_api
from core.utils import validate_uploaded_file

router = Router()


@router.get("/{credor_id}", response=CredorSchema)
def get_credor_by_id(request, credor_id: UUID):
    try:
        credor = Credor.objects.get(id=credor_id)
    except Credor.DoesNotExist:
        raise HttpError(404, "Credor não encontrado")

    return CredorSchema.from_orm(credor)


@router.post("/", response=CredorPrecatorioSchema)
def create_credor(request, data: CredorPrecatorioSchema):
    credor_data = data.dict(exclude={"precatorio"})
    precatorio_data = data.precatorio.dict()

    credor = Credor.objects.create(**credor_data)
    Precatorio.objects.create(**precatorio_data, credor=credor)

    credor.refresh_from_db()

    return CredorPrecatorioSchema.from_orm(credor)


@router.post("/{credor_id}/documentos", response=DocumentoSchema)
def upload_documento(
    request, credor_id: UUID, tipo: str = Form(...), file: UploadedFile = File(...)
):
    try:
        credor = Credor.objects.get(id=credor_id)
    except Credor.DoesNotExist:
        raise HttpError(404, "Credor não encontrado")

    validate_uploaded_file(file)

    documento = Documento.objects.create(credor_id=credor.id, tipo=tipo, arquivo=file)
    return DocumentoSchema.from_orm(documento)


@router.post("/{credor_id}/certidoes", response=CertidaoSchema)
def upload_certidao(
    request,
    credor_id: UUID,
    tipo: str = Form(...),
    status: str = Form(...),
    file: UploadedFile = File(...),
):
    try:
        credor = Credor.objects.get(id=credor_id)
    except Credor.DoesNotExist:
        raise HttpError(404, "Credor não encontrado")

    validate_uploaded_file(file)

    certidao = Certidao.objects.create(
        credor_id=credor.id, tipo=tipo, origem="manual", status=status, arquivo=file
    )
    return CertidaoSchema.from_orm(certidao)


@router.post("/{credor_id}/buscar-certidoes", response=List[CertidaoSchema])
def search_certidoes(request, credor_id: UUID):
    try:
        credor = Credor.objects.get(id=credor_id)
    except Credor.DoesNotExist:
        raise HttpError(404, "Credor não encontrado")

    response = get_certidoes_api(credor.cpf_cnpj)

    if "error" in response:
        return HttpError(400, "Erro ao buscar as certidões")

    certidoes_criadas = []

    for certidao_data in response["certidoes"]:
        certidao_values = {
            "credor_id": credor.id,
            "tipo": certidao_data["tipo"],
            "status": certidao_data["status"],
            "origem": "api",
            "conteudo_base64": certidao_data["conteudo_base64"],
            "recebida_em": datetime.utcnow(),
        }

        obj, created = Certidao.objects.update_or_create(
            credor_id=credor.id, tipo=certidao_data["tipo"], defaults=certidao_values
        )
        certidoes_criadas.append(obj)

    return certidoes_criadas
