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

def guardar_tareas(tareas):
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tareas, f, indent=4)

def agregar_tarea(tarea):
    tareas = cargar_tareas()
    tareas.append(tarea)
    guardar_tareas(tareas)

def listar_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print("No hay tareas pendientes.")
    else:
        for i, tarea in enumerate(tareas, start=1):
            print(f"{i}. {tarea}")

def eliminar_tarea(indice):
    tareas = cargar_tareas()
    if 0 < indice <= len(tareas):
        tarea_eliminada = tareas.pop(indice - 1)
        guardar_tareas(tareas)
        print(f"Tarea eliminada: {tarea_eliminada}")
    else:
        print("Índice inválido. No se eliminó ninguna tarea.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python todo.py [agregar|listar|eliminar] [tarea/índice]")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "agregar":
        if len(sys.argv) < 3:
            print("Por favor, proporciona una tarea para agregar.")
            sys.exit(1)
        tarea = " ".join(sys.argv[2:])
        agregar_tarea(tarea)
        print(f"Tarea agregada: {tarea}")

    elif comando == "listar":
        listar_tareas()

    elif comando == "eliminar":
        if len(sys.argv) < 3:
            print("Por favor, proporciona el índice de la tarea a eliminar.")
            sys.exit(1)
        try:
            indice = int(sys.argv[2])
            eliminar_tarea(indice)
        except ValueError:
            print("Índice inválido. Debe ser un número entero.")
    else:
        print("Comando desconocido. Usa 'agregar', 'listar' o 'eliminar'.")





