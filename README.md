# Agente de Soporte para Restaurantes

## Problema → Solución → ROI

**Problema**: Restaurantes pierden clientes por no tener respuestas rápidas a preguntas sobre menú, horarios y políticas. Las soluciones existentes requieren APIs pagas, datos en la nube, o conexión a internet.

**Solución**: Agente IA local que responde preguntas en tiempo real usando solo un archivo JSON estático, corriendo en tu servidor con Ollama.

**ROI**: Costo ~0 para funcionar, respuestas automáticas 24/7, datos 100% privados, sin dependencias de terceros.

---

## Arquitectura

```
Entrada: Pregunta del cliente
  ↓
Sistema FastAPI (puerto 8000)
  ↓
Carga menu.json (contexto)
  ↓
Inyecta en prompt estricto ("solo responde con datos del menú")
  ↓
Llamada a Ollama local (http://localhost:11434)
  ↓
Salida: Respuesta generada por qwen2.5-coder:14b
```

---

## Requisitos

- **Python** 3.10+
- **Ollama** instalado localmente (https://ollama.ai)
- **Modelo**: `qwen2.5-coder:14b` descargado en Ollama
- **Memoria**: ~8GB RAM recomendado

---

## Setup Rápido

### 1. Preparar entorno Python

```bash
# Crear virtualenv
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate
# Activar (macOS/Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Instalar y ejecutar Ollama

```bash
# Descargar modelo (ejecutar UNA SOLA VEZ)
ollama pull qwen2.5-coder:14b

# Iniciar servidor Ollama en background
ollama serve
```

Ollama estará disponible en `http://localhost:11434`

### 3. Ejecutar aplicación FastAPI

```bash
uvicorn app.main:app --reload
```

La API estará en `http://localhost:8000`

---

## Pruebas

### Opción A: Script automático (3 preguntas)
```bash
python test.py
```

### Opción B: cURL manual
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuál es el precio del bife de chorizo?"}'
```

### Opción C: Swagger intereactivo
Abre en navegador: `http://localhost:8000/docs`

---

## Estructura de Archivos

| Archivo | Propósito |
|---------|-----------|
| `app/main.py` | FastAPI con endpoint `/chat` |
| `data/menu.json` | Menú, horarios, políticas, alergenos |
| `test.py` | Script con 3 preguntas de prueba |
| `requirements.txt` | Dependencias pip |

---

## Customización

### Cambiar el menú
Edita `data/menu.json`. El agente automáticamente usará los nuevos datos en la próxima pregunta.

### Cambiar el modelo Ollama
En `app/main.py`, modifica:
```python
MODEL_NAME = "otro-modelo:version"
```

### Ajustar precisión de respuestas
En `app/main.py`:
- `temperature: 0.2` → más bajo = más determinístico
- `num_predict: 256` → máximo tokens en respuesta

---

## Deployment

### Local (desarrollo)
```bash
uvicorn app.main:app --reload
```

### Producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

---

## Format de Endpoint

**POST** `/chat`

**Request**:
```json
{
  "question": "¿Qué platos sin gluten tienen?"
}
```

**Response**:
```json
{
  "answer": "Tenemos Ensalada Verde, Fruta de Estación..."
}
```

---

## Troubleshooting

| Error | Solución |
|-------|----------|
| `ConnectionError: http://localhost:11434` | Ollama no está corriendo. Ejecuta `ollama serve` |
| `FileNotFoundError: menu.json` | Verifica que `data/menu.json` exista con datos válidos |
| `Timeout 30s` | Modelo lento. Aumenta timeout o usa máquina más potente |
| No encuentra respuesta | System prompt es restrictivo. Revisa que la pregunta tenga respuesta en `menu.json` |

---

## Próximos Pasos (si escalas)

- [ ] Base de datos para histórico de preguntas
- [ ] Embeddings + búsqueda semántica en menú
- [ ] Endpoint adicional para actualizar menú
- [ ] Rate limiting y autenticación
- [ ] Logging y métricas de uso
- [ ] Integración con WhatsApp/Telegram/email

---

**Versión**: 1.0 | **Estado**: MVP | **Última actualización**: 2026-04-20
