import librosa

class AudioAnalyzer:
    def __init__(self):
        pass

    def analizar_tono(self, audio_path):
        """Analiza el tono y ritmo del audio."""
        try:
            y, sr = librosa.load(audio_path)
            pitch = librosa.feature.rms(y=y).mean()  # Energía del audio
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)  # Ritmo
            return {"pitch": pitch, "tempo": tempo}
        except Exception as e:
            print(f"❌ Error al analizar el audio: {e}")
            return {"pitch": None, "tempo": None}

# Instancia global del analizador de audio
audio_analyzer = AudioAnalyzer()