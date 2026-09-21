```markdown
# Taller de árboles, recorridos y complejidad computacional
## Estructuras de datos para el análisis sintáctico descendente

**Curso:** Lenguajes de Programación y Traducción  
**Estudiantes:** Dylan Torres - Juan Gomez - Javier Rosero  
**Fecha:** 22 de septiembre de 2026  

---

## Propósito del taller

Este taller busca afianzar el manejo de los árboles como estructura formal y computacional, ya que resultan indispensables para representar y procesar expresiones durante el análisis sintáctico. A lo largo de los ejercicios se trabaja la representación de relaciones jerárquicas, la identificación de propiedades estructurales, la implementación de recorridos en profundidad y en anchura, la relación directa entre esos recorridos y el funcionamiento de los analizadores descendentes, y el análisis formal de la complejidad temporal y espacial de los algoritmos empleados.

---

## Punto 1. Conceptos y representación de árboles

Partimos del siguiente árbol general, definido mediante relaciones padre-hijo:

| Nodo padre | Nodos hijos |
| :--- | :--- |
| A | B, C, D |
| B | E, F |
| C | G |
| D | H, I |
| F | J |
| H | K, L |

### 1. Dibujo del árbol correspondiente

El árbol tiene su raíz en A y se ramifica hacia abajo hasta completar doce nodos:

```text
               [A]
          /     |     \
        /       |       \
      [B]      [C]      [D]
     /   \      |      /   \
   [E]   [F]   [G]   [H]   [I]
          |         /   \
         [J]       [K]  [L]
```

Visto como árbol jerárquico detallado:

```text
└── [A]
    ├── [B]
    │   ├── [E]
    │   └── [F]
    │       └── [J]
    ├── [C]
    │   └── [G]
    └── [D]
        ├── [H]
        │   ├── [K]
        │   └── [L]
        └── [I]
