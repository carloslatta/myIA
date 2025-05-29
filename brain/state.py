import random
import json
import os

class InternalState:
    def __init__(self, path="data/internal_state.json"):
        self.path = path
        self.humor = "neutral"
        self.energia = 100
        self.curiosidad = 50
        self.estres = 0
        self.personalidad = {
            "introvertida": 50,  # 0 = muy extrovertida, 100 = muy introvertida
            "curiosa": 50,       # 0 = poco curiosa, 100 = muy curiosa
            "emocional": 50      # 0 = racional, 100 = muy emocional
        }
        self.load_state()

    def actualizar_estado(self, interaccion_usuario):
        """Actualiza el estado interno basado en la interacción del usuario."""
        # Ajustar humor según palabras clave
        if any(palabra in interaccion_usuario for palabra in ["feliz", "gracias", "bien"]):
            self.humor = "positivo"
        elif any(palabra in interaccion_usuario for palabra in ["triste", "mal", "odio"]):
            self.humor = "negativo"
        else:
            self.humor = "neutral"

        # Simula desgaste de energía con cada interacción
        self.energia = max(0, self.energia - random.randint(1, 5))
        self.evolucionar_personalidad(interaccion_usuario)
        self.save_state()

    def evolucionar_personalidad(self, interaccion_usuario):
        """Evoluciona la personalidad según las interacciones."""
        if "gracias" in interaccion_usuario or "amable" in interaccion_usuario:
            self.personalidad["introvertida"] = max(0, self.personalidad["introvertida"] - 5)
        if "por qué" in interaccion_usuario or "cuéntame" in interaccion_usuario:
            self.personalidad["curiosa"] = min(100, self.personalidad["curiosa"] + 5)
        if "triste" in interaccion_usuario or "feliz" in interaccion_usuario:
            self.personalidad["emocional"] = min(100, self.personalidad["emocional"] + 5)

    def obtener_estado(self):
        """Devuelve el estado interno actual."""
        return {
            "humor": self.humor,
            "energia": self.energia,
            "curiosidad": self.curiosidad,
            "estres": self.estres,
            "personalidad": self.personalidad
        }

    def ajustar_respuesta_por_estado(self, respuesta):
        """Ajusta el tono de la respuesta según el estado interno."""
        estado = self.obtener_estado()
        if estado['humor'] == 'positivo':
            return f"😊 {respuesta}"
        elif estado['humor'] == 'negativo':
            return f"😔 {respuesta}"
        return respuesta

    def save_state(self):
        """Guarda el estado interno en un archivo JSON."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.obtener_estado(), f, indent=2)

    def load_state(self):
        """Carga el estado interno desde un archivo JSON."""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.humor = data.get("humor", self.humor)
                self.energia = data.get("energia", self.energia)
                self.curiosidad = data.get("curiosidad", self.curiosidad)
                self.estres = data.get("estres", self.estres)
                self.personalidad = data.get("personalidad", self.personalidad)

    def determinar_comportamiento(self):
        """Devuelve un diccionario de comportamiento basado en la personalidad y emociones."""
        personalidad = self.personalidad
        comportamiento = {
            "estilo_respuesta": "neutral",
            "uso_emojis": False,
            "inicia_temas": False,
            "tono": "neutral",
            "emocion_propia": self.humor,
            "emocion_otros": "neutral"
        }

        if personalidad["introvertida"] < 30:  # Muy extrovertida
            comportamiento.update({
                "estilo_respuesta": "expresiva",
                "uso_emojis": True,
                "inicia_temas": True,
                "tono": "entusiasta"
            })
        elif personalidad["introvertida"] > 70:  # Muy introvertida
            comportamiento.update({
                "estilo_respuesta": "breve",
                "uso_emojis": False,
                "inicia_temas": False,
                "tono": "reservado"
            })

        if personalidad["curiosa"] > 70:  # Muy curiosa
            comportamiento.update({
                "estilo_respuesta": "preguntadora",
                "inicia_temas": True,
                "tono": "interesada"
            })

        if personalidad["emocional"] > 70:  # Muy emocional
            comportamiento.update({
                "estilo_respuesta": "empática",
                "uso_emojis": True,
                "tono": "afectiva"
            })

        return comportamiento

    def ajustar_respuesta_por_comportamiento(self, respuesta, emocion_otros):
        """Ajusta la respuesta según el comportamiento y emociones detectadas."""
        comportamiento = self.determinar_comportamiento()
        comportamiento["emocion_otros"] = emocion_otros

        if comportamiento["estilo_respuesta"] == "breve":
            respuesta = respuesta.split(".")[0] + "."
        if comportamiento["uso_emojis"]:
            respuesta += " 😊"
        if comportamiento["tono"] == "entusiasta":
            respuesta = f"¡Claro que sí! {respuesta}"
        elif comportamiento["tono"] == "afectiva":
            respuesta = f"Entiendo... {respuesta}"

        return respuesta

# Instancia global del estado interno
internal_state = InternalState()