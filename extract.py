import json
from anthropic import Anthropic
from dotenv import load_dotenv
from schemas import Factura

load_dotenv()
client = Anthropic()

texto = open("factura_ejemplo_3.txt").read()
schema = json.dumps(Factura.model_json_schema(), ensure_ascii=False)

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

crudo = respuesta.content[0].text
print("--- CRUDO ---")
print(crudo)

crudo = crudo.strip()
if crudo.startswith("```"):
    crudo = crudo.split("```")[1]
    if crudo.startswith("json"):
        crudo = crudo[4:]
    crudo = crudo.strip()

factura = Factura.model_validate_json(crudo)
print("--- VALIDADO ---")
print(factura)