from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #Modelo
from langchain_core.prompts import PromptTemplate #Plantilla -> Prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Parsea la respuesta y la transforma en solo textos
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Bifurcaciones/Branches/Ramificaciones

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra: "
    "pregunta, queja o sugerencia. Responde solo con esa palabra. \n\n {mensaje}"
)

# Función constructora: permite inyectar un modelo falso (MagicMock) en los tests
def construir_paso_clasificacion(modelo_a_usar=modelo):
    return (
        plantilla_clasificacion
        | modelo_a_usar
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )
paso_clasificacion = construir_paso_clasificacion(modelo)


cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluará dentro del producto: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

#Fallback: cadena de respaldo. Captura las caídas de mi LLM (RateLimitError, 401, APIConnectionError, respuestas vacías)
respuesta_generica = RunnableLambda(
    lambda x: (
        "Gracias por tu mensaje. Un miembro de nuestro "
        "equipo te va a responder pronto."
    )
)

# Función constructora: envuelve cadena_queja con fallback para proteger la ruta y probarla con mocks
def construir_cadena_queja_segura(cadena_queja=cadena_queja):
    return cadena_queja.with_fallbacks([respuesta_generica])
cadena_queja_segura = construir_cadena_queja_segura(cadena_queja)

# Función constructora: arma la bifurcación (RunnableBranch) y la cadena completa con enrutamiento
def construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=cadena_queja_segura,
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
):
    bifurcacion = RunnableBranch(
        (lambda x: x["clasificacion"] == "queja", cadena_queja),           # if clasificacion == "queja"
        (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia), # elif clasificacion == "sugerencia"
        cadena_pregunta                                                    # else (ruta por defecto)
    )
    return (
        RunnablePassthrough.assign(clasificacion=paso_clasificacion)
        | bifurcacion
    )
cadena_con_enrutamiento = construir_cadena_con_enrutamiento()
cadena_robusta = cadena_con_enrutamiento.with_fallbacks([respuesta_generica])


# Red de seguridad final: captura cualquier error no cubierto en clasificación y lo registra
def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        print(f"Error procesando mensaje: {error}")
        return "No pudimos procesar tu mensaje en este momento. Intenta de nuevo más tarde."
    

if __name__ == "__main__": #Solamente ejecuta el siguiente bloque de código si la ejecución es directa del archivo. NO EJECUTES si es import
    mensaje = "Llevo varios días sin poder entrar a mi cuenta."
    print(procesar_mensaje_seguro(cadena_robusta, mensaje))
    
# Entrada inicial: {"mensaje": "Deberían de tener más agentes disponibles."}
#                   │
#                   ▼
# RunnablePassthrough
#   1: Pasa el mensaje a paso_clasificacion -> Return "sugerencia"
#   2: Fusiono clasificacion y mensaje
#   3: Return {"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion": "sugerencia"}
#                   │
#                   ▼
# bifurcacion (RunnableBranch)
#   ¿clasificacion == "queja"? NO
#   ¿clasificacion == "sugerencia" SI
#       Entra a la cadena_sugerencia
#       cadena_sugerencia.invoke({"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion": "sugerencia"})
#       Return respuesta final generada