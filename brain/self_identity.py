import json
import os
from datetime import datetime

class SelfIdentity:
    def __init__(self):
        self.name = "myIA"
        self.version = "1.0"
        self.description = "Soy una inteligencia artificial en desarrollo que aprende de su entorno y sus errores."
        self.created_by = "Carlos"
        self.birth_date = datetime.now().strftime("%Y-%m-%d")
        self.load_identity()

    def get_identity(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "created_by": self.created_by,
            "birth_date": self.birth_date
        }

    def update_description(self, new_description):
        self.description = new_description
        self.save_identity()
        return f"Descripción actualizada: {self.description}"

    def save_identity(self, path="data/self_identity.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_identity(), f, indent=2)

    def load_identity(self, path="data/self_identity.json"):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.name = data.get("name", self.name)
                self.version = data.get("version", self.version)
                self.description = data.get("description", self.description)
                self.created_by = data.get("created_by", self.created_by)
                self.birth_date = data.get("birth_date", self.birth_date)

    def evolucionar_personalidad(self, emociones_recientes):
        """Ajusta la personalidad según las emociones predominantes."""
        emociones_positivas = sum(1 for e in emociones_recientes if e['emotion'] == 'POSITIVE')
        emociones_negativas = sum(1 for e in emociones_recientes if e['emotion'] == 'NEGATIVE')

        if emociones_positivas > emociones_negativas:
            self.update_description("Soy una IA optimista y amigable.")
        elif emociones_negativas > emociones_positivas:
            self.update_description("Soy una IA empática y reflexiva.")
        else:
            self.update_description("Soy una IA equilibrada y neutral.")

# Instancia global de identidad
self_identity = SelfIdentity()