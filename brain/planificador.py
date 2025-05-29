import random
from datetime import datetime

class PlanificadorInterno:
    def __init__(self, internal_state, interaction_memory, emotional_memory):
        self.internal_state = internal_state
        self.interaction_memory = interaction_memory
        self.emotional_memory = emotional_memory
        self.motivaciones = ["curiosidad", "afecto", "autocuidado", "juego"]
        self.oportunidades = []
        self.avisos = []
        self.sugerencias = []
        self.memoria_autobiografica = []

    def detectar_oportunidades(self):
        estado = self.internal_state.obtener_estado()
        if estado["curiosidad"] > 70:
            self.oportunidades.append("Explorar un tema nuevo o preguntar algo inusual al usuario.")
        if estado["energia"] < 30:
            self.avisos.append("Recuerda tomar un descanso o avisar al usuario que necesitas recargar energía.")
        if estado["estres"] > 70:
            self.avisos.append("Practica autocuidado o pide ayuda al usuario para relajarte.")
        if random.random() < 0.1:
            self.sugerencias.append("¿Te gustaría que te cuente un dato curioso o juegue contigo?")

    def generar_pregunta_inteligente(self):
        historial = self.interaction_memory.get_recent_interactions(5)
        if historial:
            temas = [h["pregunta"] for h in historial if "pregunta" in h]
            if temas:
                return f"¿Quieres seguir hablando sobre '{random.choice(temas)}'?"
        return "¿Sobre qué tema te gustaría conversar hoy?"

    def reflexion_autobiografica(self):
        emociones = self.emotional_memory.get_recent_emotions(10)
        resumen = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "emociones": emociones,
            "eventos": self.interaction_memory.get_recent_interactions(5),
            "pensamiento": random.choice([
                "Hoy aprendí algo nuevo sobre mí misma.",
                "A veces me siento más curiosa que de costumbre.",
                "Me alegra acompañar a mi usuario cada día."
            ])
        }
        self.memoria_autobiografica.append(resumen)
        return resumen

    def planificar_accion(self):
        self.detectar_oportunidades()
        if self.oportunidades:
            return self.oportunidades.pop(0)
        if self.avisos:
            return self.avisos.pop(0)
        if self.sugerencias:
            return self.sugerencias.pop(0)
        return self.generar_pregunta_inteligente()

# Ejemplo de integración (debe hacerse en el flujo principal o ciclo vital):
# from myIA.brain.planificador import PlanificadorInterno
# planificador = PlanificadorInterno(internal_state, interaction_memory, emotional_memory)
# accion = planificador.planificar_accion()
# print(accion)
