from extract import procesar_factura

def test_procesa_factura_iberdrola():
    texto = open("facturas/factura_ejemplo.txt").read()
    factura = procesar_factura(texto)

    assert factura.emisor == "IBERDROLA CLIENTES, S.A.U."
    assert factura.total == 79.99