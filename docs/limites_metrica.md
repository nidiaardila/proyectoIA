# Límites de la métrica de evaluación

## Qué mide
Mide el traslape léxico exacto de palabras entre la respuesta generada por el modelo y la referencia de políticas internas de RRHH, contabilizando repeticiones mediante métricas de precisión, cobertura y F1.

## Modos de falla conocidos
- **Paráfrasis y sinonimia técnica (Falso negativo):** Respuestas que orientan al empleado de forma correcta obtienen un F1 bajo si utilizan términos equivalentes. Ejemplo: en la consulta "¿El uniforme de trabajo tiene algún costo?", el modelo respondió "es totalmente gratuito" en lugar de "sin ningún costo", obteniendo un F1 de apenas 0.087 a pesar de ser factualmente correcta.
- **Cifras legales y plazos alterados con alto F1 (Falso positivo):** La métrica no pondera el valor semántico de números o fechas frente al resto de la frase. Ejemplo: en "¿Cuál es la jornada ordinaria máxima de trabajo semanal?", el modelo respondió "40 horas semanales" en vez de "cuarenta y cuatro horas semanales", conservando un F1 engañosamente alto de 0.7273 con un dato incorrecto.
- **Omisión de condiciones habilitantes:** Respuestas que confirman un beneficio pero omiten restricciones críticas (como topes de períodos o días específicos de permiso) mantienen puntuaciones bajas o moderadas de F1 y fallan en completitud operativa.

## Muestra revisada
10 casos evaluados a mano (los 5 con menor F1 y los 5 con mayor F1) seleccionados a partir de un conjunto de 20 consultas sobre políticas de RRHH ejecutadas el 2026-11-02.

## Recomendación de uso
Utilizar el F1 léxico únicamente como métrica orientativa para pruebas de regresión masivas y control de consistencia estructural. Toda respuesta que defina plazos de licencias, cantidad de días de permiso o cifras de compensación debe validarse mediante una verificación de datos exactos o revisión manual obligatoria.