# Taller de árboles, recorridos y complejidad computacional
## Estructuras de datos para el análisis sintáctico descendente

**Curso:** Lenguajes de Programación y Traducción  
**Estudiantes:** Dylan Torres - Juan Gomez - Javier Rosero  
**Fecha:** 22 de septiembre de 2026  

---

## Propósito del taller

Fortalecer el manejo de los árboles como estructura formal y computacional indispensable para representar y procesar expresiones durante el análisis sintáctico. Mediante el desarrollo de este taller se aborda la representación de relaciones jerárquicas, la identificación de propiedades estructurales, la implementación de recorridos en profundidad y en anchura, la vinculación directa de dichos recorridos con el funcionamiento de los analizadores descendentes y el análisis formal de la complejidad temporal y espacial de los algoritmos empleados.

---

## Punto 1. Conceptos y representación de árboles

Se considera el árbol general definido mediante las siguientes relaciones padre-hijo:

| Nodo padre | Nodos hijos |
| :--- | :--- |
| A | B, C, D |
| B | E, F |
| C | G |
| D | H, I |
| F | J |
| H | K, L |

### 1. Dibujo del árbol correspondiente

El árbol presenta una estructura jerárquica con raíz en el nodo A, ramificándose hacia abajo con doce nodos en total:

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

En formato de árbol jerárquico detallado:

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

### 2. Identificación de componentes y relaciones

- **Raíz:** El nodo A, por ser el único nodo del árbol que carece de nodo padre.
- **Hojas:** Los nodos E, J, G, K, L e I, debido a que su conjunto de hijos se encuentra vacío (grado cero).
- **Nodos internos:** Los nodos B, C, D, F y H, además de la raíz A, ya que poseen al menos un hijo.
- **Padre del nodo J:** El nodo F.
- **Ancestros del nodo L:** El conjunto de nodos que integran el camino ascendente desde L hacia la raíz, correspondientes a H, D y A.
- **Descendientes del nodo B:** Todos los nodos alcanzables hacia abajo a partir de B, conformados por E, F y J.
- **Hermanos del nodo H:** El nodo I, puesto que ambos comparten de manera directa al mismo nodo padre D.

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

- **Grado del árbol:** Corresponde al grado máximo entre todos sus nodos. En este caso, el grado del árbol es 3, determinado por la raíz A.
- **Profundidad de nodos específicos:**
  - profundidad(A) = 0 (nivel raíz)
  - profundidad(F) = 2 (camino A -> B -> F)
  - profundidad(J) = 3 (camino A -> B -> F -> J)
  - profundidad(L) = 3 (camino A -> D -> H -> L)
- **Altura total del árbol:** Medida convencionalmente por la longitud en aristas del camino más largo desde la raíz hasta la hoja más profunda, la altura es 3 (o 4 si se computa en número de niveles de nodos, correspondientes a los niveles 0, 1, 2 y 3).

### 4. Clasificación y propiedades estructurales

- **¿Es binario?:** No. Un árbol binario impone que ningún nodo posea más de dos hijos. En este caso, el nodo raíz A posee grado 3 al tener como hijos a B, C y D.
- **¿Es completo?:** No. Un árbol completo de orden m requiere que todos los nodos internos presenten exactamente m hijos y que todas las hojas residan estrictamente en el mismo nivel terminal. En esta estructura, los nodos internos presentan grados dispares (A tiene 3, B y D tienen 2, mientras C y F tienen únicamente 1) y las hojas se distribuyen entre los niveles 2 y 3.
- **¿Es balanceado?:** No. Existe un desbalance entre las ramas laterales y centrales: las hojas E, G e I culminan a profundidad 2, mientras que las ramas que conducen a J, K y L descienden hasta la profundidad 3.

### Análisis de complejidad

- **Contar las hojas:** Para contabilizar las hojas, cualquier algoritmo debe inspeccionar la totalidad de los nodos para evaluar si su lista de descendientes está vacía. Al visitar cada nodo exactamente una vez, la complejidad temporal es lineal, es decir, O(n), donde n representa los 12 nodos de la estructura. La complejidad espacial corresponde a O(h), ligada a la altura máxima almacenada en la pila de recursión.
- **Calcular la altura:** Requiere recorrer recursivamente todos los subárboles para computar el máximo de sus alturas respectivas. Este recorrido exhaustivo toma tiempo O(n) y requiere un espacio proporcional a la altura O(h).
- **Buscar un valor que no se encuentra en el árbol:** Dado que este árbol general no posee un orden relacional entre hermanos (a diferencia de un árbol binario de búsqueda), no existe un criterio de poda que permita descartar ramas. Por consiguiente, ante un elemento inexistente, el algoritmo está obligado a explorar todos los nodos del árbol en el peor caso, resultando en una complejidad temporal de O(n) y una complejidad espacial de O(h).

