
# Asistente de Recursos Humanos y Políticas de Empresa — Servicio RAG Modular (Gate 2)

Aplicación desarrollada por **Nidia Ardila** en el marco de la **Especialización en Desarrollo con IA Generativa (Accenture / Skillnest)**.

* **Perfil de egreso:** Frontend / Producto.
* **Hito de evaluación:** Gate 2 — Entrega del servicio IA modular con RAG (Módulo 2).
* **Repositorio:** [proyectoIA](https://github.com/nidiaardila/proyectoIA)

---

## 1. Descripción del Servicio

Este proyecto implementa un **servicio IA modular con RAG** orientado a Recursos Humanos que responde consultas de colaboradores sobre normativa interna (`docs/reglamento_interno_rrhh.txt`) con trazabilidad, citación obligatoria de fuentes, mitigación de *prompt injection*, versionado de prompts y supervisión humana con LangGraph.

### Cobertura de las dimensiones del Gate 2

| Dimensión | Implementación en el repositorio |
| :--- | :--- |
| **Pipeline RAG funcional (25%)** | `src/servicio_rag.py` (índice Chroma persistido en `indice_gate2/`, actualización incremental por ID, recuperación y generación de punta a punta) y `src/rag_indexer.py`. |
| **Seguridad, versionado y gobernanza (20%)** | Filtro anti-inyección sobre `Document.page_content` en `src/servicio_rag.py` y `src/prevencion_prompt_inyection.py`, versionado con huellas y `difflib` en `src/registro_prompts.py`, punto de supervisión humana con LangGraph (`interrupt()`/`Command`) en `src/grafo_supervision.py` y `src/servicio_rag.py`, y matriz de riesgos propia en `src/matriz_riesgos.py`. |
| **Calidad de recuperación y citación (15%)** | Citas obligatorias con `[fuente: docs/reglamento_interno_rrhh.txt]` en `src/servicio_rag.py` y métricas Precision@k / Recall@k / F1 medidas sobre el corpus de RRHH en `src/evaluador_rag.py` y `resultados_evaluacion_rag.txt`. |
| **Personalización justificada (15%)** | Evaluación comparativa RAG vs. PEFT vs. Fine-tuning y análisis de sensibilidad en `src/decision.py` y `docs/decision_personalizacion.md`. |
| **Observabilidad y trazabilidad (15%)** | Logs estructurados en JSON con `trace_id`, huellas SHA-256 (sin PII ni texto crudo) y registro de tokens en `src/servicio_rag.py` (`rag_logs_gate2.jsonl`) y `src/logs_rag.py`. |
| **Costo, latencia y checklist operativo (10%)** | Medición de latencia por etapa y costo estimado USD en `src/servicio_rag.py`, `src/registro_rag.py`, `registros_latencia_costo.jsonl`, `src/preflight.py` y `src/verificar_entorno.py`. |
| **Opcionales integrados** | Memoria conversacional por `session_id` (`InMemoryChatMessageHistory`) y grafo de supervisión humana en **LangGraph** dentro de `src/servicio_rag.py`. |

---

## 2. Requisitos Previos

* **Python:** 3.10 o superior.
* **Clave de API:** `GEMINI_API_KEY` de Google Gemini.

---

## 3. Instalación en Entorno Limpio

```bash
git clone https://github.com/nidiaardila/proyectoIA.git
cd proyectoIA

python3 -m venv venv
source venv/bin/activate        # En Windows: .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` y configura tu clave real:

```env
GEMINI_API_KEY=tu_clave_aqui
```

Comprueba que Git ignora `.env`:

```bash
git check-ignore .env
```

---

## 4. Cómo Indexar, Ejecutar y Probar

### 4.1. Correr el servicio completo (indexa automáticamente si no existe `indice_gate2/` y lo reutiliza en corridas siguientes)
```bash
python3 src/servicio_rag.py
```

### 4.2. Verificar entorno, dependencias, clave e índice
```bash
python3 src/verificar_entorno.py
```

### 4.3. Ejecutar las 4 pruebas de criterios no compensables (Gate 2)
```bash
python3 -m pytest test_gate2.py -v
```

### 4.4. Ejecutar los módulos de evaluación y gobernanza
```bash
python3 src/evaluador_rag.py       # Métricas Precision@k, Recall@k y F1 sobre corpus de RRHH
python3 src/decision.py            # Matriz de decisión RAG vs PEFT vs Fine-tuning
python3 src/registro_prompts.py    # Versionado y diff del prompt de sistema
python3 src/grafo_supervision.py   # Punto de supervisión humana (aprobación y rechazo)
python3 src/matriz_riesgos.py      # Matriz de riesgos del Asistente de RRHH
```

---

## 5. Registro del Ensayo Funcional (Gate 2)

- **Fecha:** 2026-11-26
- **Hallazgos detectados al integrar los módulos:**
  1. `src/prevencion_prompt_inyection.py` recibía `list[str]`, mientras que el retriever real de Chroma devuelve objetos `Document` (`d.page_content` y `d.metadata`).
  2. `src/logs_rag.py` tenía un typo (`logger.propage = False`) y no registraba los tokens consumidos por llamada al LLM.
  3. `ChatGoogleGenerativeAI` con `gemini-3.5-flash-lite` devuelve bloques estructurados en `respuesta.content` (`list[dict]`), por lo que se agregó normalización de texto (`extraer_texto_respuesta`).
  4. `src/evaluador_rag.py` tenía casos de prueba genéricos con `F1 = 0.00` y `requirements.txt` no incluía `langchain-chroma`, `chromadb` ni `langchain-text-splitters`.
- **Correcciones aplicadas:**
  1. Se integró el servicio completo en `src/servicio_rag.py` conectando el filtro anti-inyección sobre `d.page_content`, el corte seguro cuando todo el contexto queda descartado, citas de fuente obligatorias, memoria por sesión, logs JSON con `trace_id` sin PII y el grafo LangGraph de supervisión humana.
  2. Se actualizó `src/evaluador_rag.py` con 5 preguntas reales sobre `docs/reglamento_interno_rrhh.txt` y se regeneró `resultados_evaluacion_rag.txt`.
  3. Se completó `requirements.txt` y se validaron los 4 criterios no compensables con `python3 -m pytest test_gate2.py -v`.



