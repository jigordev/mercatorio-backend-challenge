from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from factory import generate_certidoes

app = FastAPI(root_path="/api-mock")


class Certidao(BaseModel):
    tipo: str
    status: str
    conteudo_base64: str


class CertidaoResponse(BaseModel):
    cpf_cnpj: str
    certidoes: List[Certidao]


@app.get("/certidoes", response_model=CertidaoResponse)
async def get_certidoes(cpf_cnpj: str):
    certidoes = generate_certidoes()
    return {"cpf_cnpj": cpf_cnpj, "certidoes": certidoes}
