import os
import requests
from dotenv import load_dotenv
from .entrenamiento import entrenar_modelo  # Cambiado a importación relativa
import json
from datetime import datetime

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("⚠️ No se encontró el token de Hugging Face. Verifica tu archivo .env.")
    exit(1)  # Salir si no hay token configurado

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

KNOWLEDGE_PATH = "knowledge.json"

def consulta_huggingface(texto):
    payload = {"inputs": texto}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error al consultar Hugging Face: {response.status_code}"

def buscar_y_aprender(texto):
    """
    Consulta Hugging Face si no hay respuesta, guarda la nueva respuesta y reentrenar el modelo.
    Si Hugging Face no responde, pregunta al usuario directamente.
    """
    # Consultar Hugging Face
    print("🔍 Consultando Hugging Face...")
    respuesta_hf = consulta_huggingface(texto)

    if isinstance(respuesta_hf, list) and len(respuesta_hf) > 0:
        nueva_respuesta = respuesta_hf[0].get("generated_text", "").strip()
        if nueva_respuesta:
            print(f"🤖 Respuesta de Hugging Face: {nueva_respuesta}")
        else:
            print("❌ Respuesta vacía de Hugging Face.")
    else:
        print("❌ No se pudo obtener una respuesta válida de Hugging Face.")
        nueva_respuesta = None

    # Si no hay respuesta válida, preguntar al usuario
    if not nueva_respuesta:
        nueva_respuesta = input(f"🤔 No sé la respuesta a '{texto}'. ¿Qué debería responder? ").strip()

    # Guardar en knowledge.json
    nuevo_conocimiento = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": texto,
        "contexto": "aprendido",
        "tags": ["huggingface", "aprendido"],
        "respuesta": nueva_respuesta
    }

    try:
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        datos = []

    datos.append(nuevo_conocimiento)

    with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

    print("✅ Aprendí algo nuevo")

    # Reentrenar el modelo
    print("🔄 Reentrenando modelo...")
    entrenar_modelo()

    return nueva_respuesta
