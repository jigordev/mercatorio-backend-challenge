import httpx
from typing import Optional, Any
from django.conf import settings


def _make_request(
    method: str, endpoint: str, params: Optional[Any] = None, data: Optional[Any] = None
):
    try:
        url = f"{settings.MOCK_API_URL}/{endpoint}"
        response = httpx.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_certidoes_api(cpf_cnpj: str):
    return _make_request("GET", "/certidoes", params={"cpf_cnpj": cpf_cnpj})
