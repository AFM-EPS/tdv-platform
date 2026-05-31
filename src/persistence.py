import json
from pathlib import Path

# El archivo de guardado estará en la raíz del proyecto
SAVE_FILE_PATH = Path(__file__).parent.parent / "save_data.json"

def _ensure_save_file():
    """Asegura que el archivo de guardado exista y contenga una estructura válida."""
    if not SAVE_FILE_PATH.exists():
        default_data = {
            "unlocked_levels": [1],
            "high_score": 0
        }
        try:
            with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
        except Exception as e:
            print(f"Error al inicializar el archivo de guardado: {e}")

def load_data():
    """Carga los datos de guardado desde el archivo JSON."""
    _ensure_save_file()
    try:
        with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Sanitizar y asegurar que las claves existan y tengan el tipo correcto
            if not isinstance(data, dict):
                data = {}
            if "unlocked_levels" not in data or not isinstance(data["unlocked_levels"], list):
                data["unlocked_levels"] = [1]
            else:
                # Asegurar que todos los elementos en unlocked_levels sean enteros
                data["unlocked_levels"] = [int(lvl) for lvl in data["unlocked_levels"]]
                if 1 not in data["unlocked_levels"]:
                    data["unlocked_levels"].append(1)
            
            if "high_score" not in data:
                data["high_score"] = 0
            else:
                data["high_score"] = int(data["high_score"])
                
            return data
    except Exception as e:
        print(f"Error al cargar datos de guardado: {e}")
        return {"unlocked_levels": [1], "high_score": 0}

def save_data(data):
    """Guarda un diccionario de datos en el archivo JSON."""
    try:
        with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error al escribir en el archivo de guardado: {e}")

def get_unlocked_levels():
    """Devuelve una lista de enteros correspondientes a los niveles desbloqueados."""
    data = load_data()
    return sorted(list(set(data["unlocked_levels"])))

def unlock_level(level_num):
    """Añade un nivel a la lista de niveles desbloqueados si no estaba ya."""
    try:
        level_num = int(level_num)
    except (ValueError, TypeError):
        return False
        
    data = load_data()
    if level_num not in data["unlocked_levels"]:
        data["unlocked_levels"].append(level_num)
        save_data(data)
        return True
    return False

def get_high_score():
    """Devuelve la puntuación máxima guardada."""
    data = load_data()
    return data["high_score"]

def update_high_score(score):
    """Actualiza la puntuación máxima si el score provisto es mayor."""
    try:
        score = int(score)
    except (ValueError, TypeError):
        return False
        
    data = load_data()
    if score > data["high_score"]:
        data["high_score"] = score
        save_data(data)
        return True
    return False
