# Decisión de personalización: Asistente de Recursos Humanos y Políticas de Empresa

## 1. El problema
El Asistente de Recursos Humanos responde con datos desactualizados u omite condiciones específicas de la empresa cuando los colaboradores consultan sobre normativa interna. En la revisión manual de 10 consultas reales (`revision_manual.json`), 4 respuestas (40 %) fallaron por contenido: 2 tuvieron errores factuales (indicó 45 horas de jornada semanal en lugar de 44 y omitió la hora límite de aviso de ausencias) y 2 fueron incompletas (omitieron el plazo de anticipación del permiso de cumpleaños y el cofinanciamiento del seguro complementario), mientras que el formato de salida mantiene 100 % de consistencia (9 de 9 pruebas aprobadas con `response_schema`).

## 2. Resultado del método de decisión
- RAG: 5 puntos
- PEFT: 1 punto
- Fine-tuning completo: 0 puntos

Ganador claro: **RAG** (sin empate).

Evidencia de las cinco preguntas evaluadas en `src/decision.py`:
- `informacion_cambia_seguido = True`: las políticas de RRHH, beneficios y normativa laboral se actualizan periódicamente (por ejemplo, versión vigente `docs/reglamento_interno_rrhh.txt` v2.0 y actualización de la jornada semanal de 45 a 44 horas).
- `problema_de_formato_o_tono = False`: 0 de 9 fallos de estructura en las pruebas de consistencia JSON (`src/consistencia.py`).
- `dataset_grande_y_de_calidad = False`: 0 ejemplos etiquetados de RRHH para entrenamiento (solo existen 8 ejemplos de prueba de clasificación de errores técnicos en `docs/ejemplos_tuning.jsonl`, muy por debajo del umbral de 200).
- `presupuesto_limitado_o_iterar_rapido = True`: se requiere reflejar cambios de normativa en minutos y mantener bajo costo operativo (las consultas medidas en `registros_latencia_costo.jsonl` cuestan entre $0.00025 y $0.00035 USD con latencias de 1.07 a 2.27 s).
- `necesita_multiples_variantes = False`: se opera un único asistente corporativo de RRHH para toda la organización.

## 3. Técnica elegida y por qué
Elijo **RAG**. El problema del sistema no es de tono ni de formato, sino de acceso a información corporativa vigente y trazable con citas. RAG resuelve esa carencia directamente: cuando RRHH actualiza un artículo o beneficio, basta con reindexar el documento en Chroma en segundos o minutos, sin trabajo humano de etiquetado ni ciclos lentos de entrenamiento.

Descarto **PEFT** y **fine-tuning completo** por costo de datos, tiempo e iteración: construir un dataset mínimo de 200 ejemplos de RRHH bien etiquetados a 5 minutos por ejemplo tomaría **16.7 horas** de trabajo humano (sin contar revisión), cada intento de entrenamiento toma de minutos a horas, y cualquier cambio futuro en el reglamento obligaría a reetiquetar y reentrenar. Además, al correr el análisis de sensibilidad cambiando una respuesta a la vez, **RAG sigue ganando en los 5 escenarios**, lo que confirma que la decisión es estable.

## 4. Qué necesitarías para ejecutarla
Actualmente el repositorio cuenta con **1 documento** de RRHH indexado (`docs/reglamento_interno_rrhh.txt`, con 5 artículos sobre vacaciones, licencias médicas, seguro complementario, permisos/modalidad híbrida y remuneraciones). Para cubrir las brechas detectadas en `revision_manual.json` y `resultados_metricas.json`, faltan **5 documentos adicionales por recopilar e indexar** en `chroma_db` (para completar un corpus inicial de **6 documentos**):
1. Política de jornada ordinaria semanal (44 horas) y protocolo de aviso de ausencias imprevistas.
2. Anexo de permisos especiales adicionales (día de cumpleaños y mudanza).
3. Política de adelantos y anticipos de sueldo.
4. Política de vestuario y uniformes corporativos.
5. Guía operativa del Portal de Colaboradores y flujo de reembolsos y escalamiento.

Adicionalmente, falta reemplazar las **4 consultas técnicas genéricas** de `resultados_evaluacion_rag.txt` (actualmente con `F1 = 0.00`) por una batería de **15 preguntas reales de RRHH** cubriendo los 6 documentos, con el fin de medir precisión y cobertura reales del índice antes de pasar a producción.