"""
Estructura de datos para un arbol binario de expresiones aritmeticas (Punto 2).
Permite representar operandos y operadores, generar notaciones prefija, infija y
postfija mediante recorridos, y evaluar la expresion navegando el arbol.
"""

from typing import Optional, List, Dict, Union

class ExprNode:
    """Nodo binario para un arbol de expresiones."""
    def __init__(self, value: str, left: Optional['ExprNode'] = None, right: Optional['ExprNode'] = None):
        self.value: str = value
        self.left: Optional['ExprNode'] = left
        self.right: Optional['ExprNode'] = right

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_punto2_expression_tree() -> ExprNode:
    """
    Construye el arbol de expresion para:
    (a + 3) * (b - 2) + (c / 4)
    """
    # Subarbol izquierdo: (a + 3)
    nodo_a = ExprNode('a')
    nodo_3 = ExprNode('3')
    nodo_suma_izq = ExprNode('+', nodo_a, nodo_3)

    # Subarbol derecho: (b - 2)
    nodo_b = ExprNode('b')
    nodo_2 = ExprNode('2')
    nodo_resta = ExprNode('-', nodo_b, nodo_2)

    # Multiplicacion: (a + 3) * (b - 2)
    nodo_mult = ExprNode('*', nodo_suma_izq, nodo_resta)

    # Subarbol division: (c / 4)
    nodo_c = ExprNode('c')
    nodo_4 = ExprNode('4')
    nodo_div = ExprNode('/', nodo_c, nodo_4)

    # Raiz suma principal: ((a + 3) * (b - 2)) + (c / 4)
    raiz = ExprNode('+', nodo_mult, nodo_div)
    return raiz


def preorder_traversal(node: Optional[ExprNode]) -> List[str]:
    """Recorrido en preorden: raiz, subarbol izquierdo, subarbol derecho (notacion prefija)."""
    if node is None:
        return []
    return [node.value] + preorder_traversal(node.left) + preorder_traversal(node.right)


def inorder_traversal(node: Optional[ExprNode], parenthesize: bool = True) -> str:
    """Recorrido en inorden: subarbol izquierdo, raiz, subarbol derecho (notacion infija)."""
    if node is None:
        return ""
    if node.is_leaf():
        return node.value

    left_str = inorder_traversal(node.left, parenthesize)
    right_str = inorder_traversal(node.right, parenthesize)

    if parenthesize:
        return f"({left_str} {node.value} {right_str})"
    return f"{left_str} {node.value} {right_str}"


def postorder_traversal(node: Optional[ExprNode]) -> List[str]:
    """Recorrido en postorden: subarbol izquierdo, subarbol derecho, raiz (notacion postfija)."""
    if node is None:
        return []
    return postorder_traversal(node.left) + postorder_traversal(node.right) + [node.value]


def evaluate_expression_tree(node: Optional[ExprNode], env: Dict[str, float], log_steps: Optional[List[str]] = None) -> float:
    """
    Evalua el arbol de expresion de forma recursiva (recorrido postorden / ascendente).
    No sustituye directamente en la cadena original; computa subarboles.
    """
    if node is None:
        return 0.0

    # Caso base: hoja (operando variable o constante)
    if node.is_leaf():
        if node.value in env:
            val = float(env[node.value])
        else:
            val = float(node.value)
        return val

    # Recorrer subarboles (postorden)
    left_val = evaluate_expression_tree(node.left, env, log_steps)
    right_val = evaluate_expression_tree(node.right, env, log_steps)

    # Aplicar operador en la raiz
    op = node.value
    if op == '+':
        res = left_val + right_val
    elif op == '-':
        res = left_val - right_val
    elif op == '*':
        res = left_val * right_val
    elif op == '/':
        if right_val == 0:
            raise ZeroDivisionError("Division por cero en arbol de expresiones")
        res = left_val / right_val
    else:
        raise ValueError(f"Operador desconocido: {op}")

    if log_steps is not None:
        log_steps.append(f"Evaluar operacion: {left_val} {op} {right_val} = {res}")

    return res


def render_ascii_expr_tree(node: Optional[ExprNode], prefix: str = "", is_tail: bool = True) -> str:
    """Renderiza visualmente el arbol de expresiones binario."""
    if node is None:
        return ""
    branch = "└── " if is_tail else "├── "
    res = prefix + branch + f"[{node.value}]\n"
    child_prefix = prefix + ("    " if is_tail else "│   ")
    children = [c for c in [node.left, node.right] if c is not None]
    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        res += render_ascii_expr_tree(child, child_prefix, is_last)
    return res