```

### 2. Componentes y relaciones

- **Raíz:** el nodo A, porque es el único que no tiene padre.
- **Hojas:** E, J, G, K, L e I, ya que ninguno de ellos tiene hijos (grado cero).
- **Nodos internos:** B, C, D, F y H, además de la raíz A, pues todos tienen al menos un hijo.
- **Padre del nodo J:** el nodo F.
- **Ancestros del nodo L:** los nodos que forman el camino ascendente desde L hasta la raíz, es decir, H, D y A.
- **Descendientes del nodo B:** todos los nodos alcanzables hacia abajo desde B, o sea, E, F y J.
- **Hermanos del nodo H:** el nodo I, porque ambos comparten directamente al mismo padre D.

### 3. Grados, profundidad y altura

- **Grado de cada nodo:**
  - grado(A) = 3 (hijos B, C, D)
  - grado(B) = 2 (hijos E, F)
  - grado(C) = 1 (hijo G)
  - grado(D) = 2 (hijos H, I)
  - grado(E) = 0
  - grado(F) = 1 (hijo J)
  - grado(G) = 0
  - grado(H) = 2 (hijos K, L)
  - grado(I) = 0
  - grado(J) = 0
  - grado(K) = 0
  - grado(L) = 0

- **Grado del árbol:** es el grado máximo entre todos los nodos. Aquí es 3, dado por la raíz A.
- **Profundidad de algunos nodos:**
  - profundidad(A) = 0 (nivel raíz)
  - profundidad(F) = 2 (camino A -> B -> F)
  - profundidad(J) = 3 (camino A -> B -> F -> J)
  - profundidad(L) = 3 (camino A -> D -> H -> L)
- **Altura total del árbol:** si se mide por la longitud en aristas del camino más largo desde la raíz hasta la hoja más profunda, la altura es 3. Si se cuenta por número de niveles de nodos, serían 4 (niveles 0, 1, 2 y 3).

### 4. Clasificación y propiedades estructurales

- **¿Es binario?** No. Un árbol binario exige que ningún nodo tenga más de dos hijos, y aquí la raíz A tiene tres (B, C y D).
- **¿Es completo?** No. Un árbol completo de orden m requiere que todos los nodos internos tengan exactamente m hijos y que todas las hojas estén en el mismo nivel terminal. En este caso los grados son dispares (A tiene 3, B y D tienen 2, C y F solo 1) y las hojas se reparten entre los niveles 2 y 3.
- **¿Es balanceado?** No. Hay desbalance entre las ramas laterales y la central: las hojas E, G e I terminan en profundidad 2, mientras que las ramas que llevan a J, K y L llegan hasta profundidad 3.

### Análisis de complejidad

- **Contar las hojas:** cualquier algoritmo debe revisar todos los nodos para comprobar si su lista de hijos está vacía. Como cada nodo se visita una sola vez, la complejidad temporal es lineal, O(n), con n = 12 nodos. La complejidad espacial es O(h), asociada a la altura máxima en la pila de recursión.
- **Calcular la altura:** se recorren recursivamente todos los subárboles para quedarse con el máximo de sus alturas. Esto toma tiempo O(n) y espacio proporcional a la altura, O(h).
- **Buscar un valor que no está en el árbol:** como este árbol general no tiene orden entre hermanos (a diferencia de un árbol binario de búsqueda), no hay forma de podar ramas. Por lo tanto, si el elemento no existe, el algoritmo debe recorrer todos los nodos en el peor caso, con complejidad temporal O(n) y espacial O(h).

---

## Punto 2. Construcción de un árbol de expresiones

Tomemos la siguiente expresión aritmética:

$$(a + 3) \times (b - 2) + \frac{c}{4}$$

### 1. Operandos y operadores

- **Operandos:** las variables a, b, c y los literales 3, 2, 4.
- **Operadores:** la suma interna (+), la resta interna (-), el producto principal (*), el cociente (/) y la suma general (+).
- **Agrupación:** los paréntesis '(' y ')', que fuerzan a que las sumas y restas se ejecuten antes del producto.

### 2. Construcción manual del árbol de expresión

Siguiendo la precedencia y la asociatividad habituales, el operador de menor precedencia que une las dos grandes partes de la expresión es la suma exterior, así que actúa como raíz. A la izquierda queda el producto de las expresiones entre paréntesis, y a la derecha la división de c entre 4:

```text
               [ + ]
             /       \
          [ * ]       [ / ]
         /     \      /   \
       [+]     [-]  [c]   [4]
      /   \   /   \
    [a]   [3][b]  [2]
```

Como estructura jerárquica con nodos hijos:

```text
└── [+]
    ├── [*]
    │   ├── [+]
    │   │   ├── [a]
    │   │   └── [3]
    │   └── [-]
    │       ├── [b]
    │       └── [2]
    └── [/]
        ├── [c]
        └── [4]
