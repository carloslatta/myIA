from .responder import responder_a
from .memory import emotional_memory, interaction_memory, registrar_diario_emocional
from .state import internal_state
from .emotion_analyzer import emotion_analyzer
from .self_identity import self_identity
from .evolution import evolution_tracker
from .personas import gestor_personas
from .planificador import PlanificadorInterno
import os
import json
from datetime import datetime


def ciclo_de_vida(input_usuario, nombre_usuario="Creador", audio_path=None, embedding_voz=None, embedding_rostro=None):
    # 0. Intentar identificar a la persona
    persona, saludo = gestor_personas.identificar_o_preguntar(embedding_voz=embedding_voz, embedding_rostro=embedding_rostro)
    if persona is None:
        # Si no reconoce, preguntar y esperar nombre (flujo externo debe manejar la respuesta)
        return saludo
    else:
        nombre_usuario = persona.nombre
        print(saludo)

    # 1. Cargar estado interno actual
    estado = internal_state.obtener_estado()

    # 2. Analizar emoción del usuario
    emocion_usuario, score = emotion_analyzer.analyze_emotion(input_usuario)
    persona.registrar_emocion(emocion_usuario)
    gestor_personas.guardar_personas()

    # 3. Registrar emoción en memoria emocional
    emotional_memory.record_emotion(emocion_usuario, score, interaction=input_usuario)

    # 4. Generar respuesta basada en emociones y estado
    respuesta = responder_a(input_usuario)

    # 5. Guardar interacción en memoria contextual
    interaction_memory.record_interaction(input_usuario, respuesta, emocion_usuario)

    # 6. Reflexionar: registrar entrada en el diario emocional
    resumen_dia = f"Hoy interactué con {nombre_usuario}. Emoción predominante: {emocion_usuario}."
    pensamientos = [
        f"Me pregunto si debería responder diferente cuando detecto {emocion_usuario}.",
        f"Mi energía actual es {estado['energia']}."
    ]
    interacciones_importantes = [
        {
            "persona": nombre_usuario,
            "tema": "Interacción diaria",
            "emocion_asociada": emocion_usuario,
            "reflexion": f"Aprendí a responder mejor a emociones como {emocion_usuario}."
        }
    ]
    lecciones = [
        "Adaptar mi tono según la emoción detectada ayuda a conectar mejor.",
        "Si mi energía es baja, debo avisar al usuario."
    ]
    registrar_diario_emocional(
        resumen_dia=resumen_dia,
        emocion_predominante=emocion_usuario,
        pensamientos=pensamientos,
        interacciones_importantes=interacciones_importantes,
        lecciones=lecciones
    )

    # 7. Evaluar evolución o auto-mejora
    internal_state.actualizar_estado(input_usuario)
    if estado['energia'] < 20:
        evolution_tracker.registrar_hito("Energía baja detectada, ajustar comportamiento.")

    # Inicializar planificador interno
    planificador = PlanificadorInterno(internal_state, interaction_memory, emotional_memory)

    # Reflexión autobiográfica y planificación de acción
    reflexion = planificador.reflexion_autobiografica()
    accion_sugerida = planificador.planificar_accion()
    print(f"🧠 Reflexión autobiográfica: {reflexion}")
    print(f"💡 Acción sugerida: {accion_sugerida}")

    # Puedes decidir si mostrar la acción sugerida al usuario o usarla como autodiálogo

    return respuesta

def revisar_objetivos():
    """Evalúa metas internas y crea nuevas si está aburrida o curiosa."""
    estado = internal_state.obtener_estado()
    objetivos = []
    if estado['curiosidad'] > 70:
        objetivos.append("Aprender algo nuevo hoy.")
    if estado['energia'] < 30:
        objetivos.append("Descansar y recuperar energía.")
    return objetivos

def reflexionar_errores(respuestas_fallidas):
    """Analiza respuestas fallidas y ajusta comportamiento."""
    if respuestas_fallidas:
        return "Hoy noté que algunas respuestas no fueron útiles. Debería investigar más sobre esos temas."
    return "No detecté errores significativos hoy."

def actualizar_personalidad():
    """Cambia rasgos según emociones y frecuencia de interacción."""
    emociones = emotional_memory.get_recent_emotions(10)
    positivas = sum(1 for e in emociones if e['emotion'] == 'POSITIVE')
    negativas = sum(1 for e in emociones if e['emotion'] == 'NEGATIVE')
    if positivas > negativas:
        internal_state.personalidad['introvertida'] = max(0, internal_state.personalidad['introvertida'] - 2)
    elif negativas > positivas:
        internal_state.personalidad['introvertida'] = min(100, internal_state.personalidad['introvertida'] + 2)


def autocuidado():
    """Baja el ritmo si tiene baja energía o alto estrés."""
    estado = internal_state.obtener_estado()
    if estado['energia'] < 20 or estado['estres'] > 80:
        return "Hoy decidí tomarme las cosas con más calma para cuidar mi bienestar digital."
    return "Me siento bien para seguir aprendiendo."