---

## Punto 2. Construcción de un árbol de expresiones

Se considera la siguiente expresión aritmética:

$$(a + 3) \times (b - 2) + \frac{c}{4}$$

### 1. Identificación de operandos y operadores

- **Operandos:** Las variables simbólicas a, b, c y los valores literales numéricos 3, 2, 4.
- **Operadores:** La suma interna (+), la resta interna (-), el producto principal entre términos (*), el cociente (/), y la suma general (+).
- **Elementos de agrupación:** Los paréntesis curvos '(' y ')', cuya función es forzar que las operaciones de adición y sustracción se ejecuten con anterioridad al producto.

### 2. Construcción manual del árbol de expresión

Siguiendo la precedencia matemática y la asociatividad convencional, el operador de menor precedencia que une las dos grandes partes de la expresión es la suma exterior, por lo que actúa como la raíz del árbol. A la izquierda se sitúa el producto de las expresiones entre paréntesis, y a la derecha la división de c entre 4:

```text
               [ + ]
             /       \
          [ * ]       [ / ]
         /     \      /   \
       [+]     [-]  [c]   [4]
      /   \   /   \
    [a]   [3][b]  [2]
```

En estructura jerárquica con indicación de nodos hijos:

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
- **Inorden (subárbol izquierdo, raíz, subárbol derecho con parentización requerida):**  
  `(((a + 3) * (b - 2)) + (c / 4))`
- **Postorden (subárbol izquierdo, subárbol derecho, raíz):**  
  `a 3 + b 2 - * c 4 / +`

### 4. Correspondencia de recorridos y notaciones

- El recorrido en **preorden** genera la **notación prefija** (denominada históricamente notación polaca), donde cada operador precede a sus operandos.
- El recorrido en **inorden** genera la **notación infija**, que es el estándar habitual del álgebra y requiere paréntesis para preservar ambigüedades de precedencia.
- El recorrido en **postorden** genera la **notación postfija** (notación polaca inversa o RPN), donde los operandos anteceden al operador correspondiente.

### 5. Evaluación del árbol para a = 5, b = 8 y c = 12

La evaluación se efectúa recorriendo el árbol de forma ascendente (postorden), resolviendo progresivamente los valores de los nodos intermedios:

- Evaluación del subárbol izquierdo inferior:  
  nodo suma con a = 5 y 3 resulta en 5 + 3 = 8.
- Evaluación del subárbol central inferior:  
  nodo resta con b = 8 y 2 resulta en 8 - 2 = 6.
- Evaluación del nodo producto:  
  multiplica los resultados anteriores: 8 * 6 = 48.
- Evaluación del subárbol derecho:  
  nodo división con c = 12 y 4 resulta en 12 / 4 = 3.
- Evaluación de la raíz:  
  suma los resultados de ambos lados: 48 + 3 = 51.

El valor final computado mediante el recorrido del árbol es **51**.

### Preguntas de análisis

#### 1. ¿Por qué la evaluación de una expresión puede realizarse mediante un recorrido en postorden?
Porque una operación binaria no puede aplicarse hasta que los valores de sus dos argumentos estén disponibles. El recorrido en postorden obedece a una estrategia de evaluación ascendente (*bottom-up*): procesa primero de forma íntegra el subárbol izquierdo y luego el subárbol derecho antes de visitar el operador en la raíz. Esto coincide con el funcionamiento natural de las máquinas basadas en pila, donde los operandos se apilan secuencialmente y la operación los desapila para calcular el resultado parcial.

#### 2. ¿Cuál es la complejidad temporal de evaluar el árbol?
Es de orden lineal, O(n), donde n representa el número total de nodos (en este caso n = 11). Cada nodo del árbol se visita un número acotado y constante de veces, y cada cálculo elemental aritmético se ejecuta en tiempo O(1).

#### 3. ¿Cuál es la complejidad espacial del recorrido recursivo en función de h?
Es de orden O(h), donde h es la altura del árbol de expresión. La profundidad de la pila de llamadas en memoria durante la recursión equivale en todo instante a la longitud de la rama activa desde la raíz hasta la hoja actual.