```

### 3. Resultado de los recorridos

- **Preorden (raíz, subárbol izquierdo, subárbol derecho):**  
  `+ * + a 3 - b 2 / c 4`
- **Inorden (subárbol izquierdo, raíz, subárbol derecho, con paréntesis):**  
  `(((a + 3) * (b - 2)) + (c / 4))`
- **Postorden (subárbol izquierdo, subárbol derecho, raíz):**  
  `a 3 + b 2 - * c 4 / +`

### 4. Correspondencia entre recorridos y notaciones

- El recorrido en **preorden** produce la **notación prefija** (históricamente llamada notación polaca), donde cada operador va antes que sus operandos.
- El recorrido en **inorden** produce la **notación infija**, el estándar del álgebra, que necesita paréntesis para no perder la precedencia.
- El recorrido en **postorden** produce la **notación postfija** (notación polaca inversa o RPN), donde los operandos van antes que su operador.

### 5. Evaluación del árbol para a = 5, b = 8 y c = 12

La evaluación se hace ascendiendo por el árbol (postorden), resolviendo los valores intermedios paso a paso:

- Subárbol izquierdo inferior: la suma con a = 5 y 3 da 5 + 3 = 8.
- Subárbol central inferior: la resta con b = 8 y 2 da 8 - 2 = 6.
- Nodo producto: multiplica los dos resultados anteriores, 8 * 6 = 48.
- Subárbol derecho: la división con c = 12 y 4 da 12 / 4 = 3.
- Raíz: suma ambos lados, 48 + 3 = 51.

El valor final obtenido al recorrer el árbol es **51**.

### Preguntas de análisis

#### 1. ¿Por qué la evaluación de una expresión puede hacerse con un recorrido en postorden?
Porque una operación binaria no puede aplicarse hasta tener disponibles los valores de sus dos argumentos. El recorrido en postorden sigue una estrategia ascendente (*bottom-up*): primero procesa por completo el subárbol izquierdo, luego el derecho, y solo entonces visita el operador de la raíz. Esto encaja con el funcionamiento natural de las máquinas basadas en pila, donde los operandos se apilan y la operación los desapila para calcular el resultado parcial.

#### 2. ¿Cuál es la complejidad temporal de evaluar el árbol?
Es lineal, O(n), con n el número total de nodos (aquí n = 11). Cada nodo se visita un número acotado y constante de veces, y cada operación aritmética elemental se ejecuta en O(1).

#### 3. ¿Cuál es la complejidad espacial del recorrido recursivo en función de h?
Es O(h), con h la altura del árbol de expresión. La profundidad de la pila de llamadas en memoria durante la recursión equivale en todo momento a la longitud de la rama activa desde la raíz hasta la hoja actual.

#### 4. ¿Qué pasa con el consumo de memoria si el árbol está completamente desbalanceado?
Si el árbol se degenera en una estructura lineal (parecida a una lista enlazada), la altura h deja de ser logarítmica y pasa a ser proporcional al número de nodos, h = O(n). Como consecuencia, el consumo de memoria de la pila sube a O(n) y crece el riesgo de sufrir un desbordamiento de pila (*stack overflow*) en expresiones complejas.

---

## Punto 3. Recorridos en profundidad: DFS

Se implementó en Python una estructura `TreeNode` pensada para modelar árboles generales con una lista dinámica de hijos, junto con las variantes y utilidades de exploración en profundidad solicitadas.

### Algoritmos implementados en `arbol_general.py`

- **DFS recursivo en preorden:** procesa el nodo actual y llama recursivamente al método sobre cada hijo, de izquierda a derecha.
- **DFS iterativo con pila:** usa una estructura LIFO (`stack`). Para conservar el orden de visita de izquierda a derecha, los hijos se insertan en la pila en orden inverso.
- **Búsqueda de un valor mediante DFS:** recorre en profundidad y se detiene justo cuando encuentra el valor buscado, contando cuántos nodos ha visitado hasta ese momento.
- **Conteo de hojas mediante DFS:** recorre el árbol y suma uno cada vez que encuentra un nodo cuya lista de hijos está vacía.
- **Cálculo de altura mediante DFS:** halla la distancia máxima desde el nodo actual hasta cualquier hoja alcanzable en su descendencia.

### Evidencias de ejecución sobre el árbol del Punto 1

- **Secuencia de visita con DFS recursivo:**  
  `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L -> I`
- **Secuencia de visita con DFS iterativo:**  
  `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L -> I`  
  *(Ambos métodos producen exactamente el mismo orden de visita).*
- **Total de hojas contadas:** 6 (E, J, G, K, L, I).
- **Altura calculada del árbol:** 3 aristas (4 niveles).

### Pruebas de búsqueda requeridas

- **Prueba 1: búsqueda de un valor cercano a la raíz ('B')**
  - Orden de visita observado: `A -> B`
  - Valor encontrado: Sí
  - Nodos visitados: 2
  - Hojas en el árbol: 6
  - Altura del árbol: 3
- **Prueba 2: búsqueda de un valor del último nivel ('L')**
  - Orden de visita observado: `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L`
  - Valor encontrado: Sí
  - Nodos visitados: 11
  - Hojas en el árbol: 6
  - Altura del árbol: 3
- **Prueba 3: búsqueda de un valor que no existe ('Z')**
  - Orden de visita observado: `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L -> I`
  - Valor encontrado: No
  - Nodos visitados: 12 (exploración exhaustiva)
  - Hojas en el árbol: 6
  - Altura del árbol: 3

### Análisis de complejidad

La tabla de complejidad para las operaciones basadas en DFS queda así:

| Operación con DFS | Mejor caso | Peor caso | Espacio |
| :--- | :--- | :--- | :--- |
| Recorrer todo el árbol | O(n) | O(n) | O(h) |
| Buscar un valor | O(1) (si el valor está en la raíz) | O(n) (si no existe o es el último explorado) | O(h) |
| Contar hojas | O(n) | O(n) | O(h) |
| Calcular la altura | O(n) | O(n) | O(h) |

### Comparación de uso de memoria

- **DFS recursivo frente a DFS iterativo:** ambos tienen la misma cota asintótica de memoria, O(h), pero difieren en dónde se ubica y qué costos trae. La versión recursiva usa la pila de ejecución del sistema (*call stack*), que guarda marcos de activación con variables locales y punteros de retorno; por eso, en árboles muy profundos, puede provocar desbordamiento de pila. La versión iterativa, en cambio, maneja una pila explícita en memoria dinámica (*heap*), lo que da más control y resistencia ante árboles profundos.
- **Árbol balanceado frente a árbol desbalanceado:** en una estructura balanceada de grado k, la altura se comporta como h = O(log n), lo que mantiene la memoria muy contenida. En cambio, en un árbol completamente desbalanceado donde cada nodo tiene un único descendiente, la altura llega a h = O(n), obligando a la pila a retener todos los nodos del árbol a la vez.

---

## Punto 4. Recorrido en anchura: BFS

Se implementó el recorrido por niveles con una cola basada en FIFO (`collections.deque`), garantizando que los nodos de un nivel se atiendan antes de explorar los descendientes del siguiente nivel.

### Actividades implementadas en `arbol_general.py`

- Recepción de la raíz del árbol.
- Exploración sistemática por niveles contiguos.
- Registro y presentación de la secuencia total de visita.
- Agrupación estructurada de los nodos de cada nivel.
- Búsqueda de elementos con reporte del nivel donde se encuentra y del total de nodos inspeccionados.

### Evidencias de ejecución sobre el árbol del Punto 1

- **Orden de visita global con BFS:**  
  `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L`

- **Nodos agrupados por nivel:**
  - Nivel 0: A
  - Nivel 1: B, C, D
  - Nivel 2: E, F, G, H, I
  - Nivel 3: J, K, L

### Pruebas de búsqueda con el formato establecido

#### Prueba 1: valor cercano a la raíz ('B')
```text
Nivel 0: A
Nivel 1: B, C, D
Nivel 2: E, F, G, H, I
Nivel 3: J, K, L
Valor buscado: B
Resultado: encontrado
Nivel del valor: 1
Nodos visitados: 2
```

#### Prueba 2: valor del último nivel ('L')
```text
Nivel 0: A
Nivel 1: B, C, D
Nivel 2: E, F, G, H, I
Nivel 3: J, K, L
Valor buscado: L
Resultado: encontrado
Nivel del valor: 3
Nodos visitados: 12
```

#### Prueba 3: valor que no existe ('Z')
```text
Nivel 0: A
Nivel 1: B, C, D
Nivel 2: E, F, G, H, I
Nivel 3: J, K, L
Valor buscado: Z
Resultado: no encontrado
Nivel del valor: N/A
Nodos visitados: 12
```

### Preguntas de análisis

#### 1. ¿Por qué BFS requiere una cola?
Porque la cola funciona con disciplina FIFO (*First-In, First-Out*). Esa propiedad garantiza que todos los nodos descubiertos en el nivel k se retiren y analicen por completo antes de empezar a procesar los del nivel k + 1, que se fueron agregando al final de la estructura mientras se exploraba el nivel anterior.

#### 2. ¿Qué pasaría si se usara una pila?
Si se cambia la cola por una pila (disciplina LIFO), el orden de extracción favorecería al último elemento agregado. Como resultado, el algoritmo dejaría de recorrer los nodos por estratos horizontales y se convertiría de inmediato en una exploración en profundidad (DFS iterativo).

#### 3. ¿Cuál es la complejidad temporal de BFS?
Es O(n). Cada nodo entra a la cola una única vez y sale exactamente una vez, y sus enlaces de ramificación se recorren en tiempo proporcional a su grado, lo que sumado sobre todos los vértices equivale al total de nodos del árbol.

#### 4. ¿Cuál es su complejidad espacial?
Es O(w), con w el ancho máximo del árbol (la mayor cantidad de nodos en un nivel). En el peor caso (un árbol de altura 1 donde la raíz tiene n - 1 hijos), la cola debe retener casi todos los elementos, con un consumo espacial de O(n).

#### 5. ¿Qué recorrido puede consumir más memoria en un árbol ancho: DFS o BFS?
En un árbol ancho, **BFS** consume bastante más memoria que DFS. La razón es que BFS debe mantener encolados a la vez todos los nodos del nivel más populoso (O(w)). DFS, en cambio, solo necesita conservar la rama activa desde la raíz hasta una hoja, con un espacio O(h) que en árboles anchos resulta muy pequeño comparado con el ancho w.

#### 6. Si se busca el nodo menos profundo que cumpla una condición, ¿qué recorrido conviene más?
**BFS** es claramente el más apropiado. Como explora los nodos en estricto orden no decreciente de profundidad (nivel 0, luego nivel 1, etc.), el primer nodo que cumpla el criterio tiene garantizado ser el de menor distancia a la raíz en número de aristas. DFS, en cambio, podría internarse primero por una rama muy profunda y encontrar una solución tardía e ineficiente.

---

## Punto 5. Aplicación al análisis sintáctico

Consideremos la siguiente gramática libre de contexto simplificada:

$$E \to T E'$$
$$E' \to + T E' \mid \epsilon$$
$$T \to F T'$$
$$T' \to * F T' \mid \epsilon$$
$$F \to (E) \mid id$$

Cadena de entrada para el análisis:

$$\text{id} + \text{id} * \text{id}$$

### 1. Construcción paso a paso del árbol sintáctico (analizador descendente)

Un analizador descendente predictivo (LL) deriva la cadena aplicando derivaciones por la izquierda a partir del símbolo inicial E:

- Derivación 1: $E \Rightarrow T E'$
- Derivación 2: $\Rightarrow F T' E'$
- Derivación 3: $\Rightarrow \text{id}_1 T' E'$ (empareja el primer terminal `id`)
- Derivación 4: $\Rightarrow \text{id}_1 \epsilon_1 E'$ (aplica la producción vacía $T' \to \epsilon$)
- Derivación 5: $\Rightarrow \text{id}_1 \epsilon_1 + T E'$ (expande $E' \to + T E'$, empareja el terminal `+`)
- Derivación 6: $\Rightarrow \text{id}_1 \epsilon_1 + F T' E'$
- Derivación 7: $\Rightarrow \text{id}_1 \epsilon_1 + \text{id}_2 T' E'$ (empareja el segundo terminal `id`)
- Derivación 8: $\Rightarrow \text{id}_1 \epsilon_1 + \text{id}_2 * F T' E'$ (expande $T' \to * F T'$, empareja el terminal `*`)
- Derivación 9: $\Rightarrow \text{id}_1 \epsilon_1 + \text{id}_2 * \text{id}_3 T' E'$ (empareja el tercer terminal `id`)
- Derivación 10: $\Rightarrow \text{id}_1 \epsilon_1 + \text{id}_2 * \text{id}_3 \epsilon_2 E'$ (aplica $T' \to \epsilon$)
- Derivación 11: $\Rightarrow \text{id}_1 \epsilon_1 + \text{id}_2 * \text{id}_3 \epsilon_2 \epsilon_3$ (aplica $E' \to \epsilon$, completando la cadena)

### 2. Numeración de los nodos según su orden de creación

En el análisis sintáctico descendente, los nodos se crean a medida que se invocan y expanden las subrutinas de parsing. El orden cronológico de creación de los 19 nodos del árbol es:

```text
└── E [ID:1, NoTerminal]
    ├── T [ID:2, NoTerminal]
    │   ├── F [ID:3, NoTerminal]
    │   │   └── id [ID:4, Terminal]
    │   └── T' [ID:5, NoTerminal]
    │       └── ε [ID:6, Epsilon]
    └── E' [ID:7, NoTerminal]
        ├── + [ID:8, Terminal]
        ├── T [ID:9, NoTerminal]
        │   ├── F [ID:10, NoTerminal]
        │   │   └── id [ID:11, Terminal]
        │   └── T' [ID:12, NoTerminal]
        │       ├── * [ID:13, Terminal]
        │       ├── F [ID:14, NoTerminal]
        │       │   └── id [ID:15, Terminal]
        │       └── T' [ID:16, NoTerminal]
        │           └── ε [ID:17, Epsilon]
        └── E' [ID:18, NoTerminal]
            └── ε [ID:19, Epsilon]
