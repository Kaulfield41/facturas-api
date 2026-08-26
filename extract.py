import json
import csv
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv
from schemas import Factura

load_dotenv()
client = Anthropic()

schema = json.dumps(Factura.model_json_schema(), ensure_ascii=False)

def procesar_factura(texto):
    prompt = f"""Extrae los datos de esta factura y devuelve SOLO un objeto JSON
que cumpla este schema, sin explicaciones ni ```json.
    
El emisor es quien cobra, no quien paga.
Las fechas en formato ISO (AAAA-MM-DD).
Los importes como números, con punto decimal.
    
SCHEMA:
{schema}
    
FACTURA:
{texto}"""
    respuesta = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
    crudo = respuesta.content[0].text.strip()
    if crudo.startswith("```"):
        crudo = crudo.split("```")[1].removeprefix("json").strip()

    factura = Factura.model_validate_json(crudo)

    suma = factura.base_imponible + factura.cuota_iva
    if abs(suma - factura.total) > 0.01:
        raise ValueError(
            f"Los importes no cuadran: {factura.base_imponible} + "
            f"{factura.cuota_iva} = {suma}, pero el total dice {factura.total}"
        )

    return factura

resultados = []
fallos = []

for ruta in Path("facturas").glob("*.txt"):
    texto = ruta.read_text()
    try:
        factura = procesar_factura(texto)
        resultados.append(factura)
        print(f"OK  {ruta.name}")
    except Exception as error:
        fallos.append((ruta.name, str(error)))
        print(f"FALLO  {ruta.name}: {error}")

print(f"\n{len(resultados)} correctas, {len(fallos)} fallidas")



with open("resultados.csv", "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(["emisor", "nif_emisor", "numero_factura",
                        "fecha_emision", "base_imponible", "cuota_iva", "total"])
    for factura in resultados:
        escritor.writerow([factura.emisor, factura.nif_emisor,
                            factura.numero_factura, factura.fecha_emision,
                            factura.base_imponible, factura.cuota_iva,
                            factura.total])

