from pathlib import Path


def recomendar_estrategia(respuestas):
    puntos = {"RAG": 0, "Fine-tuning completo": 0, "PEFT": 0}

    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3
    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1
    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1
    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1
    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2

    maximo = max(puntos.values())
    ganadoras = [tecnica for tecnica, p in puntos.items() if p == maximo]
    return puntos, ganadoras


# Asistente de Recursos Humanos y Políticas de Empresa
respuestas_mi_caso = {
    "informacion_cambia_seguido": True,           # Políticas de RRHH, beneficios y normativa laboral (reglamento v2.0, jornada 45->44 h) cambian periódicamente
    "problema_de_formato_o_tono": False,          # 9/9 pruebas de consistencia JSON aprobadas (0 % de fallos con response_schema)
    "dataset_grande_y_de_calidad": False,         # 0 ejemplos etiquetados de RRHH para tuning (solo 8 ejemplos genéricos en docs/ejemplos_tuning.jsonl)
    "presupuesto_limitado_o_iterar_rapido": True, # Presupuesto acotado (consultas RAG ~$0.00025-$0.00035 USD) y necesidad de actualizar políticas en minutos
    "necesita_multiples_variantes": False,        # Un único asistente corporativo de RRHH para toda la empresa
}

if any(valor is None for valor in respuestas_mi_caso.values()):
    raise SystemExit("Completa las cinco respuestas con True o False antes de continuar.")

puntos, ganadoras = recomendar_estrategia(respuestas_mi_caso)
print(puntos)
print("candidatas:", ganadoras)


def generar_esqueleto_decision(problema, puntos, ganadoras):
    empate = len(ganadoras) > 1
    lineas = []
    lineas.append("# Decision de personalizacion")
    lineas.append("")
    lineas.append("## 1. El problema")
    lineas.append(problema)
    lineas.append("")
    lineas.append("## 2. Resultado del metodo de decision")
    for tecnica, p in sorted(puntos.items(), key=lambda x: -x[1]):
        lineas.append(f"- {tecnica}: {p} puntos")
    if empate:
        lineas.append("")
        lineas.append(f"**Empate entre: {', '.join(ganadoras)}**")
    lineas.append("")
    lineas.append("## 3. Tecnica elegida y por que")
    if empate:
        lineas.append(
            "[COMPLETAR: el puntaje no resolvio el empate solo -- "
            "justifica aqui con criterio propio]"
        )
    else:
        lineas.append(f"[COMPLETAR: por que {ganadoras[0]} responde mejor a este caso]")
    lineas.append("")
    lineas.append("## 4. Que necesitarias para ejecutarla")
    lineas.append(
        "[COMPLETAR: corpus faltante, o cantidad de ejemplos etiquetados que faltan]"
    )
    return "\n".join(lineas)


if __name__ == "__main__":
    esqueleto = generar_esqueleto_decision(
        (
            "El Asistente de Recursos Humanos responde con datos desactualizados u omite "
            "condiciones específicas de la empresa cuando los colaboradores consultan sobre "
            "normativa interna: en la revisión manual de 10 consultas reales "
            "(revision_manual.json), 4 respuestas (40 %) presentaron errores factuales o "
            "información incompleta, mientras que el formato JSON mantiene 100 % de "
            "consistencia (9/9 pruebas aprobadas)."
        ),
        puntos,
        ganadoras,
    )
    print(esqueleto)

    ruta_salida = Path(__file__).resolve().parent.parent / "docs" / "decision_personalizacion.md"
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(esqueleto)