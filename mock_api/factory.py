import random
import base64
from faker import Faker

faker = Faker("pt_BR")

TIPOS_CERTIDAO = ["federal", "estadual", "municipal", "trabalhista"]
STATUS_CERTIDAO = ["negativa", "positiva", "invalida", "pendente"]


def generate_certidoes():
    tipos = TIPOS_CERTIDAO.copy()
    quantity = random.randint(1, len(tipos))

    certidoes = []

    for i in range(quantity):
        tipo = tipos.pop(0)
        status = random.choice(STATUS_CERTIDAO)
        conteudo = faker.text()

        certidoes.append(
            {
                "tipo": tipo,
                "status": status,
                "conteudo_base64": base64.b64encode(conteudo.encode()).decode(),
            }
        )

    return certidoes
