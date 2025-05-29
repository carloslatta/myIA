import json
import os
from datetime import datetime

class Persona:
    def __init__(self, nombre, descripcion="", embedding_voz=None, embedding_rostro=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.embedding_voz = embedding_voz  # Lista de floats
        self.embedding_rostro = embedding_rostro  # Lista de floats
        self.historial_emociones = []
        self.ultima_interaccion = None

    def registrar_emocion(self, emocion):
        self.historial_emociones.append({
            "emocion": emocion,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.ultima_interaccion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "embedding_voz": self.embedding_voz,
            "embedding_rostro": self.embedding_rostro,
            "historial_emociones": self.historial_emociones,
            "ultima_interaccion": self.ultima_interaccion
        }

class GestorPersonas:
    def __init__(self, path="data/personas.json"):
        self.path = path
        self.personas = []
        self.cargar_personas()

    def cargar_personas(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.personas = [Persona(**p) for p in data.get("personas", [])]
        else:
            self.personas = []

    def guardar_personas(self):
        data = {"personas": [p.to_dict() for p in self.personas]}
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def buscar_por_nombre(self, nombre):
        for p in self.personas:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def buscar_por_embedding_voz(self, embedding, umbral=0.75):
        # Compara el embedding de voz con los almacenados (usa similitud coseno)
        import numpy as np
        for p in self.personas:
            if p.embedding_voz is not None:
                sim = self.similitud_coseno(embedding, p.embedding_voz)
                if sim > umbral:
                    return p
        return None

    def buscar_por_embedding_rostro(self, embedding, umbral=0.75):
        import numpy as np
        for p in self.personas:
            if p.embedding_rostro is not None:
                sim = self.similitud_coseno(embedding, p.embedding_rostro)
                if sim > umbral:
                    return p
        return None

    @staticmethod
    def similitud_coseno(vec1, vec2):
        import numpy as np
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def registrar_persona(self, nombre, descripcion="", embedding_voz=None, embedding_rostro=None):
        persona = self.buscar_por_nombre(nombre)
        if not persona:
            persona = Persona(nombre, descripcion, embedding_voz, embedding_rostro)
            self.personas.append(persona)
            self.guardar_personas()
        return persona

    def actualizar_embedding_voz(self, nombre, embedding_voz):
        persona = self.buscar_por_nombre(nombre)
        if persona:
            persona.embedding_voz = embedding_voz
            self.guardar_personas()

    def actualizar_embedding_rostro(self, nombre, embedding_rostro):
        persona = self.buscar_por_nombre(nombre)
        if persona:
            persona.embedding_rostro = embedding_rostro
            self.guardar_personas()

    def identificar_o_preguntar(self, embedding_voz=None, embedding_rostro=None):
        """Intenta identificar a la persona por voz o rostro, si no la reconoce, pregunta su nombre y la registra."""
        persona = None
        if embedding_voz is not None:
            persona = self.buscar_por_embedding_voz(embedding_voz)
        if persona is None and embedding_rostro is not None:
            persona = self.buscar_por_embedding_rostro(embedding_rostro)
        if persona:
            saludo = f"¡Hola, {persona.nombre}!"
            if persona.historial_emociones:
                ultima = persona.historial_emociones[-1]["emocion"]
                saludo += f" Recuerdo que la última vez estabas {ultima}. ¿Cómo te sientes hoy?"
            return persona, saludo
        else:
            # Flujo para preguntar y registrar nueva persona
            return None, "No estoy segura de quién eres. ¿Puedes decirme tu nombre o contarme algo sobre ti?"

    def registrar_nueva_persona(self, nombre, descripcion="", embedding_voz=None, embedding_rostro=None):
        persona = self.registrar_persona(nombre, descripcion, embedding_voz, embedding_rostro)
        return persona

# Instancia global del gestor de personas
gestor_personas = GestorPersonas()
