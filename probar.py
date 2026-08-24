from pathlib import Path

carpeta = Path("facturas")
archivos = list(carpeta.glob("*.txt"))

print(archivos)