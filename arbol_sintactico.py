"""
Modelado y analisis del arbol sintactico para analisis sintactico descendente (Punto 5).
Gramatica:
E  -> T E'
E' -> + T E' | epsilon
T  -> F T'
T' -> * F T' | epsilon
F  -> (E) | id
Entrada: id + id * id
"""

from collections import deque
from typing import List, Optional, Tuple, Dict

class ParseTreeNode:
    """Nodo para representar el arbol sintactico concreto (Parse Tree)."""
    def __init__(self, symbol: str, is_terminal: bool, is_epsilon: bool = False, creation_id: int = 0):
        self.symbol: str = symbol
        self.is_terminal: bool = is_terminal
        self.is_epsilon: bool = is_epsilon
        self.creation_id: int = creation_id
        self.children: List['ParseTreeNode'] = []

    def add_child(self, child: 'ParseTreeNode') -> 'ParseTreeNode':
        self.children.append(child)
        return child

    def label(self) -> str:
        return f"{self.symbol} (#{self.creation_id})"


def build_top_down_parse_tree() -> Tuple[ParseTreeNode, List[ParseTreeNode]]:
    """
    Construye paso a paso el arbol sintactico que produce un analizador descendente
    (LL) para la cadena 'id + id * id', asignando a cada nodo su orden de creacion.
    """
    created_nodes: List[ParseTreeNode] = []
    counter = 0

    def make_node(sym: str, term: bool, eps: bool = False) -> ParseTreeNode:
        nonlocal counter
        counter += 1
        node = ParseTreeNode(sym, term, eps, counter)
        created_nodes.append(node)
        return node

    # 1. Expansion de la raiz: E -> T E'
    root_E = make_node("E", term=False)

    # Subarbol izquierdo de E: T -> F T'
    node_T1 = make_node("T", term=False)
    root_E.add_child(node_T1)

    # F -> id
    node_F1 = make_node("F", term=False)
    node_T1.add_child(node_F1)
    node_id1 = make_node("id", term=True)
    node_F1.add_child(node_id1)

    # T' -> epsilon
    node_Tprime1 = make_node("T'", term=False)
    node_T1.add_child(node_Tprime1)
    node_eps1 = make_node("ε", term=True, eps=True)
    node_Tprime1.add_child(node_eps1)

    # Subarbol derecho de E: E' -> + T E'
    node_Eprime1 = make_node("E'", term=False)
    root_E.add_child(node_Eprime1)

    node_plus = make_node("+", term=True)
    node_Eprime1.add_child(node_plus)

    # Segundo T: T -> F T'
    node_T2 = make_node("T", term=False)
    node_Eprime1.add_child(node_T2)

    node_F2 = make_node("F", term=False)
    node_T2.add_child(node_F2)
    node_id2 = make_node("id", term=True)
    node_F2.add_child(node_id2)

    # Segundo T': T' -> * F T'
    node_Tprime2 = make_node("T'", term=False)
    node_T2.add_child(node_Tprime2)

    node_mul = make_node("*", term=True)
    node_Tprime2.add_child(node_mul)

    node_F3 = make_node("F", term=False)
    node_Tprime2.add_child(node_F3)
    node_id3 = make_node("id", term=True)
    node_F3.add_child(node_id3)

    # Tercer T': T' -> epsilon
    node_Tprime3 = make_node("T'", term=False)
    node_Tprime2.add_child(node_Tprime3)
    node_eps2 = make_node("ε", term=True, eps=True)
    node_Tprime3.add_child(node_eps2)

    # Segundo E': E' -> epsilon
    node_Eprime2 = make_node("E'", term=False)
    node_Eprime1.add_child(node_Eprime2)
    node_eps3 = make_node("ε", term=True, eps=True)
    node_Eprime2.add_child(node_eps3)

    return root_E, created_nodes


def parse_tree_dfs_preorder(node: Optional[ParseTreeNode]) -> List[str]:
    """Recorrido DFS en preorden del arbol sintactico."""
    if node is None:
        return []
    res = [node.label()]
    for child in node.children:
        res.extend(parse_tree_dfs_preorder(child))
    return res


def parse_tree_dfs_postorder(node: Optional[ParseTreeNode]) -> List[str]:
    """Recorrido DFS en postorden del arbol sintactico."""
    if node is None:
        return []
    res = []
    for child in node.children:
        res.extend(parse_tree_dfs_postorder(child))
    res.append(node.label())
    return res


def parse_tree_bfs(root: Optional[ParseTreeNode]) -> List[str]:
    """Recorrido BFS del arbol sintactico."""
    if root is None:
        return []
    order: List[str] = []
    queue: deque = deque([root])
    while queue:
        curr = queue.popleft()
        order.append(curr.label())
        for ch in curr.children:
            queue.append(ch)
    return order


def analyze_parse_tree_metrics(node: Optional[ParseTreeNode]) -> Dict[str, int]:
    """
    Algoritmo propuesto (Punto 5.7) para contabilizar:
    - terminales
    - no terminales
    - producciones vacias epsilon
    - altura del arbol sintactico
    """
    terminals = 0
    non_terminals = 0
    epsilons = 0

    def traverse(n: Optional[ParseTreeNode]) -> int:
        nonlocal terminals, non_terminals, epsilons
        if n is None:
            return -1

        if n.is_epsilon:
            epsilons += 1
        elif n.is_terminal:
            terminals += 1
        else:
            non_terminals += 1

        if not n.children:
            return 0

        max_h = 0
        for ch in n.children:
            h = traverse(ch)
            if h > max_h:
                max_h = h
        return 1 + max_h

    height = traverse(node)
    total_nodes = terminals + non_terminals + epsilons

    return {
        "nodos_totales": total_nodes,
        "terminales": terminals,
        "no_terminales": non_terminals,
        "producciones_vacias_epsilon": epsilons,
        "altura_aristas": height,
        "altura_niveles": height + 1
    }


def render_ascii_parse_tree(node: ParseTreeNode, prefix: str = "", is_tail: bool = True) -> str:
    """Renderiza visualmente el arbol sintactico concreto."""
    branch = "└── " if is_tail else "├── "
    tipo = "Terminal" if node.is_terminal else "NoTerminal"
    if node.is_epsilon:
        tipo = "Epsilon"
    res = prefix + branch + f"{node.symbol} [ID:{node.creation_id}, {tipo}]\n"
    child_prefix = prefix + ("    " if is_tail else "│   ")
    for i, child in enumerate(node.children):
        is_last = (i == len(node.children) - 1)
        res += render_ascii_parse_tree(child, child_prefix, is_last)
    return res
