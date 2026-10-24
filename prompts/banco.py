BANCO_DE_PROMPT = [
    {
        "nombre": "clasificar_consulta_rrhh",
        "system_instruction": (
            "Eres un asistente de clasificación para Recursos Humanos. "
            "Analiza la consulta del empleado y responde únicamente con un JSON con las claves: "
            "'categoria' ('vacaciones', 'licencias_medicas', 'beneficios', 'remuneraciones' o 'otro'), "
            "'urgencia' ('baja', 'media' o 'alta') y "
            "'requiere_escalamiento_humano' (boolean)."
        ),
        "ejemplo_usuario": "Tuve un accidente camino a la oficina y necesito ingresar mi licencia médica hoy mismo.",
        "claves_esperadas": ["categoria", "urgencia", "requiere_escalamiento_humano"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "categoria": {"type": "STRING"},
                "urgencia": {"type": "STRING"},
                "requiere_escalamiento_humano": {"type": "BOOLEAN"},
            },
            "required": ["categoria", "urgencia", "requiere_escalamiento_humano"],
        },
    },
    {
        "nombre": "extraer_datos_solicitud",
        "system_instruction": (
            "Eres un extractor de datos para solicitudes de colaboradores. "
            "Extrae la información clave del mensaje y responde únicamente con un JSON con las claves: "
            "'tipo_tramite' (string), "
            "'periodo_o_dias' (string con la cantidad de días o rango de fechas, o 'no especificado'), y "
            "'menciona_documento' (boolean, true si habla de certificado, comprobante o formulario)."
        ),
        "ejemplo_usuario": "Quiero solicitar 5 días hábiles de vacaciones a partir del 15 de noviembre, ya tengo el visto bueno de mi jefatura.",
        "claves_esperadas": ["tipo_tramite", "periodo_o_dias", "menciona_documento"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "tipo_tramite": {"type": "STRING"},
                "periodo_o_dias": {"type": "STRING"},
                "menciona_documento": {"type": "BOOLEAN"},
            },
            "required": ["tipo_tramite", "periodo_o_dias", "menciona_documento"],
        },
    },
    {
        "nombre": "generar_respuesta_asistente",
        "system_instruction": (
            "Eres el Asistente Virtual de Políticas Internas de RRHH. "
            "Responde a la duda del empleado de manera cordial y estructurada. "
            "Devuelve únicamente un JSON con las claves: "
            "'mensaje_respuesta' (texto directo y empático), "
            "'pasos_a_seguir' (lista de strings con los pasos puntuales), y "
            "'canal_contacto' (string con el área o correo de contacto sugerido)."
        ),
        "ejemplo_usuario": "¿Cómo puedo pedir el reembolso del seguro complementario de salud?",
        "claves_esperadas": ["mensaje_respuesta", "pasos_a_seguir", "canal_contacto"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "mensaje_respuesta": {"type": "STRING"},
                "pasos_a_seguir": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                },
                "canal_contacto": {"type": "STRING"},
            },
            "required": ["mensaje_respuesta", "pasos_a_seguir", "canal_contacto"],
        },
    },
]