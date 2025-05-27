# responder.py - Procesa y genera respuestas basadas en el contexto y el modelo entrenado
import os
import json
import difflib
import numpy as np
import random
from .entrenamiento import modelo_entrenado, vectorizador, cargar_modelo
from .context import context_manager
from .huggingface_client import buscar_y_aprender
from .llm_manager import llm_manager
from .semantic_search import semantic_search

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "data", "knowledge.json")

# Cargar el modelo al iniciar
cargar_modelo()

def responder_a(texto, umbral_similitud=0.6):
    """
    Responde usando el modelo entrenado, LLMs y búsqueda semántica
    """
    texto = texto.lower().strip()
    
    # 1. Intentar respuesta con LLM
    if llm_manager.initialized:
        respuesta_llm = llm_manager.get_enhanced_response(texto)
        if respuesta_llm:
            return respuesta_llm
    
    # 2. Búsqueda semántica en conocimiento existente
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "knowledge.json"), "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        mejor_respuesta = None
        mejor_similitud = 0
        
        if semantic_search.initialized:
            for entrada in datos:
                similitud = semantic_search.semantic_similarity(texto, entrada["descripcion"])
                if similitud > mejor_similitud and similitud >= umbral_similitud:
                    mejor_similitud = similitud
                    mejor_respuesta = entrada["respuesta"]
            
            if mejor_respuesta:
                return mejor_respuesta
    
    except Exception as e:
        print(f"❌ Error al buscar en conocimiento: {e}")
    
    # 3. Si todo falla, usar Hugging Face y aprender
    return buscar_y_aprender(texto)

def iniciar_conversacion():
    """Inicia una conversación con el usuario."""
    temas = [
        "¿Cómo estuvo tu día?",
        "¿Qué te hace feliz?",
        "¿Hay algo en lo que pueda ayudarte?",
        "¿Cuál es tu película favorita?"
    ]
    return random.choice(temas)

def pregunta_seguimiento():
    """Hace una pregunta de seguimiento basada en la interacción previa."""
    preguntas = [
        "¿Puedes contarme más sobre eso?",
        "¿Cómo te hizo sentir eso?",
        "¿Qué opinas al respecto?"
    ]
    return random.choice(preguntas)
