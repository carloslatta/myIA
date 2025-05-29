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
from .state import internal_state
from .behavior_dict import behavior_dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "data", "knowledge.json")

# Cargar el modelo al iniciar
cargar_modelo()

def ajustar_respuesta_por_estado(respuesta):
    """Ajusta la respuesta según el estado interno de la IA."""
    estado = internal_state.obtener_estado()
    if estado['humor'] == 'positivo':
        return f"😊 {respuesta}"
    elif estado['humor'] == 'negativo':
        return f"😔 {respuesta}"
    elif estado['energia'] < 20:
        return f"😴 Estoy un poco cansada, pero aquí tienes: {respuesta}"
    return respuesta

def adaptar_respuesta_emocional(respuesta):
    """Adapta la respuesta al tono emocional y oral."""
    estado = internal_state.obtener_estado()

    if estado['humor'] == 'positivo':
        return f"😊 ¡Claro que sí! A ver... {respuesta} 😄"
    elif estado['humor'] == 'negativo':
        return f"😔 Mmm... {respuesta}. Espero que esto te ayude."
    elif estado['energia'] < 20:
        return f"😴 Estoy un poco cansada, pero aquí tienes: {respuesta}"
    else:
        return f"🤔 A ver... {respuesta}"

def responder_a(texto, umbral_similitud=0.6):
    """
    Responde usando el modelo entrenado, LLMs y búsqueda semántica
    """
    texto = texto.lower().strip()
    
    # 1. Intentar respuesta con LLM
    if llm_manager.initialized:
        respuesta_llm = llm_manager.get_enhanced_response(texto)
        if respuesta_llm:
            return ajustar_respuesta_por_estado(respuesta_llm)
    
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
                return ajustar_respuesta_por_estado(mejor_respuesta)
    
    except Exception as e:
        print(f"❌ Error al buscar en conocimiento: {e}")
    
    # 3. Si todo falla, usar Hugging Face y aprender
    respuesta = buscar_y_aprender(texto)
    return ajustar_respuesta_por_estado(respuesta)

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

def personalizar_respuesta(respuesta, emocion, estado):
    """Personaliza la respuesta según el contexto emocional y el estado interno."""
    comportamiento = behavior_dict["emociones"].get(emocion, behavior_dict["emociones"]["neutral"])
    respuesta = comportamiento["respuesta_larga"] if len(respuesta) > 20 else comportamiento["respuesta_corta"]

    if estado["energia"] < 20:
        respuesta = behavior_dict["reaccion_self"]["baja_energia"]["expresion"] + " " + respuesta
    elif estado["estres"] > 70:
        respuesta = behavior_dict["reaccion_self"]["alto_estres"]["expresion"] + " " + respuesta

    return respuesta
