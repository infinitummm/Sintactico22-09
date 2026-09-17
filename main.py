"""
Programa principal de ejecucion y pruebas del taller.
Autores: Dylan Torres - Juan Gomez - Javier Rosero
Asignatura: Lenguajes de Programacion y Traduccion
"""

import sys
from typing import List, Dict

from arbol_general import (
    build_punto1_tree,
    dfs_recursive,
    dfs_iterative,
    dfs_search,
    count_leaves_dfs,
    calculate_height_dfs,
    bfs_traversal,
    bfs_search,
    render_ascii_tree
)

from arbol_expresion import (
    build_punto2_expression_tree,
    preorder_traversal,
    inorder_traversal,
    postorder_traversal,
    evaluate_expression_tree,
    render_ascii_expr_tree
)

from arbol_sintactico import (
    build_top_down_parse_tree,
    parse_tree_dfs_preorder,
    parse_tree_dfs_postorder,
    parse_tree_bfs,
    analyze_parse_tree_metrics,
    render_ascii_parse_tree
)


def ejecutar_punto_1():
    print("================================================================================")
    print("PUNTO 1. CONCEPTOS Y REPRESENTACION DE ARBOLES")
    print("================================================================================")
    tree = build_punto1_tree()

    print("\nActividad 1. Diagrama del arbol correspondiente:")
    print(render_ascii_tree(tree))

    print("Actividad 2. Identificacion de nodos y relaciones estructurales:")
    print("- Raiz: A")
    print("- Nodos hojas: E, J, G, K, L, I")
    print("- Nodos internos: A, B, C, D, F, H")
    print("- Padre del nodo J: F")
    print("- Ancestros del nodo L: H, D, A")
    print("- Descendientes del nodo B: E, F, J")
    print("- Hermanos del nodo H: I")

    print("\nActividad 3. Metricas del arbol:")
    grados = {
        'A': 3, 'B': 2, 'C': 1, 'D': 2,
        'E': 0, 'F': 1, 'G': 0, 'H': 2,
        'I': 0, 'J': 0, 'K': 0, 'L': 0
    }
    print("Grado de cada nodo:")
    for nodo, g in grados.items():
        print(f"  grado({nodo}) = {g}")
    print(f"Grado del arbol: {max(grados.values())} (determinado por el nodo A)")
    print("Profundidades:")
    print("  profundidad(A) = 0")
    print("  profundidad(F) = 2")
    print("  profundidad(J) = 3")
    print("  profundidad(L) = 3")
    h = calculate_height_dfs(tree)
    print(f"Altura total del arbol: {h} aristas ({h + 1} niveles)")

    print("\nActividad 4. Clasificacion del arbol:")
    print("- Arbol binario: No. El nodo A posee grado 3 (hijos B, C, D). En un arbol binario el grado maximo es 2.")
    print("- Arbol completo: No. No todos los nodos internos poseen el mismo grado (A tiene 3, B y D tienen 2, C y F tienen 1) ni todas las hojas se hallan al mismo nivel.")
    print("- Arbol balanceado: No. Existen ramas que terminan en profundidad 2 (E, G, I) y otras que se extienden a profundidad 3 (J, K, L).")

    print("\nAnalisis de complejidad (Punto 1):")
    print("- Contar hojas: O(n) tiempo, recorriendo los 12 nodos de forma exhaustiva; O(h) espacio en pila.")
    print("- Calcular altura: O(n) tiempo, explorando recursivamente cada bifurcacion; O(h) espacio en pila.")
    print("- Buscar un valor inexistente: O(n) tiempo en el peor caso, pues al no existir orden relacional entre hermanos se debe examinar todo el arbol.")


def ejecutar_punto_2():
    print("\n================================================================================")
    print("PUNTO 2. CONSTRUCCION DE UN ARBOL DE EXPRESIONES")
    print("Expresion: (a + 3) * (b - 2) + (c / 4)")
    print("================================================================================")
    expr_tree = build_punto2_expression_tree()

    print("\nActividad 1. Identificacion de operandos y operadores:")
    print("- Operandos: variables {a, b, c} y constantes {3, 2, 4}")
    print("- Operadores: suma (+), resta (-), multiplicacion (*), division (/)")
    print("- Agrupacion: parentesis '(' y ')' que redefinen la precedencia de la suma y resta")

    print("\nActividad 2. Diagrama del arbol de expresion:")
    print(render_ascii_expr_tree(expr_tree))

    print("Actividad 3 y 4. Recorridos y notaciones correspondientes:")
    pre = preorder_traversal(expr_tree)
    ino = inorder_traversal(expr_tree, parenthesize=True)
    post = postorder_traversal(expr_tree)

    print(f"- Recorrido en Preorden  (Notacion Prefija):  {' '.join(pre)}")
    print(f"- Recorrido en Inorden   (Notacion Infija):   {ino}")
    print(f"- Recorrido en Postorden (Notacion Postfija): {' '.join(post)}")

    print("\nActividad 5. Evaluacion del arbol para a = 5, b = 8, c = 12:")
    env = {'a': 5.0, 'b': 8.0, 'c': 12.0}
    pasos: List[str] = []
    resultado = evaluate_expression_tree(expr_tree, env, pasos)
    print("Pasos de evaluacion ascendente (bottom-up):")
    for p in pasos:
        print(f"  {p}")
    print(f"Resultado final evaluado: {resultado}")

    print("\nPreguntas de analisis (Punto 2):")
    print("1. Por que la evaluacion puede realizarse en postorden:")
    print("   Porque postorden procesa primero ambos subarboles hijos antes de la raiz, garantizando que los operandos esten completamente resueltos antes de aplicar el operador.")
    print("2. Complejidad temporal de evaluar el arbol:")
    print("   O(n), donde n es la cantidad de nodos (n = 11). Cada nodo se procesa en tiempo constante O(1).")
    print("3. Complejidad espacial del recorrido recursivo:")
    print("   O(h), donde h es la altura del arbol (longitud de la rama activa en la pila de ejecucion).")
    print("4. Consumo de memoria si el arbol esta completamente desbalanceado:")
    print("   La altura h degenera a O(n), aumentando el consumo de la pila linealmente respecto al numero de nodos.")


