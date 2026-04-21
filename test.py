"""
Script de prueba para el Agente de Soporte para Restaurantes.
Ejecuta 3 preguntas reales contra FastAPI.
Requiere: servidor FastAPI corriendo en http://localhost:8000
"""

import requests

# URL del endpoint
BASE_URL = "http://localhost:8000/chat"

# Preguntas de ejemplo sobre el menú
QUESTIONS = [
    "¿Cuál es el precio del bife de chorizo y qué acompañamientos trae?",
    "¿Tiene opciones sin gluten? Listime los platos.",
    "¿A qué hora atienden los domingos y qué políticas tienen sobre cambios de pedido?"
]


def test_agent() -> None:
    """Envía 3 preguntas al agente y imprime respuestas."""
    print("=" * 70)
    print("Agente de Soporte para Restaurantes (Local con Ollama)")
    print("=" * 70)
    print(f"Conectando a: {BASE_URL}\n")
    
    for idx, question in enumerate(QUESTIONS, 1):
        try:
            # Enviar pregunta al endpoint
            response = requests.post(
                BASE_URL,
                json={"question": question},
                timeout=30
            )
            response.raise_for_status()
            
            # Extraer respuesta
            result = response.json()
            answer = result.get("answer", "Sin respuesta")
            
        except requests.exceptions.ConnectionError:
            answer = "Error: No se puede conectar. ¿Está corriendo FastAPI en puerto 8000?"
        except requests.exceptions.Timeout:
            answer = "Error: La solicitud tardó demasiado (timeout 30s)"
        except requests.exceptions.RequestException as exc:
            answer = f"Error HTTP: {exc}"
        
        # Mostrar pregunta y respuesta
        print(f"[Pregunta {idx}]")
        print(f"{question}\n")
        print(f"[Respuesta {idx}]")
        print(f"{answer}\n")
        print("-" * 70 + "\n")


if __name__ == "__main__":
    test_agent()
