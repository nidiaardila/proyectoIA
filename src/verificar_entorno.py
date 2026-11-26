import os
import sys
from importlib.metadata import PackageNotFoundError, version

PAQUETES = [
    "langchain-core",
    "langchain-chroma",
    "langchain-google-genai",
    "langgraph",
    "python-dotenv",
    "pytest",
]
VARIABLES = ["GEMINI_API_KEY"]
INDICE_DIR = "indice_gate2"

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

problemas = []
print("Python:", sys.version.split()[0])
if sys.version_info < (3, 10):
    problemas.append("usar Python 3.10 o superior")

for paquete in PAQUETES:
    try:
        print(f"{paquete}: {version(paquete)}")
    except PackageNotFoundError:
        print(f"{paquete}: NO instalado")
        problemas.append(f"instalar {paquete}")

for nombre in VARIABLES:
    estado = "definida" if os.getenv(nombre) else "FALTA"
    print(f"{nombre}: {estado}")
    if estado == "FALTA":
        problemas.append(f"definir {nombre} en el archivo .env")

if os.path.isdir(INDICE_DIR) and os.listdir(INDICE_DIR):
    print(f"indice en {INDICE_DIR}/: ok")
else:
    print(f"indice en {INDICE_DIR}/: NO existe o esta vacio")
    problemas.append("ejecutar python3 src/servicio_rag.py para crear el indice")

print()
if problemas:
    print("Pendiente: " + "; ".join(problemas))
    sys.exit(1)
print("Entorno listo para la corrida final")