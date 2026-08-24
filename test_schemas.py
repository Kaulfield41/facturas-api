from datetime import date
from schemas import Factura
import pytest
from pydantic import ValidationError

def test_factura_valida():
    factura = Factura(
        emisor="Iberdrola",
        nif_emisor="A-95758389",
        numero_factura="123",
        fecha_emision=date(2026, 6, 1),
        base_imponible=66.11,
        cuota_iva=13.88,
        total=79.99,
    )
    assert factura.emisor == "Iberdrola"
    assert factura.total == 79.99
    assert factura.fecha_emision == date(2026, 6, 1)

def test_factura_invalida():
    with pytest.raises(ValidationError):
        Factura(
            emisor="Iberdrola",
            nif_emisor="A-95758389",
            numero_factura="123",
            fecha_emision="Esto no es una fecha",  # Fecha inválida
            base_imponible=66.11,
            cuota_iva=13.88,
            total=79.99, 
        )
