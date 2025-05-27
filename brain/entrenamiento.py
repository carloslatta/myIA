import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWLEDGE_PATH = os.path.join(DATA_DIR, "knowledge.json")
MODEL_PATH = os.path.join(DATA_DIR, "modelo.pkl")
VECTORIZER_PATH = os.path.join(DATA_DIR, "vectorizador.pkl")

modelo_entrenado = None
vectorizador = None

def entrenar_modelo(verbose=True):
    global modelo_entrenado, vectorizador
    
    if verbose:
        print("📚 Cargando datos...")
        
    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        datos = json.load(f)

    X = []
    y = []
    for entrada in datos:
        if entrada.get("respuesta"):
            X.append(entrada["descripcion"])
            y.append(entrada["respuesta"])

    if len(X) < 2:
        print("⚠️ Se necesitan al menos 2 ejemplos para entrenar")
        return False

    if verbose:
        print(f"ℹ️ Datos cargados: {len(X)} ejemplos")

    # Vectorización mejorada
    vectorizador = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2),
        max_features=5000,
        min_df=2
    )
    X_vectorizado = vectorizador.fit_transform(X)

    # Validación cruzada
    if len(np.unique(y)) >= 3 and len(X) >= 5:
        if verbose:
            print("🔄 Realizando validación cruzada...")
        modelo_cv = LogisticRegression(max_iter=1000, class_weight='balanced')
        scores = cross_val_score(modelo_cv, X_vectorizado, y, cv=min(5, len(X)))
        if verbose:
            print(f"📊 Precisión promedio en validación: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})")

    # Entrenamiento final
    if verbose:
        print("🧠 Entrenando modelo final...")
    modelo_entrenado = LogisticRegression(max_iter=1000, class_weight='balanced')
    modelo_entrenado.fit(X_vectorizado, y)

    # Evaluación en conjunto de entrenamiento
    y_pred = modelo_entrenado.predict(X_vectorizado)
    accuracy = accuracy_score(y, y_pred)
    if verbose:
        print(f"📈 Precisión en entrenamiento: {accuracy:.2f}")
        print("\nInforme detallado:")
        print(classification_report(y, y_pred))

    # Guardar modelo
    if verbose:
        print("💾 Guardando modelo...")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(modelo_entrenado, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizador, f)

    if verbose:
        print("✅ Modelo entrenado y guardado")
    return True

def cargar_modelo(verbose=True):
    global modelo_entrenado, vectorizador
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            with open(MODEL_PATH, "rb") as f:
                modelo_entrenado = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                vectorizador = pickle.load(f)
            if verbose:
                print("✅ Modelo cargado correctamente")
            return True
    except Exception as e:
        if verbose:
            print(f"❌ Error al cargar el modelo: {e}")
    return False
