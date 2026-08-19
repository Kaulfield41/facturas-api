import json
from schemas import Factura

resultado = Factura.model_json_schema()

print("--- DICCIONARIO ---")
print(type(resultado))
print(resultado)

texto = json.dumps(resultado, ensure_ascii=False)

print("--- DESPUÉS DE DUMPS ---")
print(type(texto))
print(texto)