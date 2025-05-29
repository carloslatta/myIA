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
from myIA.brain.voice import voice
from myIA.brain.audio_analyzer import audio_analyzer
from myIA.brain.behavior_dict import behavior_dict
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import soundfile as sf
from myIA.brain.ciclo_vital import ciclo_de_vida
import random
import cv2
from deepface import DeepFace

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

def procesar_interaccion_con_audio(audio_path, texto):
    """Procesa la interacción del usuario combinando análisis de audio y texto."""
    # Analizar tono de voz
    tono = audio_analyzer.analizar_tono(audio_path)
    print(f"🎵 Tono de voz analizado: {tono}")

    # Analizar emoción en texto
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

def procesar_interaccion_con_contexto(audio_path, texto):
    """Procesa la interacción del usuario combinando análisis de audio, texto y contexto emocional."""
    # Analizar tono de voz
    tono = audio_analyzer.analizar_tono(audio_path)
    print(f"🎵 Tono de voz analizado: {tono}")

    # Analizar emoción en texto
    emotion, score = emotion_analyzer.analyze_emotion(texto)
    print(f"🧠 Emoción detectada: {emotion} (confianza: {score})")

    # Registrar emoción en la memoria emocional
    emotional_memory.record_emotion(emotion, score, interaction=texto)

    # Actualizar estado interno
    internal_state.actualizar_estado(texto)
    estado_actual = internal_state.obtener_estado()
    print(f"📊 Estado interno actualizado: {estado_actual}")

    # Obtener respuesta base
    respuesta = responder.responder_a(texto)

    # Ajustar respuesta según comportamiento emocional
    comportamiento = behavior_dict["emociones"].get(emotion, behavior_dict["emociones"]["neutral"])
    respuesta = comportamiento["respuesta_larga"] if len(texto) > 20 else comportamiento["respuesta_corta"]

    # Ajustar respuesta según estado interno
    if estado_actual["energia"] < 20:
        respuesta = behavior_dict["reaccion_self"]["baja_energia"]["expresion"] + " " + respuesta
    elif estado_actual["estres"] > 70:
        respuesta = behavior_dict["reaccion_self"]["alto_estres"]["expresion"] + " " + respuesta

    # Registrar interacción completa
    interaction_memory.record_interaction(texto, respuesta, emotion)

    # Evolucionar personalidad
    emociones_recientes = emotional_memory.get_recent_emotions()
    self_identity.evolucionar_personalidad(emociones_recientes)

    # Registrar hito si es necesario
    if estado_actual['energia'] < 20:
        evolution_tracker.registrar_hito("Energía baja detectada, ajustar comportamiento.")

    return respuesta

def capturar_audio_y_guardar(path="audio_usuario.wav"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Escuchando...")
        audio = r.listen(source)
        with open(path, "wb") as f:
            f.write(audio.get_wav_data())
    return path

def extraer_embedding_voz(audio_path):
    wav = preprocess_wav(audio_path)
    encoder = VoiceEncoder()
    embedding = encoder.embed_utterance(wav)
    return embedding.tolist()

def capturar_imagen_y_guardar(path="rostro_usuario.jpg"):
    cam = cv2.VideoCapture(0)
    print("📸 Capturando imagen del usuario...")
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(path, frame)
        print("✅ Imagen capturada y guardada.")
    else:
        print("❌ No se pudo capturar la imagen.")
    cam.release()
    return path

# Reemplazo la función de extracción de embedding facial usando DeepFace
def extraer_embedding_rostro(imagen_path):
    try:
        embedding = DeepFace.represent(img_path=imagen_path, model_name='Facenet')[0]["embedding"]
        return embedding
    except Exception as e:
        print(f"❌ No se pudo extraer el embedding facial: {e}")
        return None

if __name__ == "__main__":
    print("✅ Sistema iniciado. Inicializando modelos...")
    llm_manager.initialize()  # Inicializar LLM
    print(f"✅ Hola, soy {self_identity.name}. {self_identity.description}")
    voice.hablar(f"Hola, soy {self_identity.name}. Estoy lista para aprender y responder.")

    while True:
        audio_path = capturar_audio_y_guardar()
        imagen_path = capturar_imagen_y_guardar()
        texto = escuchar()
        embedding_voz = extraer_embedding_voz(audio_path) if audio_path else None
        embedding_rostro = extraer_embedding_rostro(imagen_path) if imagen_path else None
        if texto:
            respuesta = ciclo_de_vida(texto, audio_path=audio_path, embedding_voz=embedding_voz, embedding_rostro=embedding_rostro)
            print(f"🤖 Respuesta: {respuesta}")
            voice.hablar(respuesta)
