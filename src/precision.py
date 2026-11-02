import json
from collections import Counter
import time
from src.pipeline_limpieza import procesar_texto
from src.cliente import consultar_modelo


def contar_coincidencias(tokens_ref: list[str], tokens_resp: list[str]) -> int:
    conteo_ref = Counter(tokens_ref)
    conteo_resp = Counter(tokens_resp)
    return sum((conteo_ref & conteo_resp).values())


def calcular_precision_cobertura_f1(tokens_ref: list[str], tokens_resp: list[str]) -> dict[str, float]:
    coincidencias = contar_coincidencias(tokens_ref, tokens_resp)
    if not tokens_resp or not tokens_ref:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_resp)
    cobertura = coincidencias / len(tokens_ref)
    f1 = 0.0 if (precision + cobertura) == 0 else (2 * precision * cobertura) / (precision + cobertura)

    return {
        "precision": round(precision, 4),
        "cobertura": round(cobertura, 4),
        "f1": round(f1, 4),
    }


def calcular_metricas(texto_ref: str, texto_resp: str) -> dict[str, float]:
    return calcular_precision_cobertura_f1(procesar_texto(texto_ref), procesar_texto(texto_resp))


# 20 casos de evaluación para el Asistente de RRHH
casos = [
    ("¿Cuántos días de vacaciones legales corresponden al año?", "Corresponden quince días hábiles de vacaciones remuneradas por cada año trabajado."),
    ("¿Qué plazo tengo para entregar una licencia médica?", "El trabajador tiene un plazo de dos días hábiles para presentarla."),
    ("¿Dónde consulto el reglamento interno?", "El reglamento interno está publicado para libre consulta en la intranet corporativa."),
    ("¿Cómo solicito el permiso por día de cumpleaños?", "El día libre de cumpleaños se solicita con una semana de anticipación."),
    ("¿Hasta qué hora puedo avisar una ausencia imprevista?", "Debes avisar a tu jefatura directa antes de las diez de la mañana."),
    ("¿Cuándo se pagan los sueldos en la empresa?", "Los sueldos se transfieren el último día hábil de cada mes."),
    ("¿Cómo reembolso un gasto de salud dental?", "Ingresa al portal de beneficios y adjunta la boleta del gasto médico."),
    ("¿Cuántos días corresponden por permiso de matrimonio?", "Corresponden cinco días hábiles continuos de permiso pagado por matrimonio civil."),
    ("¿Qué beneficio existe para el nacimiento de un hijo?", "El padre tiene derecho a cinco días de permiso laboral pagado."),
    ("¿Cómo solicito un adelanto de sueldo?", "Los anticipos se solicitan en el portal interno entre los días diez y quince."),
    ("¿Dónde descargo mi liquidación de sueldo?", "Las liquidaciones mensuales se descargan directamente en el portal de autoservicio de personal."),
    ("¿El uniforme de trabajo tiene algún costo?", "La empresa entrega los uniformes y elementos de protección sin ningún costo."),
    ("¿Cuántos días de permiso corresponden por duelo de un padre?", "Corresponden cuatro días hábiles continuos por fallecimiento de padre o madre."),
    ("¿Se pueden acumular períodos de vacaciones?", "Se pueden acumular legalmente hasta dos períodos consecutivos con autorización previa."),
    ("¿Qué canal uso para denunciar acoso laboral?", "Las denuncias se ingresan confidencialmente mediante el canal ético de la intranet."),
    ("¿A quién solicito constancia de antigüedad laboral?", "El certificado de antigüedad se solicita al correo del departamento de personas."),
    ("¿Cuál es la jornada ordinaria máxima de trabajo semanal?", "La jornada máxima ordinaria de trabajo es de cuarenta y cuatro horas semanales."),
    ("¿Qué seguro complementario tiene la empresa?", "La empresa cuenta con un seguro complementario de salud financiado de manera compartida."),
    ("¿El permiso por mudanza es remunerado?", "El trabajador dispone de un día hábil pagado por cambio de domicilio."),
    ("¿Dónde reviso los convenios corporativos vigentes?", "Los convenios y descuentos comerciales están listados en la pestaña beneficios de intranet."),
]

system_instruction = (
    "Eres un asistente de Recursos Humanos. Responde en español con una frase concisa "
    "de máximo 15 palabras, sin introducciones ni listas."
)

resultados = []

print("Generando 20 consultas y calculando métricas...")
for consulta, referencia in casos:
    respuesta = consultar_modelo(consulta, system_instruction=system_instruction)
    metricas = calcular_metricas(referencia, respuesta)
    resultados.append({
        "consulta": consulta,
        "referencia": referencia,
        "respuesta": respuesta,
        **metricas,
    })
    # Pausa de 5 segundos para respetar el límite de 15 peticiones por minuto
    time.sleep(5)

resultados_ordenados = sorted(resultados, key=lambda r: r["f1"])

with open("resultados_metricas.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados_ordenados, archivo, indent=2, ensure_ascii=False)

print("¡Listo! Guardado en resultados_metricas.json")