# context.py - Maneja el contexto y el historial de las conversaciones
from collections import deque
from datetime import datetime

class ContextManager:
    def __init__(self, max_history=5):
        self.conversation_history = deque(maxlen=max_history)
        self.current_context = {}
        
    def add_to_history(self, texto, respuesta):
        """Agrega una interacción a la historia de la conversación"""
        self.conversation_history.append({
            'texto': texto,
            'respuesta': respuesta,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def update_context(self, texto, tags=None):
        """Actualiza el contexto basado en la entrada actual"""
        if not tags:
            tags = []
        
        # Actualizar contexto basado en palabras clave
        keywords = {
            'personal': ['tu', 'nombre', 'eres', 'quien'],
            'emocional': ['sientes', 'feliz', 'triste', 'enojado'],
            'conocimiento': ['sabes', 'conoces', 'explica', 'que es'],
            'acción': ['puedes', 'hacer', 'ayuda']
        }
        
        texto_lower = texto.lower()
        for context_type, words in keywords.items():
            if any(word in texto_lower for word in words):
                self.current_context['tipo'] = context_type
                
        self.current_context['tags'] = tags
        
    def get_context(self):
        """Obtiene el contexto actual de la conversación"""
        return {
            'history': list(self.conversation_history),
            'current': self.current_context
        }
    
    def clear_context(self):
        """Limpia el contexto actual"""
        self.current_context = {}
        self.conversation_history.clear()

# Instancia global del manejador de contexto
context_manager = ContextManager()