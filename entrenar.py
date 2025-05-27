from brain.entrenamiento import entrenar_modelo
from brain.init_data import init_knowledge

if __name__ == "__main__":
    print("Inicializando datos de ejemplo...")
    init_knowledge()
    print("\nEntrenando modelo...")
    entrenar_modelo()
