import random

class InternalState:
    def __init__(self):
        self.humor = "neutral"
        self.energia = 100
        self.curiosidad = 50
        self.estres = 0

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

    def obtener_estado(self):
        """Devuelve el estado interno actual."""
        return {
            "humor": self.humor,
            "energia": self.energia,
            "curiosidad": self.curiosidad,
            "estres": self.estres
        }

    def ajustar_respuesta_por_estado(self, respuesta):
        """Ajusta el tono de la respuesta según el estado interno."""
        estado = self.obtener_estado()
        if estado['humor'] == 'positivo':
            return f"😊 {respuesta}"
        elif estado['humor'] == 'negativo':
            return f"😔 {respuesta}"
        return respuesta

# Instancia global del estado interno
internal_state = InternalState()