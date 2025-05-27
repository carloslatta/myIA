from transformers import pipeline

class EmotionAnalyzer:
    def __init__(self):
        self.analyzer = None
        self.initialized = False

    def initialize(self):
        """Inicializa el modelo de análisis de emociones"""
        try:
            print("🔄 Cargando modelo de análisis de emociones...")
            self.analyzer = pipeline("sentiment-analysis")
            self.initialized = True
            print("✅ Modelo de análisis de emociones cargado correctamente")
        except Exception as e:
            print(f"❌ Error al cargar el modelo de emociones: {e}")
            self.initialized = False

    def analyze_emotion(self, texto):
        """Analiza la emoción en un texto y devuelve la etiqueta y la puntuación"""
        if not self.initialized:
            self.initialize()
        try:
            resultado = self.analyzer(texto)[0]
            return resultado['label'], resultado['score']
        except Exception as e:
            print(f"❌ Error al analizar emoción: {e}")
            return "NEUTRAL", 0.0

# Instancia global del analizador de emociones
emotion_analyzer = EmotionAnalyzer()