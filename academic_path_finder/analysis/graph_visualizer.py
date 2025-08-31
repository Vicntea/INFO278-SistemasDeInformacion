# academic_path_finder/analysis/graph_visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

# Agrega la ruta base del proyecto al path de Python para importar correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from academic_path_finder.data_handler.json_loader import load_graph_data

def create_and_visualize_graph():
    """
    Crea un grafo dirigido y lo visualiza con nodos
    posicionados de izquierda a derecha por semestre.
    Ajusta el tamaño de nodos y texto, y oculta flechas
    con una diferencia de semestre mayor a 3.
    """
    # 1. Cargar los datos desde el archivo JSON
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', 'data', 'academic_graph.json')
    
    asignaturas, conexiones = load_graph_data(data_path)
    if asignaturas is None or conexiones is None:
        print("No se pudieron cargar los datos. Asegúrate de que el archivo JSON exista y esté en la ruta correcta.")
        return

    # 2. Construir el objeto de grafo con NetworkX
    G = nx.DiGraph()

    # Añadir los nodos (asignaturas) con sus atributos
    for codigo, info in asignaturas.items():
        G.add_node(codigo, nombre=info['nombre'], semestre=info['semestre'])

    # Añadir las aristas (conexiones)
    # y filtrar aquellas con más de 3 semestres de diferencia
    filtered_conexiones = []
    semestre_map = {romano: int(arabigo) for arabigo, romano in zip(
        ['1','2','3','4','5','6','7','8','9','10','11'],
        ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI']
    )}

    for conn in conexiones:
        origen_semestre_romano = asignaturas[conn['origen']]['semestre']
        destino_semestre_romano = asignaturas[conn['destino']]['semestre']

        origen_semestre_int = semestre_map.get(origen_semestre_romano)
        destino_semestre_int = semestre_map.get(destino_semestre_romano)

        if origen_semestre_int is not None and destino_semestre_int is not None:
            if abs(destino_semestre_int - origen_semestre_int) <= 2: #DISTANCIA DE SEMESTRE PARA NO GRAFICAR
                G.add_edge(conn['origen'], conn['destino'])
                filtered_conexiones.append(conn)
        else:
            # Si no se encuentra el semestre, añade la conexión por defecto
            G.add_edge(conn['origen'], conn['destino'])

    # 3. Calcular las posiciones de los nodos para la visualización
    pos = {}
    semestres = {}
    for codigo, data in G.nodes(data=True):
        sem = data['semestre']
        if sem not in semestres:
            semestres[sem] = []
        semestres[sem].append(codigo)

    # Ordenar los semestres para asegurar el flujo de izquierda a derecha
    semestres_ordenados = sorted(semestres.keys(), key=lambda s: semestre_map.get(s, float('inf')))
    
    x_offset_mult = 3  
    y_offset_mult = 1.0 
    
    for i, sem in enumerate(semestres_ordenados):
        x = i * x_offset_mult
        num_nodes = len(semestres[sem])
        
        if num_nodes > 1:
            y_step = y_offset_mult / (num_nodes -1)
        else:
            y_step = 0
            
        total_height = (num_nodes - 1) * y_step
        y_start_offset = total_height / 2
        
        for j, node in enumerate(semestres[sem]):
            y = j * y_step - y_start_offset
            pos[node] = (x, y)

    # 4. Configurar y dibujar el grafo con Matplotlib
    plt.figure(figsize=(25, 18))
    
    # Dibujar solo los nodos
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=1000,
        node_color='lightblue',
        edgecolors='gray'
    )

    # Dibujar solo las aristas (flechas)
    nx.draw_networkx_edges(
        G,
        pos,
        arrowsize=15,
        edge_color='gray',
        width=1.5
    )

    # Añadir las etiquetas de los nodos (el código de la asignatura)
    # **AQUÍ ESTÁ EL CAMBIO**
    node_labels = {node: node for node in G.nodes()} 
    nx.draw_networkx_labels(
        G,
        pos,
        labels=node_labels,
        font_size=8,
        font_weight='normal'
    )
    
    # Dibujar etiquetas de semestre en la parte superior
    max_y_coord = max(y for x, y in pos.values()) if pos else 0.5
    for sem in semestres_ordenados:
        sem_nodes = semestres[sem]
        if sem_nodes:
            x_pos_sem = pos[sem_nodes[0]][0]
            plt.text(x_pos_sem, max_y_coord + 0.3, f"Semestre {sem}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.title("Plan de Estudios de Ingeniería - UACH", size=18, y=1.02)
    plt.tight_layout()
    plt.show()

# Ejecuta la función cuando el script se inicie
if __name__ == '__main__':
    create_and_visualize_graph()