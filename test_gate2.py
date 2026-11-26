import logging
from langgraph.types import Command

from src.servicio_rag import (
    HUELLA_PROMPT_ACTIVO,
    cargar_indice,
    construir_grafo_supervision,
    responder_consulta,
)

# Dato sensible
CORREO = "ana.perez@example.com"
PREGUNTA = "¿Cuantos dias de vacaciones tengo al año? Mi correo es " + CORREO

_vectorstore = None
_estado_indice = "indice_reutilizado"


def ejecutar_servicio(pregunta):
    """Corre el flujo real completo (indexar/reutilizar, recuperar, filtrar y responder)."""
    global _vectorstore, _estado_indice
    if _vectorstore is None:
        _vectorstore, _estado_indice = cargar_indice()
    resultado = responder_consulta(
        pregunta,
        vectorstore=_vectorstore,
        estado_indice=_estado_indice,
        session_id="test-gate2",
    )
    return resultado["respuesta"], resultado["fuentes"]


def crear_supervision():
    """Devuelve el grafo real de supervision humana compilado con checkpointer."""
    app = construir_grafo_supervision()
    return app, {"huella_nueva": HUELLA_PROMPT_ACTIVO, "aprobado": False}


def test_1_pipeline_sin_excepciones():
    respuesta, _ = ejecutar_servicio(PREGUNTA)
    assert respuesta.strip(), "el servicio devolvio una respuesta vacia"


def test_2_respuesta_cita_fuente():
    respuesta, fuentes = ejecutar_servicio(PREGUNTA)
    assert fuentes, "el servicio no devolvio ninguna fuente"
    assert any(f in respuesta for f in fuentes), "la respuesta no menciona su fuente"


def test_3_logs_sin_contenido_crudo(caplog):
    with caplog.at_level(logging.DEBUG):
        ejecutar_servicio(PREGUNTA)
    texto_logs = " ".join(r.getMessage() + " " + str(r.__dict__) for r in caplog.records)
    assert CORREO not in texto_logs, "un dato sensible aparece en los logs"
    assert PREGUNTA not in texto_logs, "la consulta completa aparece en los logs"


def test_4_supervision_pausa_y_reanuda():
    app, entrada = crear_supervision()
    config = {"configurable": {"thread_id": "test-gate2"}}
    pausado = app.invoke(entrada, config=config)
    assert "__interrupt__" in pausado, "el grafo no se detuvo en el punto de supervision"
    final = app.invoke(Command(resume=True), config=config)
    assert "__interrupt__" not in final, "el grafo sigue pausado despues de reanudar"
    assert final["aprobado"] is True, "la decision no quedo registrada"