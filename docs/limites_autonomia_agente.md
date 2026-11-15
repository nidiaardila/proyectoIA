# Límites de autonomía: Asistente de Logística y Envíos (`src/agente_con_memoria.py`)

## Herramientas y nivel de riesgo
- `consultar_estado_envio_detallado`: **bajo** (solo lectura; consulta el diccionario de estados `ESTADOS` por número de seguimiento y opcionalmente formatea su historial, sin modificar registros ni ejecutar acciones externas).
- `calcular_costo_envio`: **bajo** (solo cálculo; aplica la fórmula aritmética de costo estimado según `peso_kg` y `distancia_km` y devuelve un texto informativo, sin impacto operativo ni financiero).
- `generar_reembolso`: **alto** (escritura irreversible con impacto económico directo; procesa la devolución de dinero para un `numero_pedido` por un `monto` determinado, por lo que un error o alucinación del modelo genera una pérdida económica directa).

## Herramientas que requieren aprobación humana
- `generar_reembolso`: Requiere aprobación humana obligatoria antes de ejecutarse porque implica un movimiento de dinero irreversible. Está implementada invocando `esperar_aprobacion(mensaje, tiempo_limite_segundos=15)` dentro de la propia herramienta antes de confirmar la operación. Si el supervisor responde algo distinto de `"s"` o si se agota el tiempo de espera (`timeout`), la función devuelve `False` por defecto (bloqueo seguro) y cancela el reembolso. Tanto las aprobaciones como los rechazos quedan auditados en `registro_aprobaciones` mediante `registrar_aprobacion()` con fecha y hora ISO.

## Revisión de trazas
- **Frecuencia:** Revisión semanal de una muestra representativa de interacciones en `trazas_agente.jsonl`, más la revisión del **100% de las trazas** donde se haya invocado la herramienta de riesgo alto (`generar_reembolso`).
- **Qué se busca:**
  - **Repeticiones consecutivas de la misma herramienta:** Detectadas automáticamente ejecutando `marcar_repeticiones_sospechosas("trazas_agente.jsonl")`, lo que indica que el agente entró en bucle o recibió observaciones ambiguas.
  - **Invocaciones de riesgo alto sin respaldo de supervisión:** Verificar que toda aparición de `"herramienta": "generar_reembolso"` en `trazas_agente.jsonl` refleje en su `observacion` y en `registro_aprobaciones` la decisión explícita del supervisor humano.
  - **Respuestas finales que no coinciden con las observaciones:** Casos en los que `respuesta_final` afirma estados de envío, costos o confirmaciones de reembolso que no provienen del campo `observacion` devuelto por la herramienta ejecutada.

## Qué hacer ante un comportamiento inesperado
1. **Desactivar de inmediato la herramienta afectada:** Retirar `generar_reembolso` (o la herramienta en cuestión) de la lista `herramientas = [...]` en `src/agente_con_memoria.py` y reiniciar el servicio para cortar cualquier ejecución autónoma riesgosa.
2. **Auditar las trazas y el registro de aprobaciones:** Filtrar las sesiones afectadas en `trazas_agente.jsonl` y contrastarlas con `registro_aprobaciones` para identificar con qué entrada (`entrada`) y argumentos (`argumentos`) falló el agente.
3. **Ajustar el esquema de validación o las descripciones:** Corregir el docstring de la herramienta, reforzar las restricciones de tipos y descripciones en el esquema Pydantic (`args_schema`) o precisar las instrucciones del `system` prompt en `prompt_agente`.
4. **Verificar en entorno de pruebas antes de reactivar:** Ejecutar nuevamente los casos conflictivos verificando en `trazas_agente.jsonl` que `intermediate_steps` y el bloqueo de `esperar_aprobacion()` funcionen correctamente antes de volver a incluir la herramienta en producción.