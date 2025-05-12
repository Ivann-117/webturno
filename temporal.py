# Clase que representa un nodo del árbol
class Nodo:
    def __init__(self, valor):
        self.valor = valor  # Valor del nodo
        self.izquierda = None  # Subárbol izquierdo
        self.derecha = None    # Subárbol derecho

# Clase que representa el árbol binario de búsqueda
class ArbolBinario:
    def __init__(self):
        self.raiz = None  # Inicialmente el árbol está vacío

    # Inserta un nuevo valor en el árbol
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)  # Si el árbol está vacío, el nuevo valor es la raíz
        else:
            self._insertar_recursivo(self.raiz, valor)  # Llama a función recursiva auxiliar

    # Función auxiliar recursiva para insertar
    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, valor)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecha, valor)

    # Recorre el árbol en inorden (izquierda, raíz, derecha)
    def recorrido_inorden(self):
        return self.inorden_recursivo(self.raiz)

    def inorden_recursivo(self, nodo):
        resultado = []
        if nodo:
            resultado += self.inorden_recursivo(nodo.izquierda)
            resultado.append(nodo.valor)
            resultado += self.inorden_recursivo(nodo.derecha)
        return resultado

    # Recorre el árbol en preorden (raíz, izquierda, derecha)
    def recorrido_preorden(self):
        return self._preorden_recursivo(self.raiz)

    def _preorden_recursivo(self, nodo):
        resultado = []
        if nodo:
            resultado.append(nodo.valor)
            resultado += self._preorden_recursivo(nodo.izquierda)
            resultado += self._preorden_recursivo(nodo.derecha)
        return resultado

        # Recorre el árbol en postorden (izquierda, derecha, raíz)
    def recorrido_postorden(self):
            return self._postorden_recursivo(self.raiz)

    def _postorden_recursivo(self, nodo):
            resultado = []
            if nodo:
                resultado += self._postorden_recursivo(nodo.izquierda)
                resultado += self._postorden_recursivo(nodo.derecha)
                resultado.append(nodo.valor)
            return resultado

    # Busca un valor en el árbol
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False  # Valor no encontrado
        if valor == nodo.valor:
            return True   # Valor encontrado
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        else:
            return self._buscar_recursivo(nodo.derecha, valor)

    # Encuentra el valor mínimo del árbol (extremo izquierdo)
    def encontrar_minimo(self):
        actual = self.raiz
        if actual is None:
            return None
        while actual.izquierda:
            actual = actual.izquierda
        return actual.valor

    # Encuentra el valor máximo del árbol (extremo derecho)
    def encontrar_maximo(self):
        actual = self.raiz
        if actual is None:
            return None
        while actual.derecha:
            actual = actual.derecha
        return actual.valor

    # Elimina un nodo del árbol
    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            # Nodo con un solo hijo o sin hijos
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            # Nodo con dos hijos: buscar sucesor inorden
            sucesor = self._minimo_nodo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.valor)
        return nodo

    # Encuentra el nodo con el valor mínimo (usado al eliminar nodo con dos hijos)
    def _minimo_nodo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual

# --- Menú interactivo directamente ejecutado ---
arbol = ArbolBinario()

while True:
    print("\n======= MENÚ ÁRBOL BINARIO ========")
    print("1. Insertar valor")
    print("2. Recorrido inorden")
    print("3. Recorrido preorden")
    print("4. Recorrido postorden")
    print("5. Buscar valor")
    print("6. Valor mínimo")
    print("7. Valor máximo")
    print("8. Eliminar valor")
    print("9. Salir")

    opcion = input("Seleccione una opción: ")

    match opcion:
        case "1":
            entrada = input("Ingrese uno o varios valores a insertar (separados por espacio): ")
            valores = entrada.split()
            for val in valores:
                arbol.insertar(int(val))
            print("Valores insertados.")
            print("Árbol actual (inorden):", arbol.recorrido_inorden())
        case "2":
            print("Inorden:", arbol.recorrido_inorden())
        case "3":
            print("Preorden:", arbol.recorrido_preorden())
        case "4":
            print("Postorden:", arbol.recorrido_postorden())
        case "5":
            entrada = input("Ingrese uno o varios valores a buscar (separados por espacio): ")
            valores = entrada.split()
            for val in valores:
                encontrado = arbol.buscar(int(val))
                print(f"Valor {val}: {'encontrado' if encontrado else 'no encontrado'}.")
        case "6":
            minimo = arbol.encontrar_minimo()
            if minimo is not None:
                print("Valor mínimo:", minimo)
            else:
                print("Árbol vacío.")
        case "7":
            maximo = arbol.encontrar_maximo()
            if maximo is not None:
                print("Valor máximo:", maximo)
            else:
                print("Árbol vacío.")
        case "8":
            entrada = input("Ingrese uno o varios valores a eliminar (separados por espacio): ")
            valores = entrada.split()
            for val in valores:
                arbol.eliminar(int(val))
                print(f"Valor {val} eliminado si existía.")
            print("Árbol actual (inorden):", arbol.recorrido_inorden())
        case "9":
            print("Saliendo del programa...")
            break
        case _:
            print("Opción no válida. Intente de nuevo.")