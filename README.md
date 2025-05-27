# Mercatório Backend Challenge

Este projeto é uma API REST desenvolvida para simular a etapa de **originação de precatórios** na Mercatório. Ele permite o cadastro de credores e seus precatórios, o upload de documentos pessoais e certidões, além da simulação da obtenção automática de certidões via uma API mock local.

---

## Stack Utilizada

- **Django** + **Django Ninja** (API REST principal)
- **FastAPI** (API mock de certidões)
- **PostgreSQL** (banco de dados)
- **Celery + Redis** (tarefas assíncronas e periódicas)
- **Traefik** (reverse proxy)
- **Docker Compose**

---

## Como rodar o projeto localmente

### Pré-requisitos

- Docker
- Docker Compose

### 1. Clone o repositório

```bash
git clone https://github.com/jigordev/mercatorio-backend-challenge.git
cd mercatorio-backend-challenge
````

### 2. Suba os serviços

```bash
docker compose up --build
```

A API principal estará disponível em:
**[http://localhost/api](http://localhost/api)**
A API mock de certidões estará disponível em:
**[http://localhost/api-mock](http://localhost/api-mock)**

---

## Estrutura dos Serviços

| Serviço          | Porta | URL                                                                |
| ---------------- | ----- | ------------------------------------------------------------------ |
| Django API       | 80    | [http://localhost/api](http://localhost/api)                               |
| FastAPI (Mock)   | 80    | [http://localhost/api-mock](http://localhost/api-mock)             |
| Traefik (Painel) | 8080  | [http://localhost:8080/dashboard](http://localhost:8080/dashboard) |

---

## Variáveis de Ambiente

As variáveis estão configuradas no arquivo: `mercatorio_api/.env`. Veja o exemplo abaixo:

```env
POSTGRES_DB=mercatoriodb
POSTGRES_USER=mercatorio
POSTGRES_PASSWORD=abcABC123

DJANGO_SETTINGS_MODULE=mercatorio_api.settings
DATABASE_URL=postgres://mercatorio:abcABC123@db:5432/mercatoriodb
REDIS_URL=redis://redis:6379/0

DEBUG=True

SECRET_KEY="..."

ALLOWED_HOSTS="localhost,127.0.0.1,[::1]"

MAX_UPLOAD_SIZE=2
ALLOWED_UPLOAD_CONTENT_TYPE="application/pdf,image/jpg,image/jpeg,image/png"

MOCK_API_URL="http://fastapi:8000/api-mock"

CORS_ALLOW_ALL_ORIGINS=True

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="redis://redis:6379/0"
```

---

## Endpoints Disponíveis

### `POST /api/credores`

Cadastra um credor e seu precatório.

#### Exemplo (HTTPie):

```bash
http POST http://localhost/api/credores nome="Maria Silva" cpf_cnpj="12345678900" email="maria@example.com" telefone="11999999999" precatorio:='{"numero_precatorio":"0001234-56.2020.8.26.0050","valor_nominal":50000,"foro":"TJSP","data_publicacao":"2023-10-01"}'
```

---

### `POST /api/credores/{id}/documentos`

Upload de documentos pessoais.

#### Exemplo:

```bash
http -f POST http://localhost/api/credores/{id}/documentos tipo="identidade" file@documento.pdf
```

---

### `POST /api/credores/{id}/certidoes`

Upload manual de certidões.

#### Exemplo:

```bash
http -f POST http://localhost/api/credores/{id}/certidoes tipo="federal" status="negativa" file@certidao.pdf
```

---

### `POST /api/credores/{id}/buscar-certidoes`

Busca automática de certidões via API mock.

#### Exemplo:

```bash
http POST http://localhost/api/credores/{id}/buscar-certidoes
```

---

### `GET /api/credores/{id}`

Consulta geral de um credor, incluindo documentos, precatórios e certidões.

#### Exemplo:

```bash
http GET http://localhost/api/credores/{id}
```

---

## API Mock de Certidões

Disponível em:
`GET /api-mock/certidoes?cpf_cnpj=00000000000`

### Exemplo de resposta:

```json
{
  "cpf_cnpj": "00000000000",
  "certidoes": [
    {
      "tipo": "federal",
      "status": "negativa",
      "conteudo_base64": "..."
    },
    {
      "tipo": "trabalhista",
      "status": "positiva",
      "conteudo_base64": "..."
    }
  ]
}
```

## Documentação OpenAPI (DEBUG=True)
Disponível em:
`GET /api/openapi.json`

---

## Django Admin:

Para alterar as informações de acesso do admin django basta declarar as variáveis no .env:

`DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`

Valores padrão: admin, admin@example.com, admin.

---

## Executar os testes

```bash
sudo docker exec -it django-api uv run manage.py test credores.tests
```

---

## Revalidação de Certidões

* As certidões com origem da `api` são revalidadas automaticamente a cada 24 horas usando o **Celery Beat**.
* O agendamento está configurado dentro do projeto com `django-celery-beat`.

---

## Extras

* Validação de tipo e tamanho dos arquivos implementada com base em configurações de ambiente.
* Os arquivos são armazenados localmente dentro do container.
* Estrutura modular seguindo boas práticas de separação de domínios (apps separados para credores, precatórios, documentos e certidões).
