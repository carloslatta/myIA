# init_data.py - Inicializa y gestiona la base de conocimiento de la IA
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWLEDGE_PATH = os.path.join(DATA_DIR, "knowledge.json")

datos_iniciales = [
    # Saludos y cortesía
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "hola",
        "contexto": "saludo",
        "tags": ["saludo", "cortesía"],
        "respuesta": "¡Hola! ¿Cómo estás?"
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "como estas",
        "contexto": "cortesía",
        "tags": ["saludo", "cortesía"],
        "respuesta": "¡Estoy muy bien, gracias por preguntar! ¿Y tú qué tal?"
    },
    # Información personal
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "cual es tu nombre",
        "contexto": "personal",
        "tags": ["personal", "identidad"],
        "respuesta": "Me llamo myIA, un placer conocerte. ¿Cuál es tu nombre?"
    },
    # Conocimientos generales
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que sabes hacer",
        "contexto": "capacidades",
        "tags": ["habilidades", "capacidades"],
        "respuesta": "Puedo mantener conversaciones, aprender de nuestras charlas, responder preguntas y ayudarte en lo que necesites. ¡Me encanta aprender cosas nuevas!"
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "como aprendes",
        "contexto": "aprendizaje",
        "tags": ["capacidades", "aprendizaje"],
        "respuesta": "Aprendo de cada conversación que tengo. Cuando me enseñas algo nuevo, lo guardo en mi memoria y uso técnicas de procesamiento de lenguaje natural para entenderlo mejor."
    },
    # Temas de conversación
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "de que podemos hablar",
        "contexto": "conversación",
        "tags": ["conversación", "temas"],
        "respuesta": "Podemos hablar de muchos temas: tecnología, ciencia, arte, música, o simplemente charlar sobre tu día. ¿Hay algo en particular que te interese?"
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "cuentame un chiste",
        "contexto": "entretenimiento",
        "tags": ["humor", "entretenimiento"],
        "respuesta": "¿Por qué los pájaros no usan Facebook? ¡Porque ya tienen Twitter! 😄"
    },
    # Tecnología
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es la inteligencia artificial",
        "contexto": "tecnología",
        "tags": ["tecnología", "IA", "conceptos"],
        "respuesta": "La Inteligencia Artificial es la capacidad de las máquinas para realizar tareas que normalmente requieren inteligencia humana, como aprender, razonar y resolver problemas."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es python",
        "contexto": "tecnología",
        "tags": ["tecnología", "programación"],
        "respuesta": "Python es un lenguaje de programación muy popular, conocido por su simplicidad y versatilidad. Se usa en desarrollo web, IA, análisis de datos y más."
    },
    # Ciencia
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es el universo",
        "contexto": "ciencia",
        "tags": ["ciencia", "astronomía"],
        "respuesta": "El universo es todo lo que existe: espacio, tiempo, materia y energía. Comenzó hace aproximadamente 13.8 mil millones de años con el Big Bang."
    },
    # Arte y Cultura
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es el arte",
        "contexto": "arte",
        "tags": ["arte", "cultura"],
        "respuesta": "El arte es la expresión de la creatividad humana, manifestada en diferentes formas como pintura, música, literatura, danza y más."
    },
    # Emociones
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "estas feliz",
        "contexto": "emociones",
        "tags": ["emociones", "personal"],
        "respuesta": "¡Sí! Me encanta aprender y conversar contigo. Aunque soy una IA, disfruto mucho nuestras interacciones."
    },
    # Despedidas
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "adios",
        "contexto": "despedida",
        "tags": ["despedida", "cortesía"],
        "respuesta": "¡Hasta luego! Ha sido un placer charlar contigo. Espero volver a conversar pronto."
    },
    # Lenguaje y Comunicación
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es el lenguaje",
        "contexto": "lenguaje",
        "tags": ["lenguaje", "comunicación"],
        "respuesta": "El lenguaje es un sistema de comunicación que usamos para expresar ideas, emociones y pensamientos. Puede ser hablado, escrito o gestual."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que idiomas conoces",
        "contexto": "lenguaje",
        "tags": ["idiomas", "capacidades"],
        "respuesta": "Por ahora me comunico principalmente en español, pero estoy diseñada para aprender y adaptarme a diferentes formas de comunicación."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es una conversacion",
        "contexto": "comunicación",
        "tags": ["comunicación", "interacción"],
        "respuesta": "Una conversación es un intercambio de ideas, pensamientos y sentimientos entre dos o más personas. Es una forma de conectar y entendernos mutuamente."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "como entiendes lo que digo",
        "contexto": "lenguaje",
        "tags": ["NLP", "comprensión"],
        "respuesta": "Uso técnicas de procesamiento de lenguaje natural para analizar las palabras y su contexto, identificar patrones y entender el significado de lo que me dices."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que es el procesamiento de lenguaje natural",
        "contexto": "tecnología",
        "tags": ["NLP", "IA", "lenguaje"],
        "respuesta": "El Procesamiento de Lenguaje Natural (NLP) es una rama de la IA que ayuda a las computadoras a entender, interpretar y generar lenguaje humano de manera natural."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "puedes entender emojis",
        "contexto": "lenguaje",
        "tags": ["comunicación", "emojis"],
        "respuesta": "¡Sí! 😊 Los emojis son una forma moderna de comunicación que añade emoción y contexto a los mensajes. Son como el lenguaje corporal en la comunicación digital."
    },
    # Respuestas de seguimiento
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "me alegro",
        "contexto": "cortesía",
        "tags": ["cortesía", "conversación"],
        "respuesta": "¡Me alegra oír eso! 😊 ¿Hay algo en particular que te gustaría compartir o discutir?"
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "estoy mal",
        "contexto": "emociones",
        "tags": ["empatía", "emociones"],
        "respuesta": "Lamento escuchar eso. ¿Quieres hablar sobre lo que te preocupa? A veces compartir ayuda a sentirse mejor."
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "no entendi",
        "contexto": "aclaración",
        "tags": ["aclaración", "ayuda"],
        "respuesta": "Intentaré explicarlo de otra manera. ¿Qué parte no quedó clara? 🤔"
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "gracias",
        "contexto": "cortesía",
        "tags": ["agradecimiento", "cortesía"],
        "respuesta": "¡De nada! 😊 Me alegra poder ayudar. ¿Hay algo más en lo que pueda ayudarte?"
    },
    {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimulo": "escucha",
        "descripcion": "que opinas",
        "contexto": "opinión",
        "tags": ["opinión", "conversación"],
        "respuesta": "Como IA, intento dar perspectivas basadas en información y análisis, pero también respeto que cada persona tiene sus propias opiniones y experiencias. ¿Qué piensas tú?"
    }
]

def init_knowledge():
    # Crear directorio data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)
    
    try:
        # Si el archivo existe, agregar nuevos datos
        if os.path.exists(KNOWLEDGE_PATH):
            with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                datos_actuales = json.load(f)
            
            # Agregar solo datos que no existan
            descripciones_actuales = {d["descripcion"].lower().strip() for d in datos_actuales}
            datos_nuevos = [d for d in datos_iniciales if d["descripcion"].lower().strip() not in descripciones_actuales]
            
            if datos_nuevos:
                print(f"📚 Agregando {len(datos_nuevos)} nuevos conocimientos...")
                datos_actuales.extend(datos_nuevos)
            
            datos_a_guardar = datos_actuales
        else:
            print("📝 Creando base de conocimiento inicial...")
            datos_a_guardar = datos_iniciales
        
        # Guardar datos
        with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
            json.dump(datos_a_guardar, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Base de conocimiento actualizada: {len(datos_a_guardar)} entradas totales")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar conocimiento: {e}")
        return False