from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

try:
    from src.enrutamiento import (
        construir_paso_clasificacion,
        construir_cadena_con_enrutamiento,
        construir_cadena_queja_segura,
        procesar_mensaje_seguro,
    )
except ImportError:
    from enrutamiento import (
        construir_paso_clasificacion,
        construir_cadena_con_enrutamiento,
        construir_cadena_queja_segura,
        procesar_mensaje_seguro,
    )


def test_clasificacion_normaliza_antes_de_comparar():
    """Verifica que el paso de clasificación limpie espacios y pase a minúsculas."""
    modelo_falso = MagicMock()
    modelo_falso.return_value = AIMessage(content=" Queja \n")
    paso = construir_paso_clasificacion(modelo_falso)
    resultado = paso.invoke({"mensaje": "algo salió mal"})
    assert resultado == "queja"


def test_enrutamiento_va_a_cadena_queja():
    """Verifica que si clasifica como queja ejecute la rama de quejas."""
    paso_clasif_falso = RunnableLambda(lambda x: "queja")
    cadena_queja_falsa = RunnableLambda(lambda x: "atendiendo reclamo")
    cadena_sugerencia_falsa = RunnableLambda(lambda x: "atendiendo sugerencia")
    cadena_defecto_falsa = RunnableLambda(lambda x: "atendiendo defecto")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=paso_clasif_falso,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_defecto_falsa,
    )
    resultado = cadena.invoke({"mensaje": "estoy inconforme"})
    assert resultado == "atendiendo reclamo"


def test_enrutamiento_va_a_cadena_sugerencia():
    """Verifica que si clasifica como sugerencia ejecute la rama de sugerencias."""
    paso_clasif_falso = RunnableLambda(lambda x: "sugerencia")
    cadena_queja_falsa = RunnableLambda(lambda x: "atendiendo reclamo")
    cadena_sugerencia_falsa = RunnableLambda(lambda x: "atendiendo sugerencia")
    cadena_defecto_falsa = RunnableLambda(lambda x: "atendiendo defecto")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=paso_clasif_falso,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_defecto_falsa,
    )
    resultado = cadena.invoke({"mensaje": "podrían agregar modo oscuro"})
    assert resultado == "atendiendo sugerencia"


def test_enrutamiento_va_a_cadena_pregunta():
    """Verifica que si clasifica como pregunta ejecute la rama de preguntas."""
    paso_clasif_falso = RunnableLambda(lambda x: "pregunta")
    cadena_queja_falsa = RunnableLambda(lambda x: "atendiendo reclamo")
    cadena_sugerencia_falsa = RunnableLambda(lambda x: "atendiendo sugerencia")
    cadena_pregunta_falsa = RunnableLambda(lambda x: "atendiendo pregunta")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=paso_clasif_falso,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )
    resultado = cadena.invoke({"mensaje": "¿cómo cambio mi clave?"})
    assert resultado == "atendiendo pregunta"


def test_enrutamiento_usa_default_ante_categoria_desconocida():
    """Verifica que categorías imprevistas caigan en la rama por defecto."""
    paso_clasif_falso = RunnableLambda(lambda x: "desconocido")
    cadena_queja_falsa = RunnableLambda(lambda x: "atendiendo reclamo")
    cadena_sugerencia_falsa = RunnableLambda(lambda x: "atendiendo sugerencia")
    cadena_defecto_falsa = RunnableLambda(lambda x: "atendiendo por defecto")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=paso_clasif_falso,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_defecto_falsa,
    )
    resultado = cadena.invoke({"mensaje": "mensaje ambiguo"})
    assert resultado == "atendiendo por defecto"


def test_cadena_queja_usa_fallback_ante_fallo_del_modelo():
    """Verifica que with_fallbacks ejecute la respuesta de contingencia ante caídas de la ruta."""
    def fallar_a_proposito(x):
        raise ConnectionError("Fallo simulado de red en el modelo")

    cadena_queja_rota = RunnableLambda(fallar_a_proposito)
    cadena_segura = construir_cadena_queja_segura(cadena_queja_rota)

    resultado = cadena_segura.invoke({"mensaje": "esto no funciona"})
    assert "equipo" in resultado.lower()


def test_procesar_mensaje_seguro_no_propaga_excepciones():
    """Verifica que el try/except global capture fallos fuera de las rutas (ej. en clasificación)."""
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.side_effect = ConnectionError(
        "Fallo simulado antes del enrutamiento"
    )

    cadena_falsa = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
    )

    resultado = procesar_mensaje_seguro(cadena_falsa, "mensaje de prueba")
    assert "no pudimos procesar" in resultado.lower()