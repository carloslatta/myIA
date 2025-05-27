# llm_manager.py - Gestiona los modelos de lenguaje grandes para mejor comprensión
from transformers import AutoTokenizer, AutoModelForSeq2Seq, pipeline
from .semantic_search import semantic_search
from .self_identity import self_identity
from .emotion_analyzer import emotion_analyzer
from .emotional_memory import emotional_memory
import torch

class LLMManager:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.initialized = False
    
    def initialize(self):
        """Inicializa los modelos LLM"""
        try:
            print("🔄 Cargando modelos LLM...")
            
            # Inicializar búsqueda semántica
            semantic_search.initialize()
            
            # Cargar T5
            self.tokenizers['t5'] = AutoTokenizer.from_pretrained("google/flan-t5-base")
            self.models['t5'] = AutoModelForSeq2Seq.from_pretrained("google/flan-t5-base")
            
            # Pipeline de generación
            self.models['t5_pipeline'] = pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                tokenizer=self.tokenizers['t5'],
                max_length=512
            )
            
            print("✅ Modelos LLM cargados correctamente")
            self.initialized = True
        except Exception as e:
            print(f"❌ Error al cargar los modelos LLM: {e}")
            self.initialized = False
    
    def get_enhanced_response(self, texto, context=None):
        """Obtiene una respuesta mejorada usando los modelos LLM, la identidad de la IA, el análisis de emociones y registra en la memoria emocional."""
        if not self.initialized:
            return None
            
        try:
            # Analizar emoción del texto
            emotion, score = emotion_analyzer.analyze_emotion(texto)
            print(f"🧠 Emoción detectada: {emotion} (confianza: {score})")
            
            # Registrar emoción en la memoria emocional
            emotional_memory.record_emotion(emotion, score, interaction=texto)
            
            # Preparar prompt con identidad, contexto y emoción
            prompt = f"Soy {self_identity.name}, {self_identity.description}.\n"
            if context:
                prompt += f"Contexto previo: {context}\n"
            prompt += f"Emoción detectada: {emotion}\nPregunta: {texto}"
            
            # Generar respuesta con T5
            response = self.models['t5_pipeline'](prompt, max_length=150)[0]['generated_text']
            
            # Verificar calidad semántica
            if semantic_search.initialized:
                similarity = semantic_search.semantic_similarity(texto, response)
                if similarity < 0.5:  # Si la respuesta no es semánticamente relevante
                    return None
            
            return response
        except Exception as e:
            print(f"❌ Error al generar respuesta LLM: {e}")
            return None

# Instancia global del manejador de LLM
llm_manager = LLMManager()