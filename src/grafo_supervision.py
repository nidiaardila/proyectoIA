from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class EstadoDespliegue(TypedDict):
    huella_nueva: str
    aprobado: bool


def proponer(estado: EstadoDespliegue):
    print("nodo: proponer, huella propuesta:", estado["huella_nueva"])
    return {}


def supervisar(estado: EstadoDespliegue):
    decision = interrupt({
        "motivo": "aprobar nueva version de prompt_asistente_rrhh en produccion",
        "huella_propuesta": estado["huella_nueva"],
    })
    return {"aprobado": decision}


def aplicar(estado: EstadoDespliegue):
    if estado["aprobado"]:
        print("version", estado["huella_nueva"], "activada")
    else:
        print("version", estado["huella_nueva"], "rechazada, se mantiene la anterior")
    return {}


grafo = StateGraph(EstadoDespliegue)
grafo.add_node("proponer", proponer)
grafo.add_node("supervisar", supervisar)
grafo.add_node("aplicar", aplicar)
grafo.add_edge(START, "proponer")
grafo.add_edge("proponer", "supervisar")
grafo.add_edge("supervisar", "aplicar")
grafo.add_edge("aplicar", END)

app_despliegue = grafo.compile(checkpointer=InMemorySaver())

# Huella de la v2 generada en registro_prompts.py
huella = "3c5e5ac08c7d"

# 1) Camino de aprobacion
config = {"configurable": {"thread_id": "mi-despliegue-rrhh-1"}}
resultado_pausado = app_despliegue.invoke(
    {"huella_nueva": huella, "aprobado": False},
    config=config,
)
print("1) tras invocar (interrumpido):", resultado_pausado)

snapshot = app_despliegue.get_state(config)
print("2) pendiente:", snapshot.interrupts[0].value)

resultado_aprobado = app_despliegue.invoke(Command(resume=True), config=config)
print("3) tras aprobar:", resultado_aprobado)

# 2) Camino de rechazo (con otro thread_id)
config2 = {"configurable": {"thread_id": "mi-despliegue-rrhh-2"}}
app_despliegue.invoke(
    {"huella_nueva": huella, "aprobado": False},
    config=config2,
)
snapshot2 = app_despliegue.get_state(config2)
print("\n4) pendiente (segundo hilo):", snapshot2.interrupts[0].value)

resultado_rechazado = app_despliegue.invoke(Command(resume=False), config=config2)
print("5) tras rechazar:", resultado_rechazado)