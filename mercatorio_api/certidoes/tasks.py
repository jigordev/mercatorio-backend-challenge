from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Certidao
from .services.certidoes_api import get_certidoes_api
from core.utils import get_file_from_base64
from django.utils import timezone
from datetime import timedelta

logger = get_task_logger(__name__)


@shared_task
def revalidate_certidoes():
    expired = Certidao.objects.filter(
        origem="api", recebida_em__lt=timezone.now() - timedelta(days=180)
    )

    cpf_cnpj_dict = {}
    for certidao in expired:
        cpf_cnpj = certidao.credor.cpf_cnpj
        if cpf_cnpj not in cpf_cnpj_dict:
            cpf_cnpj_dict[cpf_cnpj] = []
        cpf_cnpj_dict[cpf_cnpj].append(certidao)

    for cpf_cnpj, certidoes in cpf_cnpj_dict.items():
        try:
            result = get_certidoes_api(cpf_cnpj)

            if "error" in result:
                logger.warning(
                    f"Erro ao buscar certidões para o credor {cpf_cnpj}: {result['error']}"
                )
                continue

            for new_certidao in result["certidoes"]:
                tipo = new_certidao["tipo"]
                for old_certidao in [c for c in certidoes if c.tipo == tipo]:
                    old_certidao.status = new_certidao["status"]
                    old_certidao.arquivo = get_file_from_base64(
                        new_certidao["conteudo_base64"]
                    )
                    old_certidao.recebida_em = timezone.now()
                    old_certidao.save()
        except Exception as e:
            logger.exception(f"Erro ao validar certidões de {cpf_cnpj}: {e}")