def ejecutar_punto_3():
    print("\n================================================================================")
    print("PUNTO 3. RECORRIDOS EN PROFUNDIDAD: DFS")
    print("================================================================================")
    tree = build_punto1_tree()

    rec_order = dfs_recursive(tree)
    iter_order = dfs_iterative(tree)
    leaves_count = count_leaves_dfs(tree)
    height_val = calculate_height_dfs(tree)

    print(f"1. DFS recursivo en preorden: {' -> '.join(rec_order)}")
    print(f"2. DFS iterativo con pila:    {' -> '.join(iter_order)}")
    print(f"4. Conteo de nodos hoja:      {leaves_count} hojas")
    print(f"5. Altura del arbol:          {height_val} aristas ({height_val + 1} niveles)")

    print("\n3. Pruebas de busqueda mediante DFS:")
    casos = [
        ("Valor cercano a la raiz", "B"),
        ("Valor del ultimo nivel", "L"),
        ("Valor que no existe", "Z")
    ]
    for desc, target in casos:
        found, visited_count, path = dfs_search(tree, target)
        print(f"- Prueba: {desc} ('{target}')")
        print(f"  Orden de visita: {' -> '.join(path)}")
        print(f"  Valor encontrado: {'Si' if found else 'No'}")
        print(f"  Nodos visitados: {visited_count}")
        print(f"  Numero de hojas en arbol: {leaves_count}")
        print(f"  Altura del arbol: {height_val}")


def ejecutar_punto_4():
    print("\n================================================================================")
    print("PUNTO 4. RECORRIDO EN ANCHURA: BFS")
    print("================================================================================")
    tree = build_punto1_tree()

    visit_order, levels = bfs_traversal(tree)
    print(f"Orden de visita BFS: {' -> '.join(visit_order)}\n")
    print("Nodos agrupados por nivel:")
    for lvl, nodos in levels.items():
        print(f"Nivel {lvl}: {', '.join(nodos)}")

    print("\nPruebas de busqueda mediante BFS:")
    casos = [
        ("Valor cercano a la raiz", "B"),
        ("Valor del ultimo nivel", "L"),
        ("Valor que no existe", "Z")
    ]
    for desc, target in casos:
        found, level_found, visited_count, _ = bfs_search(tree, target)
        print("--------------------------------------------------")
        print(f"Prueba: {desc}")
        for lvl, nodos in levels.items():
            print(f"Nivel {lvl}: {', '.join(nodos)}")
        print(f"Valor buscado: {target}")
        print(f"Resultado: {'encontrado' if found else 'no encontrado'}")
        print(f"Nivel del valor: {level_found if found is not None else 'N/A'}")
        print(f"Nodos visitados: {visited_count}")


def ejecutar_punto_5():
    print("\n================================================================================")
    print("PUNTO 5. APLICACION AL ANALISIS SINTACTICO")
    print("Gramatica descendente simplificada para: id + id * id")
    print("================================================================================")
    parse_tree, created_nodes = build_top_down_parse_tree()

    print("\nActividad 1 y 2. Arbol sintactico y orden de creacion de nodos:")
    print(render_ascii_parse_tree(parse_tree))

    print("Orden de creacion de nodos por el analizador descendente:")
    for n in created_nodes:
        tipo = "Terminal" if n.is_terminal else "No terminal"
        if n.is_epsilon:
            tipo = "Produccion vacia (epsilon)"
        print(f"  Nodo #{n.creation_id:02d}: simbolo '{n.symbol}' ({tipo})")

    print("\nActividad 3. Recorridos sobre el arbol sintactico:")
    pre = parse_tree_dfs_preorder(parse_tree)
    post = parse_tree_dfs_postorder(parse_tree)
    bfs = parse_tree_bfs(parse_tree)

    print("Recorrido DFS en preorden:")
    print("  " + " -> ".join(pre))
    print("\nRecorrido DFS en postorden:")
    print("  " + " -> ".join(post))
    print("\nRecorrido BFS por niveles:")
    print("  " + " -> ".join(bfs))

    print("\nActividad 7. Metricas del algoritmo sobre el arbol sintactico:")
    metricas = analyze_parse_tree_metrics(parse_tree)
    for k, v in metricas.items():
        print(f"- {k.replace('_', ' ').capitalize()}: {v}")


def main():
    print("################################################################################")
    print("TALLER DE ARBOLES, RECORRIDOS Y COMPLEJIDAD COMPUTACIONAL")
    print("Asignatura: Lenguajes de Programacion y Traduccion")
    print("Integrantes: Dylan Torres - Juan Gomez - Javier Rosero")
    print("################################################################################\n")

    ejecutar_punto_1()
    ejecutar_punto_2()
    ejecutar_punto_3()
    ejecutar_punto_4()
    ejecutar_punto_5()

    print("\n################################################################################")
    print("EJECUCION DE TODOS LOS PUNTOS FINALIZADA CON EXITO")
    print("################################################################################")


if __name__ == "__main__":
    main()
