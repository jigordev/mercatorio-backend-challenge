from django.test import TestCase
from ninja.testing import TestClient
from .views import router
from .models import Credor
from precatorios.models import Precatorio
from certidoes.models import Certidao
from documentos.models import Documento
from django.core.files.uploadedfile import SimpleUploadedFile

credor_data = {
    "nome": "Maria Silva",
    "cpf_cnpj": "12345678900",
    "email": "maria@example.com",
    "telefone": "11999999999",
    "precatorio": {
        "numero_precatorio": "0001234-56.2020.8.26.0050",
        "valor_nominal": 50000.00,
        "foro": "TJSP",
        "data_publicacao": "2023-10-01",
    },
}


class CredoresTest(TestCase):
    def test_create_credor(self):
        client = TestClient(router)

        data = credor_data.copy()

        response = client.post("/", json=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get("cpf_cnpj"), data.get("cpf_cnpj"))
        self.assertTrue(result.get("id") is not None)

    def test_upload_documento(self):
        fake_file = SimpleUploadedFile(
            content_type="application/pdf",
            content=b"Fake document for test",
            name="documento.pdf",
        )

        data = credor_data.copy()
        data.pop("precatorio")

        credor = Credor.objects.create(**data)

        client = TestClient(router)

        response = client.post(
            f"/{credor.id}/documentos",
            FILES={"file": fake_file},
            data={"tipo": "identidade"},
        )
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get("tipo"), "identidade")
        self.assertEqual(str(result.get("credor_id", "")), str(credor.id))

    def test_upload_certidao(self):
        fake_file = SimpleUploadedFile(
            content_type="application/pdf",
            content=b"Fake certificate for test",
            name="certificado.pdf",
        )

        data = credor_data.copy()
        data.pop("precatorio")

        credor = Credor.objects.create(**data)

        client = TestClient(router)

        response = client.post(
            f"/{credor.id}/certidoes",
            FILES={"file": fake_file},
            data={"tipo": "federal", "status": "positiva"},
        )
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get("tipo"), "federal")
        self.assertEqual(result.get("status"), "positiva")
        self.assertEqual(str(result.get("credor_id", "")), str(credor.id))

    def test_get_api_certidoes(self):
        data = credor_data.copy()
        data.pop("precatorio")

        credor = Credor.objects.create(**data)

        client = TestClient(router)

        response = client.post(f"/{credor.id}/buscar-certidoes")
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result.get("certidoes"), list)

    def test_get_credor(self):
        data = credor_data.copy()
        precatorio_data = data.pop("precatorio")

        credor = Credor.objects.create(**data)
        precatorio = Precatorio.objects.create(credor_id=credor.id, **precatorio_data)

        documento_file = SimpleUploadedFile(
            name="documento.pdf",
            content=b"Test document",
            content_type="application/pdf",
        )
        documento = Documento.objects.create(
            credor_id=credor.id, tipo="identidade", arquivo=documento_file
        )

        certidao_file = SimpleUploadedFile(
            name="certidao.pdf",
            content=b"Test certificate",
            content_type="application/pdf",
        )
        certidao = Certidao.objects.create(
            credor_id=credor.id,
            tipo="federal",
            origem="manual",
            status="positiva",
            arquivo=certidao_file,
        )

        client = TestClient(router)

        response = client.get(f"/{credor.id}")
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result.get("cpf_cnpj"), data.get("cpf_cnpj"))
        self.assertEqual(
            result.get("precatorio", {}).get("numero_precatorio"),
            precatorio.numero_precatorio,
        )

        documentos = result.get("documentos")
        self.assertIsInstance(documentos, list)
        self.assertEqual(documentos[0].get("tipo"), documento.tipo)

        certidoes = result.get("certidoes")
        self.assertIsInstance(certidoes, list)
        self.assertEqual(certidoes[0].get("tipo"), certidao.tipo)
