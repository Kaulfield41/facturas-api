# Extracción estructurada de facturas

Extrae datos de facturas en texto libre y devuelve 7 campos tipados y validados:
emisor, NIF del emisor, número de factura, fecha de emisión, base imponible, cuota de iva y total.

Usa la API de Claude para la extracción y Pydantic para definir el formato de salida
y validar la respuesta. El esquema del prompt se genera desde el propio modelo Pydantic,
de forma que añadir un campo solo requiere modificar `schemas.py`.

Probado con facturas de Iberdrola, Jazztel y tickets de Alcampo.

## Limitaciones conocidas

- **El modelo calcula valores que no están en el documento.** Con un ticket con tres
  tipos de IVA, devolvió como base imponible la suma de las tres bases, un número que
  no aparece escrito en el ticket.
- **Prohibirlo en el prompt no lo resuelve.** Al añadir "extrae únicamente valores
  literales", el resultado empeoró: devolvió un número que no era ni la suma ni ninguna
  de las bases, y truncó el número de factura.
- **El esquema asume un único tipo de IVA.** Documentos con varios tipos no encajan.
- **La extracción de PDF no es limpia.** El símbolo del euro aparece como `¤` y las
  tablas llegan con las columnas desalineadas.
- **La comprobación de importes verifica coherencia, no fidelidad.** Se valida que
  base + cuota = total, lo que detecta valores corruptos o mal leídos. No detecta
  una reconstrucción coherente: con el ticket de Alcampo, el modelo sumó las tres
  bases y las tres cuotas, y la comprobación pasó con datos que no están escritos
  en el documento.
- **Documentos con varios tipos de IVA deberían rechazarse, no procesarse.** Aún
  no está implementado.

  ## Coste

Aproximadamente 0,003 $ por factura con Claude Sonnet, según el consumo
registrado durante el desarrollo (0,06 $ en unas veinte llamadas de prueba).
Con esa cifra, procesar doscientas facturas al mes cuesta menos de 1 $.