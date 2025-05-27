# main.py - Punto de entrada principal que maneja la interacción por voz con la IA
import speech_recognition as sr
from myIA.brain import responder, memory
from myIA.brain.llm_manager import llm_manager
from myIA.brain.self_identity import self_identity
from myIA.brain.state import internal_state
from myIA.brain.emotion_analyzer import emotion_analyzer
from myIA.brain.emotional_memory import emotional_memory
from myIA.brain.memory import interaction_memory
from myIA.brain.evolution import evolution_tracker
from myIA.brain.responder import iniciar_conversacion, pregunta_seguimiento

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Escuchando...")
        audio = r.listen(source)
        print("🔊 Audio capturado:", type(audio), "Duración:", getattr(audio, 'duration_seconds', 'desconocida'))
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("👂 Entendido:", texto)
        memory.guardar_aprendizaje("escucha", texto, tags=["voz", "audio", "palabra hablada"])
        return texto
    except sr.UnknownValueError:
        print("⚠️ No entendí nada.")
    except sr.RequestError:
        print("🚫 Error al conectar con el servicio de voz.")
    return None

def procesar_interaccion(texto):
    """Procesa la interacción del usuario, analiza emociones, actualiza el estado interno y registra la interacción."""
    # Analizar emoción
    emotion, score = emotion_analyzer.analyze_emotion(texto)
    print(f"🧠 Emoción detectada: {emotion} (confianza: {score})")

    # Registrar emoción en la memoria emocional
    emotional_memory.record_emotion(emotion, score, interaction=texto)

    # Actualizar estado interno
    internal_state.actualizar_estado(texto)
    estado_actual = internal_state.obtener_estado()
    print(f"📊 Estado interno actualizado: {estado_actual}")

    # Obtener respuesta mejorada
    respuesta = responder.responder_a(texto)

    # Registrar interacción completa
    interaction_memory.record_interaction(texto, respuesta, emotion)

    # Evolucionar personalidad
    emociones_recientes = emotional_memory.get_recent_emotions()
    self_identity.evolucionar_personalidad(emociones_recientes)

    # Registrar hito si es necesario
    if estado_actual['energia'] < 20:
        evolution_tracker.registrar_hito("Energía baja detectada, ajustar comportamiento.")

    return respuesta

if __name__ == "__main__":
    print("✅ Sistema iniciado. Inicializando modelos...")
    llm_manager.initialize()  # Inicializar LLM
    print(f"✅ Hola, soy {self_identity.name}. {self_identity.description}")
    print("✅ Estoy lista para aprender y responder.")

    while True:
        texto = escuchar()
        if texto:
            if texto.lower() in ["inicia conversación", "comienza"]:
                print(f"🤖 {iniciar_conversacion()}")
            else:
                respuesta = procesar_interaccion(texto)
                print(f"🤖 Respuesta: {respuesta}")
