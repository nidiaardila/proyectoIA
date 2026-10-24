# Respaldo de Validación de Consistencia - Banco de Prompts (U1.5)

**Fecha:** Octubre 2026  
**Proyecto:** Asistente de Recursos Humanos y Políticas de Empresa  
**Comando ejecutado:** `python3 -m src.consistencia`  
**Resultado global:** 9/9 ejecuciones exitosas (100% de consistencia)

---

## 1. Resumen por Prompt

| Prompt | Tarea | Intentos | Éxitos | Tasa de éxito |
| :--- | :--- | :---: | :---: | :---: |
| `clasificar_consulta_rrhh` | Clasificación de área y urgencia | 3 | 3 | 100% |
| `extraer_datos_solicitud` | Extracción de fechas y trámites | 3 | 3 | 100% |
| `generar_respuesta_asistente` | Respuesta estructurada al empleado | 3 | 3 | 100% |

---

## 2. Detalle de Salidas Obtenidas

### Prompt 1: `clasificar_consulta_rrhh`
* **Entrada de prueba:** *"Tuve un accidente camino a la oficina y necesito ingresar mi licencia médica hoy mismo."*
* **Salidas obtenidas (JSON estructurado):**
  * **Intento 1:**
    ```json
    {
      "categoria": "licencias_medicas",
      "urgencia": "alta",
      "requiere_escalamiento_humano": true
    }
    ```
  * **Intento 2:**
    ```json
    {
      "categoria": "licencias_medicas",
      "urgencia": "alta",
      "requiere_escalamiento_humano": true
    }
    ```
  * **Intento 3:**
    ```json
    {
      "categoria": "licencias_medicas",
      "urgencia": "alta",
      "requiere_escalamiento_humano": true
    }
    ```

---

### Prompt 2: `extraer_datos_solicitud`
* **Entrada de prueba:** *"Quiero solicitar 5 días hábiles de vacaciones a partir del 15 de noviembre, ya tengo el visto bueno de mi jefatura."*
* **Salidas obtenidas (JSON estructurado):**
  * **Intentos 1, 2 y 3 (consistentes):**
    ```json
    {
      "tipo_tramite": "vacaciones",
      "periodo_o_dias": "5 días hábiles a partir del 15 de noviembre",
      "menciona_documento": false
    }
    ```

---

### Prompt 3: `generar_respuesta_asistente`
* **Entrada de prueba:** *"¿Cómo puedo pedir el reembolso del seguro complementario de salud?"*
* **Salidas obtenidas (JSON estructurado):**
  * **Intento 1:**
    ```json
    {
      "mensaje_respuesta": "Hola. Entiendo que necesites realizar el reembolso de tu seguro complementario de salud. Con gusto te guío en el proceso para que puedas solicitarlo de manera rápida y sencilla.",
      "pasos_a_seguir": [
        "Reúne los documentos necesarios: boleta original de la atención o compra de medicamentos, receta médica (si aplica) y el bono de Isapre o Fonasa bonificado.",
        "Ingresa a la plataforma web de la compañía de seguros o a la app móvil destinada para los beneficios de salud de la empresa.",
        "Selecciona la opción 'Solicitar Reembolso' y completa el formulario con los datos requeridos.",
        "Adjunta las imágenes o archivos PDF legibles de los documentos recopilados y envía la solicitud."
      ],
      "canal_contacto": "beneficios@tuempresa.com o el área de Compensaciones y Beneficios"
    }
    ```
  * **Intento 2 y 3:** Estructura idéntica con claves `mensaje_respuesta`, `pasos_a_seguir` y `canal_contacto` validadas correctamente.

---

## 3. Log de Consola en Crudo

```text
(venv) 📦[nidia@fedora-python proyectoIA]$ python3 -m src.consistencia
Respuesta: {'categoria': 'licencias_medicas', 'urgencia': 'alta', 'requiere_escalamiento_humano': True}
Respuesta: {'categoria': 'licencias_medicas', 'urgencia': 'alta', 'requiere_escalamiento_humano': True}
Respuesta: {'categoria': 'licencias_medicas', 'urgencia': 'alta', 'requiere_escalamiento_humano': True}
clasificar_consulta_rrhh: 3/3 respuestas válidas
Respuesta: {'tipo_tramite': 'vacaciones', 'periodo_o_dias': '5 días hábiles a partir del 15 de noviembre', 'menciona_documento': False}
Respuesta: {'tipo_tramite': 'vacaciones', 'periodo_o_dias': '5 días hábiles a partir del 15 de noviembre', 'menciona_documento': False}
Respuesta: {'tipo_tramite': 'vacaciones', 'periodo_o_dias': '5 días hábiles a partir del 15 de noviembre', 'menciona_documento': False}
extraer_datos_solicitud: 3/3 respuestas válidas
Respuesta: {'mensaje_respuesta': 'Hola. Entiendo que necesites realizar el reembolso de tu seguro complementario de salud. Con gusto te guío en el proceso para que puedas solicitarlo de manera rápida y sencilla.', 'pasos_a_seguir': ['Reúne los documentos necesarios: boleta original de la atención o compra de medicamentos, receta médica (si aplica) y el bono de Isapre o Fonasa bonificado.', 'Ingresa a la plataforma web de la compañía de seguros o a la app móvil destinada para los beneficios de salud de la empresa.', "Selecciona la opción 'Solicitar Reembolso' y completa el formulario con los datos requeridos.", 'Adjunta las imágenes o archivos PDF legibles de los documentos recopilados y envía la solicitud.'], 'canal_contacto': 'beneficios@tuempresa.com o el área de Compensaciones y Beneficios'}
Respuesta: {'mensaje_respuesta': 'Hola. Lamento que hayas tenido gastos médicos, pero con gusto te ayudo a gestionar el reembolso de tu seguro complementario de salud de forma rápida y sencilla.', 'pasos_a_seguir': ['Reúne la boleta o factura original de los gastos médicos y la orden médica.', 'Ingresa al portal web de la compañía de seguros o a nuestra plataforma interna de beneficios.', 'Completa el formulario digital de solicitud de reembolso adjuntando los documentos escaneados.', 'Envía la solicitud y guarda el número de folio para hacer seguimiento.'], 'canal_contacto': 'beneficios@empresa.com'}
Respuesta: {'mensaje_respuesta': 'Hola. Lamento que hayas tenido gastos médicos, pero con gusto te ayudaré a gestionar el reembolso de tu seguro complementario de salud de forma rápida y sencilla.', 'pasos_a_seguir': ['Reúne la boleta o factura original de los gastos médicos y la orden médica correspondiente.', 'Ingresa al portal web de la compañía de seguros o a nuestra plataforma interna de beneficios.', 'Completa el formulario digital de solicitud de reembolso adjuntando los documentos escaneados.', 'Envía la solicitud y guarda el número de folio para hacer el seguimiento.'], 'canal_contacto': 'beneficios@empresa.com'}
generar_respuesta_asistente: 3/3 respuestas válidas
```