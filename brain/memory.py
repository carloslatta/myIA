# memory.py - Gestiona el almacenamiento y recuperación de conocimientos de la IA
from datetime import datetime
import os
import json

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_PATH = os.path.join(DATA_DIR, "log.txt")
KNOWLEDGE_PATH = os.path.join(DATA_DIR, "knowledge.json")

# Crear carpeta si no existe
os.makedirs(DATA_DIR, exist_ok=True)

# Crear archivos si no existen
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("=== Registro de aprendizajes ===\n")

if not os.path.exists(KNOWLEDGE_PATH):
    with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)

def guardar_aprendizaje(estímulo, descripcion, tags=None, respuesta=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar en log.txt (histórico)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ({estímulo.upper()}) {descripcion}\n")

    # Guardar en knowledge.json (memoria estructurada)
    nuevo_aprendizaje = {
        "fecha": timestamp,
        "estimulo": estímulo,
        "descripcion": descripcion,
        "tags": tags or [],
        "respuesta": respuesta or ""
    }

    with open(KNOWLEDGE_PATH, "r+", encoding="utf-8") as f:
        datos = json.load(f)
        datos.append(nuevo_aprendizaje)
        f.seek(0)
        f.truncate()
        json.dump(datos, f, indent=2, ensure_ascii=False)

    print("🧠 Guardado:", descripcion)

import json
from datetime import datetime

class InteractionMemory:
    def __init__(self, path="data/interacciones.json"):
        self.path = path
        self.interactions = []
        self.load_interactions()

    def record_interaction(self, pregunta, respuesta, emocion):
        """Registra una interacción completa."""
        entry = {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "emocion": emocion,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.interactions.append(entry)
        self.save_interactions()

    def save_interactions(self):
        """Guarda las interacciones en un archivo JSON."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.interactions, f, indent=2)

    def load_interactions(self):
        """Carga las interacciones desde un archivo JSON."""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.interactions = json.load(f)

# Instancia global de memoria de interacciones
interaction_memory = InteractionMemory()
