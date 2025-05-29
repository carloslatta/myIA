import pyttsx3

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.configure_voice()

    def configure_voice(self):
        """Configura la voz y velocidad del motor de síntesis."""
        self.engine.setProperty('rate', 150)  # Velocidad de habla
        self.engine.setProperty('volume', 0.9)  # Volumen (0.0 a 1.0)

        # Seleccionar una voz (opcional, depende del sistema operativo)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'es' in voice.languages:  # Buscar una voz en español
                self.engine.setProperty('voice', voice.id)
                break

    def hablar(self, texto):
        """Convierte texto a voz y lo reproduce."""
        self.engine.say(texto)
        self.engine.runAndWait()

# Instancia global de voz
voice = Voice()