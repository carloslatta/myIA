import json
from datetime import datetime
import os

class EvolutionTracker:
    def __init__(self, path="data/evolucion.json"):
        self.path = path
        self.hitos = []
        self.load_hitos()

    def registrar_hito(self, hito):
        """Registra un hito importante en la evolución de la IA."""
        entry = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hito": hito
        }
        self.hitos.append(entry)
        self.save_hitos()

    def save_hitos(self):
        """Guarda los hitos en un archivo JSON."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.hitos, f, indent=2)

    def load_hitos(self):
        """Carga los hitos desde un archivo JSON."""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.hitos = json.load(f)

# Instancia global del rastreador de evolución
evolution_tracker = EvolutionTracker()