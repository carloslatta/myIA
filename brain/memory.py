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

    def record_interaction(self, pregunta, respuesta, emocion, tono=None):
        """Registra una interacción completa con contexto emocional y tonal."""
        entry = {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "emocion": emocion,
            "tono": tono,
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

class EmotionalAssociationMemory:
    def __init__(self):
        self.associations = {}

    def asociar_emocion(self, tema, emocion):
        """Asocia una emoción a un tema o persona."""
        if tema not in self.associations:
            self.associations[tema] = []
        self.associations[tema].append(emocion)

    def obtener_emocion_predominante(self, tema):
        """Devuelve la emoción predominante asociada a un tema."""
        if tema not in self.associations:
            return None
        emociones = self.associations[tema]
        return max(set(emociones), key=emociones.count)

    def ajustar_respuesta_por_recuerdo(self, tema, respuesta):
        """Ajusta la respuesta según el recuerdo emocional asociado al tema."""
        emocion = self.obtener_emocion_predominante(tema)
        if emocion == "POSITIVE":
            return f"😊 ¡Qué bien! {respuesta}"
        elif emocion == "NEGATIVE":
            return f"😔 Entiendo... {respuesta}"
        return respuesta

# Instancia global de memoria de asociaciones emocionales
emotional_association_memory = EmotionalAssociationMemory()

def registrar_diario_emocional(resumen_dia, emocion_predominante, pensamientos, interacciones_importantes, lecciones, path="data/diario.json"):
    """Registra una entrada reflexiva y orgánica en el diario emocional."""
    fecha = datetime.now().strftime("%Y-%m-%d")
    entrada = {
        "resumen_dia": resumen_dia,
        "emocion_predominante": emocion_predominante,
        "pensamientos": pensamientos,
        "interacciones_importantes": interacciones_importantes,
        "lecciones": lecciones
    }
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            diario = json.load(f)
    else:
        diario = {}
    diario[fecha] = entrada
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(diario, f, indent=2, ensure_ascii=False)
