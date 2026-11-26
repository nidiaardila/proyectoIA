def puntaje_riesgo(probabilidad, impacto):
    return probabilidad * impacto


def categoria_riesgo(puntaje):
    if puntaje >= 15:
        return "CRITICO"
    if puntaje >= 9:
        return "ALTO"
    if puntaje >= 4:
        return "MEDIO"
    return "BAJO"


def esta_en_el_limite(probabilidad, impacto):
    categoria_actual = categoria_riesgo(puntaje_riesgo(probabilidad, impacto))
    vecinos = [
        (probabilidad + 1, impacto),
        (probabilidad - 1, impacto),
        (probabilidad, impacto + 1),
        (probabilidad, impacto - 1),
    ]
    for p2, i2 in vecinos:
        if not (1 <= p2 <= 5 and 1 <= i2 <= 5):
            continue
        if categoria_riesgo(puntaje_riesgo(p2, i2)) != categoria_actual:
            return True
    return False


mis_riesgos = [
    {
        "riesgo": "Inyeccion de prompt via consulta de colaborador o documento de RRHH indexado",
        "probabilidad": 4,
        "impacto": 4,
        "mitigacion": "Separacion System/Human, delimitacion con <contexto> y filtro regex en src/prevencion_prompt_inyection.py (Bloque 31)",
    },
    {
        "riesgo": "Filtracion de PII en logs cuando colaboradores consultan sobre licencias medicas o remuneraciones",
        "probabilidad": 3,
        "impacto": 5,
        "mitigacion": "Registro de huellas SHA-256 (generar_huella) y longitud en vez de contenido crudo en src/logs_rag.py (Bloque 31)",
    },
    {
        "riesgo": "Respuesta con normativa laboral obsoleta (ej. 45 h en vez de 44 h) por reglamento de RRHH no reindexado",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": "Actualizacion incremental del indice Chroma con IDs explicitos y chequeo de integridad en src/rag_indexer.py (Bloque 25)",
    },
    {
        "riesgo": "Despliegue de una nueva version del prompt de RRHH que rompa citas obligatorias o protecciones de seguridad",
        "probabilidad": 3,
        "impacto": 3,
        "mitigacion": "Registro versionado con huellas SHA-256 y diff palabra por palabra en registro_prompts.py (Bloque 32)",
    },
    {
        "riesgo": "Deprecacion sin aviso del modelo de embeddings (models/gemini-embedding-001) que rompa la busqueda en Chroma",
        "probabilidad": 2,
        "impacto": 4,
        "mitigacion": "Revision periodica de documentacion oficial y prueba de embeddings en src/prueba_embeddings.py (Bloque 28)",
    },
    {
        "riesgo": "Respuesta incompleta por brecha de cobertura del corpus (faltan 5 documentos de RRHH por indexar)",
        "probabilidad": 3,
        "impacto": 2,
        "mitigacion": "Regla de abstencion explicita en el prompt y plan de carga de 5 documentos en docs/decision_personalizacion.md (Bloque 30)",
    },
    {
        "riesgo": "Sobrecosto inesperado por consulta individual en el flujo RAG actual de RRHH",
        "probabilidad": 1,
        "impacto": 1,
        "mitigacion": "Instrumentacion de tokens y costo por consulta en src/registro_rag.py y registros_latencia_costo.jsonl (Bloque 26)",
    },
]

# Puntos de supervision humana asociados a cada riesgo ALTO o CRITICO
puntos_supervision = {
    "Inyeccion de prompt via consulta de colaborador o documento de RRHH indexado": (
        "Revision humana antes de responder o indexar cuando detectar_inyeccion() marca un texto sospechoso."
    ),
    "Filtracion de PII en logs cuando colaboradores consultan sobre licencias medicas o remuneraciones": (
        "Aprobacion humana para autorizar acceso de lectura a rag_logs.jsonl y para agregar nuevos campos al logger."
    ),
    "Respuesta con normativa laboral obsoleta (ej. 45 h en vez de 44 h) por reglamento de RRHH no reindexado": (
        "Validacion humana de un encargado de RRHH sobre la version vigente antes de reindexar cambios normativos en produccion."
    ),
    "Despliegue de una nueva version del prompt de RRHH que rompa citas obligatorias o protecciones de seguridad": (
        "Aprobacion explicita via interrupt() en grafo_supervision.py tras revisar el diff antes de activar la nueva huella."
    ),
}

for r in mis_riesgos:
    r["puntaje"] = puntaje_riesgo(r["probabilidad"], r["impacto"])
    r["categoria"] = categoria_riesgo(r["puntaje"])
    r["al_limite"] = esta_en_el_limite(r["probabilidad"], r["impacto"])

print("=== MATRIZ DE RIESGOS ORDENADA POR PUNTAJE ===")
for r in sorted(mis_riesgos, key=lambda x: -x["puntaje"]):
    marca = "[AL LIMITE]" if r["al_limite"] else ""
    print(f"{r['categoria']:8} ({r['puntaje']:2}) - {r['riesgo']} {marca}")

print("\n=== FILAS AL LIMITE (REVISAR CON OTRA PERSONA) ===")
for r in sorted(mis_riesgos, key=lambda x: -x["puntaje"]):
    if r["al_limite"]:
        print("revisar con otra persona:", r["riesgo"])

print("\n=== PUNTOS DE SUPERVISION HUMANA (RIESGOS ALTO Y CRITICO) ===")
for r in sorted(mis_riesgos, key=lambda x: -x["puntaje"]):
    if r["categoria"] in ("CRITICO", "ALTO"):
        supervision = puntos_supervision[r["riesgo"]]
        print(f"- [{r['categoria']}] {r['riesgo']}\n  Supervision: {supervision}")