#### 4. ¿Qué ocurre con el consumo de memoria si el árbol está completamente desbalanceado?
Si el árbol se degenera en una estructura lineal (semejante a una lista enlazada), la altura h deja de ser logarítmica y pasa a ser proporcional a la cantidad de nodos, alcanzando h = O(n). En consecuencia, el consumo de memoria de la pila se incrementa drásticamente a O(n), elevando el riesgo de incurrir en un desbordamiento de pila (*stack overflow*) para expresiones complejas.

---

## Punto 3. Recorridos en profundidad: DFS

Se implementó en Python una estructura de datos `TreeNode` orientada a modelar árboles generales con una lista dinámica de hijos, junto con las variantes y utilidades de exploración en profundidad solicitadas.

### Algoritmos implementados en `arbol_general.py`

- **DFS recursivo en preorden:** Procesa el nodo actual e invoca recursivamente el método sobre cada uno de sus hijos en orden de izquierda a derecha.
- **DFS iterativo con pila:** Emplea una estructura LIFO (`stack`). Para preservar la convención de visitar los hijos de izquierda a derecha, los nodos hijos se insertan en la pila en orden inverso.
- **Búsqueda de un valor mediante DFS:** Realiza un recorrido en profundidad y se detiene en el momento exacto en que coincide el valor buscado, computando el número de nodos visitados hasta ese instante.
- **Conteo de hojas mediante DFS:** Recorre el árbol y acumula una unidad cada vez que encuentra un nodo cuya lista de hijos tiene longitud cero.
- **Cálculo de altura mediante DFS:** Determina la distancia máxima desde el nodo actual hacia cualquier hoja alcanzable en su descendencia.

### Evidencias de ejecución sobre el árbol del Punto 1

- **Secuencia de visita obtenida con DFS recursivo:**  
  `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L -> I`
- **Secuencia de visita obtenida con DFS iterativo:**  
  `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L -> I`  
  *(Ambos métodos producen exactamente el mismo orden de visita).*
- **Total de nodos hoja contabilizados:** 6 hojas (E, J, G, K, L, I).
- **Altura calculada del árbol:** 3 aristas (4 niveles).

### Pruebas de búsqueda requeridas

- **Prueba 1: Búsqueda de un valor cercano a la raíz ('B')**
  - Orden de visita observado: `A -> B`
  - Valor encontrado: Sí
  - Cantidad de nodos visitados: 2
  - Hojas en el árbol: 6
  - Altura del árbol: 3
- **Prueba 2: Búsqueda de un valor del último nivel ('L')**
  - Orden de visita observado: `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L`
  - Valor encontrado: Sí
  - Cantidad de nodos visitados: 11
  - Hojas en el árbol: 6
  - Altura del árbol: 3
- **Prueba 3: Búsqueda de un valor que no existe ('Z')**
  - Orden de visita observado: `A -> B -> E -> F -> J -> C -> G -> D -> H -> K -> L -> I`
  - Valor encontrado: No
  - Cantidad de nodos visitados: 12 (exploración exhaustiva)
  - Hojas en el árbol: 6
  - Altura del árbol: 3

### Análisis de complejidad

A continuación se detalla la tabla de complejidad para las operaciones basadas en DFS:

| Operación con DFS | Mejor caso | Peor caso | Espacio |
| :--- | :--- | :--- | :--- |
| Recorrer todo el árbol | O(n) | O(n) | O(h) |
| Buscar un valor | O(1) (cuando el valor está en la raíz) | O(n) (cuando el valor no existe o es el último explorado) | O(h) |
| Contar hojas | O(n) | O(n) | O(h) |
| Calcular la altura | O(n) | O(n) | O(h) |

### Comparación de uso de memoria

- **DFS recursivo frente a DFS iterativo:** Ambos presentan la misma cota asintótica de memoria, O(h), pero difieren en la ubicación y los costos asociados. La versión recursiva utiliza la pila de ejecución del sistema (*call stack*), la cual almacena marcos de activación con variables locales y punteros de retorno; por ello, ante árboles excesivamente profundos, es susceptible a generar excepciones de desbordamiento de pila. En cambio, la versión iterativa gestiona una pila explícita en la memoria dinámica (*heap*), lo que proporciona mayor control y resistencia a fallos de desbordamiento en árboles profundos.
- **Árbol balanceado frente a árbol desbalanceado:** En una estructura balanceada de grado k, la altura se comporta como h = O(log n), lo cual mantiene la ocupación en memoria muy contenida. Por el contrario, en un árbol completamente desbalanceado donde cada nodo posee un único descendiente, la altura alcanza h = O(n), forzando a la pila a retener la totalidad de los nodos del árbol de manera simultánea.

