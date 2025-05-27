import json
import os
from datetime import datetime

class EmotionalMemory:
    def __init__(self, path="data/emotional_memory.json"):
        self.path = path
        self.memory = []
        self.load_memory()

    def record_emotion(self, emotion, score, interaction):
        """Registra una emoción detectada junto con la interacción."""
        entry = {
            "emotion": emotion,
            "score": score,
            "interaction": interaction,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.memory.append(entry)
        self.save_memory()

    def get_recent_emotions(self, limit=5):
        """Devuelve las emociones más recientes registradas."""
        return self.memory[-limit:]

    def save_memory(self):
        """Guarda la memoria emocional en un archivo JSON."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def load_memory(self):
        """Carga la memoria emocional desde un archivo JSON."""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.memory = json.load(f)

# Instancia global de memoria emocional
emotional_memory = EmotionalMemory()