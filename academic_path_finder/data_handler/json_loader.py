# academic_path_finder/data_handler/json_loader.py
import json

def load_graph_data(file_path):
    """Carga los datos de asignaturas y conexiones desde un archivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('asignaturas', {}), data.get('conexiones', [])
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return None, None
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path} no es un JSON válido.")
        return None, None