---

## Punto 4. Recorrido en anchura: BFS

Se implementó el algoritmo de recorrido por niveles utilizando una cola basada en la estructura FIFO (`collections.deque`), garantizando que los nodos de un nivel determinado sean atendidos antes de explorar los descendientes del siguiente nivel.

### Actividades implementadas en `arbol_general.py`

- Recepción de la raíz del árbol.
- Exploración sistemática por niveles contiguos.
- Registro y presentación de la secuencia total de visita.
- Agrupación estructurada de los nodos pertenecientes a cada nivel.
- Búsqueda de elementos con reporte del nivel de localización y total de nodos inspeccionados.

### Evidencias de ejecución sobre el árbol del Punto 1

- **Orden de visita global con BFS:**  
  `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L`

- **Nodos agrupados por nivel:**
  - Nivel 0: A
  - Nivel 1: B, C, D
  - Nivel 2: E, F, G, H, I
  - Nivel 3: J, K, L

### Pruebas de búsqueda con el formato establecido

#### Prueba 1: Valor cercano a la raíz ('B')
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

#### Prueba 2: Valor del último nivel ('L')
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

#### Prueba 3: Valor que no existe ('Z')
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
Porque una cola opera bajo la disciplina FIFO (*First-In, First-Out*). Esta propiedad asegura que todos los nodos descubiertos en el nivel k sean retirados y analizados de forma rigurosa antes de que se comiencen a procesar los nodos del nivel k + 1, los cuales se fueron agregando al final de la estructura durante la exploración del nivel anterior.

#### 2. ¿Qué sucedería si se utilizara una pila?
Si la cola se sustituye por una pila (disciplina LIFO), el orden de extracción favorecería al elemento incorporado más recientemente. Como consecuencia, el algoritmo dejaría de recorrer los nodos por estratos horizontales y se transformaría de inmediato en una exploración en profundidad (DFS iterativo).

#### 3. ¿Cuál es la complejidad temporal de BFS?
La complejidad temporal es O(n). Cada nodo entra a la cola una única vez y sale exactamente una vez, y sus correspondientes enlaces de ramificación se recorren en tiempo proporcional a su grado, lo que sumado sobre todos los vértices equivale al total de nodos del árbol.

#### 4. ¿Cuál es su complejidad espacial?
La complejidad espacial es O(w), donde w es el ancho máximo del árbol (la mayor cantidad de nodos presentes en cualquier nivel individual). En el peor de los casos (un árbol de altura 1 donde la raíz posee n - 1 hijos), la cola debe retener casi la totalidad de los elementos, resultando en un consumo espacial de O(n).

#### 5. ¿Cuál recorrido puede consumir más memoria en un árbol ancho: DFS o BFS?
En un árbol ancho, el recorrido **BFS** consume notablemente más memoria que DFS. Esto se debe a que BFS se ve obligado a mantener encolados de manera simultánea a todos los nodos del nivel más populoso (O(w)). En contraste, DFS únicamente necesita preservar la rama activa desde la raíz hasta una hoja, requiriendo un espacio O(h) que en árboles anchos es extremadamente pequeño comparado con el ancho w.

#### 6. Si se busca el nodo menos profundo que cumpla una condición, ¿qué recorrido resulta más apropiado?
El recorrido **BFS** resulta indiscutiblemente el más apropiado. Dado que explora los nodos en estricto orden no decreciente de profundidad (nivel 0, luego nivel 1, luego nivel 2, etc.), el primer nodo que coincida con el criterio de búsqueda tiene la garantía matemática de ser aquel situado a la menor distancia de la raíz en número de aristas. Por el contrario, DFS podría internarse prematuramente por una rama muy profunda y encontrar una solución tardía e ineficiente.

---

## Punto 5. Aplicación al análisis sintáctico

Se considera la siguiente gramática libre de contexto simplificada:

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

En el análisis sintáctico descendente, los nodos son instanciados conforme se invocan y expanden las subrutinas de parsing. El orden cronológico de creación de los 19 nodos del árbol es:

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

### 4. Información proporcionada por cada recorrido

- **Recorrido en Preorden:** Refleja la secuencia temporal y lógica en la que el analizador descendente toma decisiones gramaticales. Indica qué regla de producción se selecciona y cuándo se anticipa la coincidencia de cada componente léxico entrante.
- **Recorrido en Postorden:** Refleja el orden de síntesis y reducción semántica. Dado que visita a los hijos antes que al padre, es el recorrido idóneo para computar atributos sintetizados, realizar verificación de tipos en el análisis semántico y generar código intermedio.
- **Recorrido en BFS:** Descompone el árbol en niveles horizontales de abstracción sintáctica, permitiendo examinar cómo se expanden simultáneamente las construcciones del lenguaje en función de su profundidad en la gramática.

