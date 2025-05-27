from fastapi import FastAPI
from factory import generate_certidoes

app = FastAPI(root_path="/api-mock")


@app.get("/certidoes")
async def get_certidoes(cpf_cnpj: str):
    certidoes = generate_certidoes()
    return {"cpf_cnpj": cpf_cnpj, "certidoes": certidoes}
