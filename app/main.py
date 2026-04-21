import json
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializar aplicación FastAPI
app = FastAPI(title="Agente de Soporte para Restaurantes")

# Configuración
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "menu.json"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:14b"


class ChatRequest(BaseModel):
    """Esquema de solicitud para el endpoint de chat."""
    question: str


def load_menu_data() -> str:
    """
    Carga el archivo JSON con menú, horarios, políticas y alergenos.
    Retorna el contenido como string.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró {DATA_PATH}")
    
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return f.read()


@app.post("/chat")
def chat_endpoint(payload: ChatRequest) -> dict:
    """
    Endpoint POST que recibe una pregunta y devuelve respuesta de Ollama.
    Contexto inyectado: contenido de menu.json.
    """
    # Cargar contexto del menú
    try:
        menu_text = load_menu_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # System prompt estricto
    system_prompt = (
        "Sos un asistente de restaurante. Respondé SOLO con información del menú. "
        "Si no está en el menú, respondé: 'No tengo esa info cargada, te recomiendo consultar con el personal.' "
        "Nunca inventés precios ni platos."
    )

    # Construir prompt con contexto
    prompt = (
        f"{system_prompt}\n\n"
        "Aquí está la información del restaurante en JSON:\n\n"
        f"{menu_text}\n\n"
        f"Pregunta del cliente: {payload.question}\n"
        "Respuesta:"
    )

    # Configurar solicitud a Ollama
    request_body = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 256,
        },
    }

    # Llamar a Ollama
    try:
        response = requests.post(OLLAMA_URL, json=request_body, timeout=30)
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error conectando con Ollama: {exc}"
        ) from exc

    # Validar respuesta HTTP
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama error {response.status_code}: {response.text}"
        )

    # Extraer respuesta del modelo
    try:
        data = response.json()
        answer = data.get("response", "").strip()
        if not answer:
            raise ValueError("Campo 'response' vacío en respuesta de Ollama")
    except (ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Formato inválido en respuesta de Ollama: {exc}"
        ) from exc

    return {"answer": answer}
