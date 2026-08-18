from datetime import date
from pydantic import BaseModel

class Factura(BaseModel):
    emisor: str
    nif_emisor: str
    numero_factura: str
    fecha_emision: date
    base_imponible: float
    total: float