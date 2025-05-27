import base64
import magic
import uuid
from ninja.errors import HttpError
from django.conf import settings
from django.core.files.base import ContentFile


def get_file_from_base64(base64_string: str):
    try:
        decoded_file = base64.b64decode(base64_string)
        mime = magic.from_buffer(decoded_file, mime=True)
        extension = mime.split("/")[-1]
        filename = f"certidao-{uuid.uuid4()}.{extension}"
        return ContentFile(decoded_file, name=filename)
    except Exception as e:
        raise ValueError("Erro ao processar base64") from e


def validate_uploaded_file(file):
    if file.size > int(settings.MAX_UPLOAD_SIZE) * 1024 * 1024:
        raise HttpError(400, f"Arquivo excede {settings.MAX_UPLOAD_SIZE}MB")

    if file.content_type not in settings.ALLOWED_UPLOAD_CONTENT_TYPE:
        raise HttpError(400, "Formato de arquivo inválido")
