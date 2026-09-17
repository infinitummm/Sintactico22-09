"""
Estructura de datos para un arbol general (n-ario).
Permite representar nodos con una cantidad arbitraria de hijos,
e implementa algoritmos fundamentales de recorrido DFS y BFS.
"""

from collections import deque
from typing import List, Optional, Tuple, Dict, Any

class TreeNode:
    """Nodo para un arbol general."""
    def __init__(self, value: str):
        self.value: str = value
        self.children: List['TreeNode'] = []

    def add_child(self, child_node: 'TreeNode') -> 'TreeNode':
        self.children.append(child_node)
        return child_node

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def get_degree(self) -> int:
        return len(self.children)


def build_punto1_tree() -> TreeNode:
    """
    Construye el arbol presentado en el Punto 1 segun las relaciones padre-hijo:
    A -> B, C, D
    B -> E, F
    C -> G
    D -> H, I
    F -> J
    H -> K, L
    """
    nodes: Dict[str, TreeNode] = {name: TreeNode(name) for name in [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'
    ]}

    # Conectar relaciones
    nodes['A'].add_child(nodes['B'])
    nodes['A'].add_child(nodes['C'])
    nodes['A'].add_child(nodes['D'])

    nodes['B'].add_child(nodes['E'])
    nodes['B'].add_child(nodes['F'])

    nodes['C'].add_child(nodes['G'])

    nodes['D'].add_child(nodes['H'])
    nodes['D'].add_child(nodes['I'])

    nodes['F'].add_child(nodes['J'])

    nodes['H'].add_child(nodes['K'])
    nodes['H'].add_child(nodes['L'])

    return nodes['A']


# ==============================================================================
# ALGORITMOS DFS (PUNTO 3)
# ==============================================================================

def dfs_recursive(node: Optional[TreeNode], visit_order: Optional[List[str]] = None) -> List[str]:
    """1. DFS recursivo en preorden."""
    if visit_order is None:
        visit_order = []
    if node is None:
        return visit_order

    visit_order.append(node.value)
    for child in node.children:
        dfs_recursive(child, visit_order)
    return visit_order


def dfs_iterative(root: Optional[TreeNode]) -> List[str]:
    """2. DFS iterativo utilizando una pila explicita."""
    if root is None:
        return []

    visit_order: List[str] = []
    stack: List[TreeNode] = [root]

    while stack:
        current = stack.pop()
        visit_order.append(current.value)
        # Apilar en orden inverso para recorrer los hijos de izquierda a derecha
        for child in reversed(current.children):
            stack.append(child)

    return visit_order


def dfs_search(root: Optional[TreeNode], target: str) -> Tuple[bool, int, List[str]]:
    """
    3. Busqueda de un valor mediante DFS.
    Retorna (encontrado, cantidad_nodos_visitados, camino_de_visita).
    """
    if root is None:
        return False, 0, []

    visited: List[str] = []
    stack: List[TreeNode] = [root]

    while stack:
        current = stack.pop()
        visited.append(current.value)
        if current.value == target:
            return True, len(visited), visited
        for child in reversed(current.children):
            stack.append(child)

    return False, len(visited), visited


def count_leaves_dfs(node: Optional[TreeNode]) -> int:
    """4. Conteo de nodos hoja mediante DFS recursivo."""
    if node is None:
        return 0
    if node.is_leaf():
        return 1
    total = 0
    for child in node.children:
        total += count_leaves_dfs(child)
    return total


def calculate_height_dfs(node: Optional[TreeNode]) -> int:
    """
    5. Calculo de la altura del arbol mediante DFS.
    Definicion por aristas: hoja = 0, arbol vacio = -1.
    """
    if node is None:
        return -1
    if node.is_leaf():
        return 0
    max_child_height = 0
    for child in node.children:
        h = calculate_height_dfs(child)
        if h > max_child_height:
            max_child_height = h
    return 1 + max_child_height


# ==============================================================================
# ALGORITMOS BFS (PUNTO 4)
# ==============================================================================

def bfs_traversal(root: Optional[TreeNode]) -> Tuple[List[str], Dict[int, List[str]]]:
    """
    Recorrido en anchura BFS utilizando una cola.
    Retorna (orden_visita, nodos_por_nivel).
    """
    if root is None:
        return [], {}

    visit_order: List[str] = []
    levels: Dict[int, List[str]] = {}
    queue: deque = deque([(root, 0)])

    while queue:
        current, level = queue.popleft()
        visit_order.append(current.value)

        if level not in levels:
            levels[level] = []
        levels[level].append(current.value)

        for child in current.children:
            queue.append((child, level + 1))

    return visit_order, levels


def bfs_search(root: Optional[TreeNode], target: str) -> Tuple[bool, Optional[int], int, List[str]]:
    """
    Busqueda de un valor mediante BFS.
    Retorna (encontrado, nivel_del_valor, cantidad_nodos_visitados, orden_de_visita).
    """
    if root is None:
        return False, None, 0, []

    visited: List[str] = []
    queue: deque = deque([(root, 0)])

    while queue:
        current, level = queue.popleft()
        visited.append(current.value)

        if current.value == target:
            return True, level, len(visited), visited

        for child in current.children:
            queue.append((child, level + 1))

    return False, None, len(visited), visited


def render_ascii_tree(node: TreeNode, prefix: str = "", is_tail: bool = True) -> str:
    """Genera representacion visual en texto del arbol general."""
    branch = "└── " if is_tail else "├── "
    res = prefix + branch + f"[{node.value}]\n"
    child_prefix = prefix + ("    " if is_tail else "│   ")
    for i, child in enumerate(node.children):
        is_last = (i == len(node.children) - 1)
        res += render_ascii_tree(child, child_prefix, is_last)
    return res
