from pathlib import Path
import json
import sys

DATA_FILE = Path(__file__).with_name('tareas.json')

def cargar_tareas():
    """
    Returns:
        Una lista de tareas cargada desde el archivo JSON. Si el archivo no existe, devuelve una lista vacía.
    """
    if DATA_FILE.exists():
        with open(DATA_FILE , 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