```

Detalle secuencial de creación:
- Nodo #01: símbolo E (No terminal)
- Nodo #02: símbolo T (No terminal)
- Nodo #03: símbolo F (No terminal)
- Nodo #04: símbolo id (Terminal)
- Nodo #05: símbolo T' (No terminal)
- Nodo #06: símbolo ε (Producción vacía)
- Nodo #07: símbolo E' (No terminal)
- Nodo #08: símbolo + (Terminal)
- Nodo #09: símbolo T (No terminal)
- Nodo #10: símbolo F (No terminal)
- Nodo #11: símbolo id (Terminal)
- Nodo #12: símbolo T' (No terminal)
- Nodo #13: símbolo * (Terminal)
- Nodo #14: símbolo F (No terminal)
- Nodo #15: símbolo id (Terminal)
- Nodo #16: símbolo T' (No terminal)
- Nodo #17: símbolo ε (Producción vacía)
- Nodo #18: símbolo E' (No terminal)
- Nodo #19: símbolo ε (Producción vacía)

### 3. Recorridos sobre el árbol sintáctico

- **DFS en Preorden:**  
  `E (#1) -> T (#2) -> F (#3) -> id (#4) -> T' (#5) -> ε (#6) -> E' (#7) -> + (#8) -> T (#9) -> F (#10) -> id (#11) -> T' (#12) -> * (#13) -> F (#14) -> id (#15) -> T' (#16) -> ε (#17) -> E' (#18) -> ε (#19)`
- **DFS en Postorden:**  
  `id (#4) -> F (#3) -> ε (#6) -> T' (#5) -> T (#2) -> + (#8) -> id (#11) -> F (#10) -> * (#13) -> id (#15) -> F (#14) -> ε (#17) -> T' (#16) -> T' (#12) -> T (#9) -> ε (#19) -> E' (#18) -> E' (#7) -> E (#1)`
- **BFS por niveles:**  
  `E (#1) -> T (#2) -> E' (#7) -> F (#3) -> T' (#5) -> + (#8) -> T (#9) -> E' (#18) -> id (#4) -> ε (#6) -> F (#10) -> T' (#12) -> ε (#19) -> id (#11) -> * (#13) -> F (#14) -> T' (#16) -> id (#15) -> ε (#17)`

### 4. Información que aporta cada recorrido

- **Preorden:** refleja la secuencia temporal y lógica en la que el analizador descendente va tomando decisiones gramaticales. Muestra qué regla de producción se elige y en qué momento se anticipa la coincidencia de cada componente léxico entrante.
- **Postorden:** refleja el orden de síntesis y reducción semántica. Como visita a los hijos antes que al padre, es el recorrido ideal para calcular atributos sintetizados, hacer verificación de tipos en el análisis semántico y generar código intermedio.
- **BFS:** descompone el árbol en niveles horizontales de abstracción sintáctica, lo que permite examinar cómo se expanden a la vez las construcciones del lenguaje según su profundidad en la gramática.

### 5. Comparación entre el orden de creación de nodos y el recorrido en preorden

Si comparamos los identificadores secuenciales de creación con el recorrido DFS en preorden, aparece una **coincidencia matemática perfecta**: la secuencia de visita en preorden es exactamente `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19`. Esto demuestra que el analizador sintáctico descendente construye el árbol con una estrategia de exploración en profundidad guiada por la derivación por la izquierda.

### 6. Representación de la precedencia de operadores en el árbol

La precedencia de la multiplicación sobre la suma queda codificada directamente en la topología estratificada de la gramática. En la estructura del árbol:
- La suma se introduce en el nodo E' (a menor profundidad, nivel 2).
- La multiplicación se introduce en el nodo T' descendiente del segundo T (a mayor profundidad, niveles 3 y 4).
Gracias a esta disposición, el producto queda encapsulado en un subárbol más interno. Durante cualquier procesamiento ascendente o de reducción semántica, el producto `id * id` debe calcularse por completo antes de que su resultado pueda sumarse con el primer `id`. Así se garantiza que la multiplicación tenga mayor jerarquía que la suma sin necesidad de paréntesis adicionales.

### 7. Algoritmo para métricas del árbol sintáctico

Se programó una función en `arbol_sintactico.py` que recorre el árbol y calcula las siguientes propiedades estructurales:
- **Nodos totales:** 19
- **Nodos terminales (tokens reales de entrada):** 5 (`id`, `+`, `id`, `*`, `id`)
- **Nodos no terminales (estructuras sintácticas intermedias):** 11 (`E`, `T`, `F`, `T'`, `E'`, etc.)
- **Producciones vacías ($\epsilon$):** 3 (derivaciones vacías para terminar las listas $T'$ y $E'$)
- **Altura del árbol (medida por aristas):** 5 aristas (6 niveles de nodos)

---

## Comparación final

La siguiente tabla resume la comparación entre las dos estrategias de recorrido fundamentales:

| Criterio | DFS | BFS |
| :--- | :--- | :--- |
| Estructura auxiliar | Pila (pila de llamadas del sistema o estructura explícita LIFO) | Cola (estructura FIFO) |
| Orden de exploración | Profundidad vertical (avanza hasta la hoja antes de retroceder) | Anchura horizontal (recorre nivel por nivel) |
| Complejidad temporal | O(n) | O(n) |
| Complejidad espacial | O(h), con h la altura del árbol | O(w), con w el ancho máximo de un nivel |
| Conveniente para evaluar expresiones | Sí (mediante el recorrido postorden) | No (no respeta la precedencia entre subárboles) |
| Conveniente para recorrer por niveles | No | Sí (es su comportamiento inherente) |
| Comportamiento en árboles profundos | Puede requerir memoria O(n) o provocar desbordamiento de pila | Eficiente en memoria si el ancho de cada nivel es reducido |
| Comportamiento en árboles anchos | Muy eficiente en memoria, pues la altura h se mantiene reducida | Muy ineficiente en memoria, pues la cola almacena todo el nivel ancho |

---

## Conclusión final

Los árboles y sus recorridos son la columna vertebral del análisis sintáctico descendente, porque dan la estructura formal necesaria para verificar, organizar y evaluar el código fuente. En este paradigma, el proceso de derivación por la izquierda modela directamente la construcción del árbol desde el símbolo inicial en la raíz hacia las hojas, que corresponden a los componentes léxicos leídos. El recorrido en profundidad (DFS) en preorden no es solo una técnica de exploración: es el mecanismo operativo exacto con el que el analizador descubre producciones, expande los símbolos no terminales y anticipa los terminales esperados. El recorrido en postorden, por su parte, resulta clave en la fase de síntesis semántica, pues asegura que todos los subárboles de una expresión estén previamente validados y computados antes de aplicar los operadores principales. Y entender el recorrido en anchura (BFS) permite inspeccionar la jerarquía por capas y optimizar la recuperación ante errores. Sin la abstracción jerárquica de los árboles y la disciplina algorítmica de sus recorridos, sería inviable transformar flujos lineales de texto en representaciones lógicas analizables, estructuradas y eficientes dentro de un compilador.

---

## Instrucciones de ejecución

Para compilar y ejecutar de forma automatizada las demostraciones computacionales de los cinco puntos:

```bash
cd "/home/Xavi/Escritorio/Trabajos/Materias/Lenguajes de Programacion y Transduccion/Corte2/Sintactico22-09"

# Ejecutar el programa completo mediante el Makefile
make run

# O ejecutar directamente mediante Python
python3 main.py
```
