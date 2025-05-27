from django.utils.timezone import now
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Certidao
from credores.models import Credor
from .services.certidoes_api import get_certidoes_api
from core.utils import get_file_from_base64

logger = get_task_logger(__name__)


def revalidate_certidoes_for_credor(credor):
    result = get_certidoes_api(credor.cpf_cnpj)

    if "error" in result:
        logger.warning(
            f"Erro ao buscar certidões para credor {credor.id}: {result['error']}"
        )
        return

    for certidao_mock in result["certidoes"]:
        try:
            Certidao.objects.update_or_create(
                credor_id=credor.id,
                origem="api",
                tipo=certidao_mock["tipo"],
                defaults={
                    "status": certidao_mock["status"],
                    "arquivo": get_file_from_base64(certidao_mock["conteudo_base64"]),
                    "recebida_em": now(),
                },
            )
            logger.info(
                f"Certidão {certidao_mock['tipo']} revalidada para credor {credor.id}"
            )
        except Exception as e:
            logger.exception(
                f"Erro ao revalidar certidão {certidao_mock['tipo']} para credor {credor.id}: {str(e)}"
            )


@shared_task
def revalidate_certidoes():
    credores = Credor.objects.filter(certidao__origem="api").distinct()
    for credor in credores:
        revalidate_certidoes_for_credor(credor)
