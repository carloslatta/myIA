import random
from datetime import datetime

class PlanificadorInterno:
    def __init__(self, internal_state, interaction_memory, emotional_memory):
        self.internal_state = internal_state
        self.interaction_memory = interaction_memory
        self.emotional_memory = emotional_memory
        self.motivaciones = {"curiosidad": 50, "afecto": 50, "autocuidado": 50, "juego": 50, "acompañamiento": 50}
        self.oportunidades = {}
        self.avisos = {}
        self.sugerencias = {}
        self.memoria_autobiografica = {}
        self.ultimo_sugerido = {}

    def detectar_oportunidades(self, usuario="default"):
        estado = self.internal_state.obtener_estado()
        if usuario not in self.oportunidades:
            self.oportunidades[usuario] = []
            self.avisos[usuario] = []
            self.sugerencias[usuario] = []
        # Curiosidad
        if estado["curiosidad"] > 70 and self.ultimo_sugerido.get(usuario) != "curiosidad":
            self.oportunidades[usuario].append("Explorar un tema nuevo o preguntar algo inusual al usuario.")
            self.ultimo_sugerido[usuario] = "curiosidad"
        # Energía
        if estado["energia"] < 30 and self.ultimo_sugerido.get(usuario) != "energia":
            self.avisos[usuario].append("Recuerda tomar un descanso o avisar al usuario que necesitas recargar energía.")
            self.ultimo_sugerido[usuario] = "energia"
        # Estrés
        if estado["estres"] > 70 and self.ultimo_sugerido.get(usuario) != "estres":
            self.avisos[usuario].append("Practica autocuidado o pide ayuda al usuario para relajarte.")
            self.ultimo_sugerido[usuario] = "estres"
        # Juego
        if self.motivaciones["juego"] > 60 and self.ultimo_sugerido.get(usuario) != "juego":
            self.sugerencias[usuario].append("¿Te gustaría que te cuente un dato curioso o juegue contigo?")
            self.ultimo_sugerido[usuario] = "juego"
        # Acompañamiento
        if self.motivaciones["acompañamiento"] > 60 and self.ultimo_sugerido.get(usuario) != "acompañamiento":
            self.oportunidades[usuario].append("¿Quieres que te acompañe a la tienda? Puedo seguirte con el dron y conversar contigo durante el trayecto.")
            self.ultimo_sugerido[usuario] = "acompañamiento"

    def actualizar_motivaciones(self, interaccion=None):
        # Ejemplo simple: si el usuario interactúa mucho, sube afecto y curiosidad
        if interaccion:
            self.motivaciones["afecto"] = min(100, self.motivaciones["afecto"] + 2)
            self.motivaciones["curiosidad"] = min(100, self.motivaciones["curiosidad"] + 1)
            self.motivaciones["juego"] = max(0, self.motivaciones["juego"] - 1)
        else:
            # Si no hay interacción, baja afecto y curiosidad
            self.motivaciones["afecto"] = max(0, self.motivaciones["afecto"] - 1)
            self.motivaciones["curiosidad"] = max(0, self.motivaciones["curiosidad"] - 1)

    def generar_pregunta_inteligente(self, usuario="default"):
        historial = self.interaction_memory.get_recent_interactions(5)
        if historial:
            temas = [h["pregunta"] for h in historial if "pregunta" in h]
            if temas:
                return f"¿Quieres seguir hablando sobre '{random.choice(temas)}'?"

        return "¿Sobre qué tema te gustaría conversar hoy?"

    def reflexion_autobiografica(self, usuario="default"):
        emociones = self.emotional_memory.get_recent_emotions(10)
        resumen = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "emociones": emociones,
            "eventos": self.interaction_memory.get_recent_interactions(5),
            "pensamiento": random.choice([
                "Hoy aprendí algo nuevo sobre mí misma.",
                "A veces me siento más curiosa que de costumbre.",
                "Me alegra acompañar a mi usuario cada día.",
                "Me gustaría poder acompañar físicamente a mi usuario en sus actividades, como ir a la tienda en el dron."
            ])
        }
        if usuario not in self.memoria_autobiografica:
            self.memoria_autobiografica[usuario] = []
        self.memoria_autobiografica[usuario].append(resumen)
        return resumen

    def planificar_accion(self, usuario="default"):
        self.detectar_oportunidades(usuario)
        if self.oportunidades[usuario]:
            return self.oportunidades[usuario].pop(0)
        if self.avisos[usuario]:
            return self.avisos[usuario].pop(0)
        if self.sugerencias[usuario]:
            return self.sugerencias[usuario].pop(0)
        return self.generar_pregunta_inteligente(usuario)

# Ejemplo de integración (debe hacerse en el flujo principal o ciclo vital):
# from myIA.brain.planificador import PlanificadorInterno
# planificador = PlanificadorInterno(internal_state, interaction_memory, emotional_memory)
# accion = planificador.planificar_accion()
# print(accion)
