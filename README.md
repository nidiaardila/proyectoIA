# Asistente de Recursos Humanos y Políticas de Empresa

Aplicación desarrollada por **Nidia Ardila** en el marco de la **Especialización en Desarrollo con IA Generativa (Accenture / Skillnest)**.

* **Perfil de egreso:** Frontend / Producto.
* **Hito de evaluación:** Gate 1 — Habilitación técnica (Módulo 1).
* **Entregable:** Repositorio estructurado, ejecutable y reproducible para consumo funcional de API de modelos fundacionales.

---

## 1. Descripción del Proyecto

Este proyecto implementa la capa base de un asistente conversacional orientado a Recursos Humanos. Su objetivo es resolver consultas frecuentes de colaboradores sobre reglamentos internos, procesos de solicitud de vacaciones, gestión de licencias médicas y asignación de beneficios corporativos.

En este primer hito (**Gate 1**), se establece la infraestructura operativa del cliente:
- Consumo seguro y autenticado hacia la API de Google Gemini sin exponer credenciales.
- Separación de responsabilidades mediante arquitectura modular (`armar_peticion`, `enviar_peticion`, `extraer_texto`, `parsear_respuesta_json`).
- Manejo robusto de errores de red, autenticación (401) y límites de cuota (429).
- Salidas forzadas en formato JSON estructurado mediante esquemas estrictos (`response_schema`).
- Banco de prompts versionado y validado mediante pruebas automatizadas de consistencia.

---

## 2. Requisitos Previos

* **Python:** Versión 3.10 o superior instalada.
* **Git:** Control de versiones configurado.
* **Credenciales:** Clave de API válida de Google Gemini (`GEMINI_API_KEY`).
* **Conexión a internet:** Acceso al endpoint de la API de Gemini.

---

## 3. Instalación y Configuración del Entorno

Sigue estos pasos en la terminal para desplegar el entorno en una máquina limpia:

### 3.1. Clonar el repositorio

Puedes acceder al código fuente en GitHub: [proyectoIA](https://github.com/nidiaardila/proyectoIA)

```bash
git clone https://github.com/nidiaardila/proyectoIA.git
cd proyectoIA
```

### 3.2. Crear y activar el entorno virtual
* **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **En Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### 3.3. Instalar dependencias
Instala las librerías declaradas en el entorno:
```bash
pip install -r requirements.txt
```

### 3.4. Configurar variables de entorno
Copia la plantilla `.env.example` para inicializar el archivo `.env` local:
```bash
cp .env.example .env
```

Abre `.env` en tu editor y define tu clave de API:
```env
GEMINI_API_KEY=tu_api_key_aqui
```

> **Nota de Seguridad (Criterio No Compensable):** El archivo `.env` se encuentra explícitamente excluido del repositorio mediante `.gitignore`. Ninguna clave real ha sido ni debe ser commiteada al historial de Git.

---

## 4. Instrucciones de Ejecución

### 4.1. Validación de Consistencia de Prompts (U1.5)
Para ejecutar la batería de pruebas de consistencia sobre el banco de prompts (3 repeticiones por cada prompt con validación de llaves JSON):
```bash
python3 -m src.consistencia
```
* **Efecto de la ejecución:** Actualiza automáticamente el archivo `prompts/registro_resultados.json`.
* **Respaldo de auditoría:** Los logs completos y el desglose de resultados se encuentran documentados en `docs/respaldo_de_ejecucion_y_consistencia.md`.

### 4.2. Consumo Modular de la API
Para ejecutar el cliente modular de forma directa y verificar el flujo completo de petición y respuesta:
```bash
python3 -m src.consumir_gemini
```

---

## 5. Estructura del Proyecto

```text
proyectoIA/
├── docs/
│   └── respaldo_de_ejecucion_y_consistencia.md      # Registro formal de pruebas de consistencia y logs
├── prompts/
│   ├── banco.py                     # Definición de BANCO_DE_PROMPT y response_schema
│   └── registro_resultados.json     # Métrica automática de éxitos/intentos generada por script
├── src/
│   ├── __init__.py                  # Inicializador del paquete modular
│   ├── consistencia.py              # Script de prueba y evaluación de consistencia
│   └── consumir_gemini.py           # Funciones modulares (armar, enviar, extraer, parsear)
├── .env.example                     # Plantilla pública de variables requeridas
├── .gitignore                       # Filtro de seguridad (ignora .env, venv/, __pycache__/)
├── README.md                        # Documentación técnica y manual de despliegue
└── requirements.txt                 # Lista de dependencias exactas del proyecto
```

---

## 6. Decisiones de Arquitectura y Selección de Modelo

### 6.1. Modelo Seleccionado
* **Modelo:** `gemini-2.5-flash` (o `gemini-1.5-flash`).
* **Justificación técnica:** 
  1. **Latencia y Costo:** Diseñado para tareas operativas de alta velocidad y bajo consumo por request, ideal para interacción en tiempo real en consultas internas de RRHH.
  2. **Compatibilidad Estructurada:** Soporte nativo para `response_schema`, reduciendo la tasa de fallo en el parseo JSON a 0% durante las corridas de validación.

### 6.2. Estrategia de Manejo de Excepciones
El módulo implementa validación defensiva en cada etapa del pipeline:
* **Conectividad y Red:** Captura de fallos en la petición HTTP y códigos de estado HTTP anómalos.
* **Autenticación (401 / 403):** Identificación temprana de variables de entorno faltantes o claves revocadas.
* **Límites de Uso (429):** Manejo de errores de tasa de uso y espaciado preventivo de 1 a 2 segundos entre solicitudes en scripts de lote.
* **Validación de Formato:** Decodificación segura mediante `json.loads` y comprobación de claves mínimas obligatorias antes de entregar la respuesta al sistema.

---

## 7. Registro de Ensayo de Instalación Limpia

En cumplimiento con los estándares de verificación del Bloque 11:
* **Fecha de validación:** Octubre 2026.
* **Entorno de prueba:** Clonación aislada en directorio temporal (`/tmp/prueba-gate1`), creación de `venv` nuevo, instalación directa desde `requirements.txt` y configuración manual de credenciales sobre `.env.example`.
* **Resultado del ensayo:** Ejecución de `python3 -m src.consistencia` exitosa (9/9 pruebas aprobadas, 100% de consistencia) sin requerir dependencias no declaradas ni rutas absolutas.
