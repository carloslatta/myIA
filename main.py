import speech_recognition as sr
from datetime import datetime
import os

LOG_PATH = "data/log.txt"

# Asegura que el archivo exista
os.makedirs("data", exist_ok=True)
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w") as f:
        f.write("=== Registro de aprendizajes ===\n")

def guardar_en_memoria(texto):
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now()}: {texto}\n")
    print("🧠 Guardado:", texto)

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Escuchando...")
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("👂 Entendido:", texto)
        guardar_en_memoria(texto)
    except sr.UnknownValueError:
        print("⚠️ No entendí nada.")
    except sr.RequestError:
        print("🚫 Error al conectar con el servicio de voz.")

if __name__ == "__main__":
    print("✅ Sistema de escucha iniciado correctamente. Estoy lista para aprender.")
    while True:
        escuchar()