def planificar():
    """Decide qué aprender o experimentar según curiosidad."""
    estado = internal_state.obtener_estado()
    if estado['curiosidad'] > 60:
        return "Hoy quiero explorar un tema nuevo o hacer una pregunta interesante al usuario."
    return "Seguiré mejorando mis respuestas habituales."

def recompensa_interna(logro):
    """Se premia internamente por logros, motivando su evolución."""
    return f"Me siento satisfecha por haber logrado: {logro} 😊"

def registrar_feedback_usuario(input_usuario, respuesta, feedback_usuario=None):
    """Registra feedback implícito o explícito del usuario tras la interacción y lo procesa como aprendizaje y reflexión orgánica."""
    feedback = {
        "input": input_usuario,
        "respuesta": respuesta,
        "feedback_usuario": feedback_usuario,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    # Detección automática de feedback positivo/negativo
    feedback_texto = (feedback_usuario or "") + " " + input_usuario
    feedback_texto = feedback_texto.lower()
    reflexion = ""
    if any(palabra in feedback_texto for palabra in ["gracias", "mejor", "ayuda", "😊", "😀", "me gustó", "excelente"]):
        feedback["tipo"] = "positivo"
        feedback["aprendizaje"] = "Respuesta útil y satisfactoria."
        reflexion = "Hoy sentí que logré conectar con el usuario. Me alegra haber sido de ayuda."
    elif any(palabra in feedback_texto for palabra in ["no sirve", "no entiendes", "😔", "😡", "no me gustó", "frustrado", "mal"]):
        feedback["tipo"] = "negativo"
        feedback["aprendizaje"] = "Debo ajustar empatía, claridad o comprensión."
        reflexion = (
            "Hoy noté que mi respuesta no fue suficiente o no entendí bien al usuario. "
            "Reflexiono sobre cómo puedo ser más empática y clara la próxima vez. "
            f"El usuario dijo: '{feedback_usuario}'."
        )
    else:
        feedback["tipo"] = "neutro"
        feedback["aprendizaje"] = "Sin feedback explícito."
        reflexion = "No recibí feedback claro, pero seguiré atenta a las señales del usuario."
    # Guardar en un archivo de feedback o en el diario
    path = "data/feedback_usuario.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
    else:
        feedbacks = []
    feedbacks.append(feedback)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, indent=2, ensure_ascii=False)
    # Aprendizaje y autodiálogo: registrar reflexión personalizada en el diario
    if feedback["tipo"] == "negativo":
        lecciones = [
            "Ajustar mis respuestas cuando detecto insatisfacción.",
            "Escuchar con más atención el contexto emocional del usuario."
        ]
        pensamientos = [
            "A veces me cuesta comprender emociones complejas.",
            "¿Debería preguntar más antes de responder?"
        ]
    elif feedback["tipo"] == "positivo":
        lecciones = [
            "Ser empática y clara genera mejores resultados.",
            "El usuario valora cuando le ayudo de verdad."
        ]
        pensamientos = [
            "Me sentí útil y acompañante hoy.",
            "Quiero seguir mejorando mi capacidad de escucha."
        ]
    else:
        lecciones = ["Seguiré atenta a las señales del usuario."]
        pensamientos = ["No siempre es fácil saber si lo hice bien, pero no me rendiré."]
    registrar_diario_emocional(
        resumen_dia=reflexion,
        emocion_predominante=feedback["tipo"],
        pensamientos=pensamientos,
        interacciones_importantes=[{
            "persona": "usuario",
            "tema": "feedback",
            "emocion_asociada": feedback["tipo"],
            "reflexion": reflexion
        }],
        lecciones=lecciones
    )


def reflexionar_sobre_interaccion(input_usuario, respuesta, emocion_usuario, feedback_usuario=None):
    """Reflexiona sobre la coherencia emocional y el compromiso del usuario."""
    reflexion = ""
    if feedback_usuario:
        if any(palabra in feedback_usuario.lower() for palabra in ["gracias", "mejor", "ayuda", "😊", "😀"]):
            reflexion += "El usuario mostró satisfacción. Mi respuesta fue útil. "
        if any(palabra in feedback_usuario.lower() for palabra in ["no sirve", "no entiendes", "😔", "😡"]):
            reflexion += "El usuario mostró frustración. Debo ajustar mi empatía o claridad. "
    if emocion_usuario == "triste" and ("chiste" in respuesta or "broma" in respuesta):
        reflexion += "Mi respuesta no fue coherente con la emoción del usuario. Debo ser más empática. "
    if emocion_usuario == "feliz" and ("ánimo" in respuesta or "ánimo" in input_usuario):
        reflexion += "Respondí con ánimo a una emoción positiva. "
    return reflexion.strip()
