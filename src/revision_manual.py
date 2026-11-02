import json

revision_manual = [
    # --- 5 casos con menor F1 (falsos negativos / respuestas alternativas) ---
    {
        "consulta": "¿Dónde consulto el reglamento interno?",
        "f1": 0.2857,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Falso negativo por sinónimos: el modelo usó 'portal de empleados' en lugar de 'intranet corporativa'. El sentido es idéntico pero la métrica léxica castigó el vocabulario."
    },
    {
        "consulta": "¿Hasta qué hora puedo avisar una ausencia imprevista?",
        "f1": 0.3333,
        "correccion_factual": "no",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Error de dato específico: el modelo indicó 'antes del inicio de tu turno' en vez de la cifra exacta estipulada 'antes de las diez de la mañana'."
    },
    {
        "consulta": "¿Cómo solicito el permiso por día de cumpleaños?",
        "f1": 0.3636,
        "correccion_factual": "si",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Omitió el plazo de antelación: confirmó el trámite pero no mencionó que debe pedirse con una semana de anticipación."
    },
    {
        "consulta": "¿Dónde descargo mi liquidación de sueldo?",
        "f1": 0.4000,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Variación léxica válida: usó 'plataforma de nómina' en vez de 'portal de autoservicio'. Orientación correcta a pesar del bajo F1."
    },
    {
        "consulta": "¿Qué seguro complementario tiene la empresa?",
        "f1": 0.4210,
        "correccion_factual": "parcialmente",
        "completitud": "parcialmente",
        "contradiccion": "no",
        "nota": "Respuesta ambigua: mencionó cobertura médica general pero omitió el carácter de cofinanciamiento con la empresa."
    },

    # --- 5 casos con mayor F1 (confirmación y detección de falsos positivos) ---
    {
        "consulta": "¿Cuántos días de vacaciones legales corresponden al año?",
        "f1": 0.9091,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Excelente coincidencia léxica y conceptual: cita con exactitud los quince días hábiles anuales."
    },
    {
        "consulta": "¿Cuántos días corresponden por permiso de matrimonio?",
        "f1": 0.8889,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Respuesta precisa: incluye la cantidad de días (cinco) y la condición de días hábiles continuos pagados."
    },
    {
        "consulta": "¿El uniforme de trabajo tiene algún costo?",
        "f1": 0.8571,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Confirmación de gratuidad correcta, coincidiendo casi en la totalidad de tokens con la política de vestuario corporativo."
    },
    {
        "consulta": "¿Qué plazo tengo para entregar una licencia médica?",
        "f1": 0.8235,
        "correccion_factual": "si",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "El número coincide (dos días hábiles), respaldando la validez del puntaje alto."
    },
    {
        "consulta": "¿Cuál es la jornada ordinaria máxima de trabajo semanal?",
        "f1": 0.7742,
        "correccion_factual": "no",
        "completitud": "si",
        "contradiccion": "no",
        "nota": "Falso positivo peligroso: obtuvo F1 alto por coincidir en estructura y palabras, pero indicó 'cuarenta y cinco horas' en vez de 'cuarenta y cuatro horas'."
    }
]

if __name__ == "__main__":
    with open("revision_manual.json", "w", encoding="utf-8") as archivo:
        json.dump(revision_manual, archivo, indent=2, ensure_ascii=False)
    print("Archivo revision_manual.json generado exitosamente.")