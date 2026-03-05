
from pathlib import Path
import json
import sys

DATA_FILE = Path(__file__).with_name('tareas.json')

def cargar_tareas():
    """Carga y normaliza el archivo de tareas.
    Soporta dos formatos antiguos:
    - lista de strings: ["Tarea 1", "Tarea 2"]
    - lista de objetos: [{"task": "Tarea", "done": false}, ...]
    Si el JSON está corrupto o no es válido, devuelve una lista vacía y muestra un mensaje de error por stderr.
    """
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print('Archivo JSON inválido. Se usará una lista vacía.', file=sys.stderr)
        return []
    except Exception as e:
        print(f'Error leyendo tareas: {e}', file=sys.stderr)
        return []
    # Normalizar a lista de dicts con keys: task, done
    if isinstance(data, list):
        normalized = []
        for item in data:
            if isinstance(item, str):
                normalized.append({'task': item, 'done': False})
            elif isinstance(item, dict) and 'task' in item:
                normalized.append({'task': str(item.get('task', '')), 'done': bool(item.get('done', False))})
        return normalized
    # Si no es una lista, devolver vacía
    return []

def guardar_tareas(tareas):
    """Guarda de forma atómica las tareas en `tareas.json` usando UTF-8."""
    tmp = DATA_FILE.with_name(DATA_FILE.name + '.tmp')
    try:
        with tmp.open('w', encoding='utf-8') as f:
            json.dump(tareas, f, ensure_ascii=False, indent=2)
        tmp.replace(DATA_FILE)
    except Exception as e:
        print(f'Error guardando tareas: {e}', file=sys.stderr)

def agregar_tarea(texto):
    texto = texto.strip()
    if not texto:
        print('La tarea no puede estar vacía.')
        return
    tareas = cargar_tareas()
    tareas.append({'task': texto, 'done': False})
    guardar_tareas(tareas)
    print(f'Tarea agregada: {texto}')

def listar_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print('\nNo hay tareas.\n')
        return
    print(f"\nTareas ({len(tareas)}):\n" + '-' * 30)
    for i, t in enumerate(tareas, start=1):
        estado = '✓' if t.get('done') else ' '
        print(f"{i}. [{estado}] {t.get('task')}")
    print('-' * 30 + '\n')

def eliminar_tarea(indice):
    tareas = cargar_tareas()
    if 1 <= indice <= len(tareas):
        tarea_eliminada = tareas.pop(indice - 1)
        guardar_tareas(tareas)
        print(f"Tarea eliminada: {tarea_eliminada.get('task')}")
    else:
        print('Índice inválido. No se eliminó ninguna tarea.')

def marcar_hecha(indice):
    tareas = cargar_tareas()
    if 1 <= indice <= len(tareas):
        tareas[indice - 1]['done'] = True
        guardar_tareas(tareas)
        print(f"Tarea marcada como hecha: {tareas[indice - 1].get('task')}")
    else:
        print('Índice inválido. No se modificó ninguna tarea.')

def imprimir_uso():
    print('Uso: python todo.py [comando] [args]')
    print('\nComandos:')
    print("  agregar <texto>    Añade una tarea")
    print("  listar             Muestra las tareas con su estado")
    print("  eliminar <n>       Elimina la tarea número n")
    print("  done <n>           Marca la tarea número n como hecha")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        imprimir_uso()
        sys.exit(1)
    comando = sys.argv[1]
    if comando == 'agregar':
        if len(sys.argv) < 3:
            print('Por favor, proporciona una tarea para agregar.')
            sys.exit(1)
        texto = ' '.join(sys.argv[2:])
        agregar_tarea(texto)
    elif comando == 'listar':
        listar_tareas()
    elif comando == 'eliminar':
        if len(sys.argv) < 3:
            print('Por favor, proporciona el índice de la tarea a eliminar.')
            sys.exit(1)
        try:
            indice = int(sys.argv[2])
            eliminar_tarea(indice)
        except ValueError:
            print('Índice inválido. Debe ser un número entero.')
    elif comando == 'done':
        if len(sys.argv) < 3:
            print('Por favor, proporciona el índice de la tarea a marcar como hecha.')
            sys.exit(1)
        try:
            indice = int(sys.argv[2])
            marcar_hecha(indice)
        except ValueError:
            print('Índice inválido. Debe ser un número entero.')
    else:
        print('Comando desconocido.')
        imprimir_uso()