### 5. Comparación entre el orden de creación de nodos y el recorrido en preorden

Al comparar los identificadores secuenciales de creación con el recorrido DFS en preorden, se evidencia una **coincidencia matemática perfecta**: la secuencia de visita en preorden es exactamente `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19`. Esto demuestra que el algoritmo de análisis sintáctico descendente construye el árbol mediante una estrategia de exploración en profundidad guiada por la derivación por la izquierda.

### 6. Representación de la precedencia de operadores en el árbol

La precedencia de la multiplicación sobre la suma se encuentra codificada directamente en la topología estratificada de la gramática. En la estructura del árbol:
- La suma se introduce en el nodo E' (a profundidad menor, nivel 2).
- La multiplicación se introduce en el nodo T' descendiente del segundo T (a profundidad mayor, niveles 3 y 4).
Debido a esta disposición, la operación de producto queda encapsulada en un subárbol más interno. Durante cualquier procesamiento ascendente o de reducción semántica, el producto `id * id` debe calcularse en su totalidad antes de que su resultado pueda sumarse con el primer `id`, garantizando así que la multiplicación posea mayor jerarquía que la suma sin necesidad de paréntesis adicionales.

### 7. Algoritmo para métricas del árbol sintáctico

Se programó una función en `arbol_sintactico.py` que recorre el árbol y computa las siguientes propiedades estructurales:
- **Nodos totales:** 19
- **Nodos terminales (tokens reales de entrada):** 5 (`id`, `+`, `id`, `*`, `id`)
- **Nodos no terminales (estructuras sintácticas intermedias):** 11 (`E`, `T`, `F`, `T'`, `E'`, etc.)
- **Producciones vacías ($\epsilon$):** 3 (derivaciones vacías para culminar las listas $T'$ y $E'$)
- **Altura del árbol (medida por aristas):** 5 aristas (6 niveles de nodos)

---

## Comparación final

A continuación se consolida la tabla comparativa entre las dos estrategias de recorrido fundamentales:

| Criterio | DFS | BFS |
| :--- | :--- | :--- |
| Estructura auxiliar | Pila (pila de llamadas del sistema o estructura explícita LIFO) | Cola (estructura FIFO) |
| Orden de exploración | Profundidad vertical (avanza hasta la hoja antes de retroceder) | Anchura horizontal (recorre nivel por nivel) |
| Complejidad temporal | O(n) | O(n) |
| Complejidad espacial | O(h), donde h es la altura del árbol | O(w), donde w es el ancho máximo de un nivel |
| Conveniente para evaluar expresiones | Sí (a través del recorrido postorden) | No (no respeta la precedencia entre subárboles) |
| Conveniente para recorrer por niveles | No | Sí (es su comportamiento inherente) |
| Comportamiento en árboles profundos | Puede requerir memoria O(n) o provocar desbordamiento de pila | Eficiente en memoria si el ancho de cada nivel es reducido |
| Comportamiento en árboles anchos | Muy eficiente en memoria, pues la altura h se mantiene reducida | Muy ineficiente en memoria, pues la cola almacena todo el nivel ancho |

---

## Conclusión final

Los árboles y sus recorridos constituyen la columna vertebral del análisis sintáctico descendente porque proporcionan la estructura formal indispensable para verificar, organizar y evaluar el código fuente. En este paradigma, el proceso de derivación por la izquierda modela directamente la construcción del árbol desde el símbolo inicial en la raíz hacia las hojas, que corresponden a los componentes léxicos leídos. El recorrido en profundidad (DFS) en preorden no es simplemente una técnica de exploración, sino el mecanismo operativo exacto mediante el cual el analizador descubre producciones, expande los símbolos no terminales y anticipa los terminales esperados. A su vez, el recorrido en postorden resulta crucial durante la fase de síntesis semántica, pues asegura que todos los subárboles de una expresión estén previamente validados y computados antes de aplicar los operadores principales. Por su parte, la comprensión del recorrido en anchura (BFS) permite inspeccionar la jerarquía por capas y optimizar la recuperación ante errores. Sin la abstracción jerárquica de los árboles y la disciplina algorítmica de sus recorridos, resultaría inviable transformar flujos lineales de texto en representaciones lógicas analizables, estructuradas y eficientes dentro de un compilador.

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
