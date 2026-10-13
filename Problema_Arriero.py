from collections import deque

IZQUIERDA = "i"
DERECHA = "d"

ESTADO_INICIAL = (IZQUIERDA, IZQUIERDA, IZQUIERDA, IZQUIERDA)
ESTADO_META = (DERECHA, DERECHA, DERECHA, DERECHA)

ACCIONES = (
    ("solo", None),
    ("puma", 1),
    ("lechuga", 2),
    ("cabra", 3),
)

NOMBRES = ("arriero", "puma", "lechuga", "cabra")
DESCRIPCION_ACCION = {
    "solo": "cruza solo",
    "puma": "cruza con el puma",
    "lechuga": "cruza con la lechuga",
    "cabra": "cruza con la cabra",
}


def aplicar_accion(estado, indice_objeto):
    """Devuelve el nuevo estado y, si el cruce no es válido, el motivo."""
    arriero = estado[0]
    destino = DERECHA if arriero == IZQUIERDA else IZQUIERDA
    nuevo = list(estado)

    # El arriero no puede llevar un objeto que esté en la otra orilla.
    if indice_objeto is not None:
        if estado[indice_objeto] != arriero:
            return None, f"{NOMBRES[indice_objeto]} no está con el arriero"
        nuevo[indice_objeto] = destino

    nuevo[0] = destino
    nuevo = tuple(nuevo)

    nuevo_arriero, puma, lechuga, cabra = nuevo

    # El puma se come a la cabra si quedan solos.
    if puma == cabra and nuevo_arriero != puma:
        return None, "puma y cabra quedan solos"

    # La cabra se come la lechuga si quedan solas.
    if lechuga == cabra and nuevo_arriero != lechuga:
        return None, "cabra y lechuga quedan solas"

    return nuevo, None


def buscar_en_anchura():
    """Busca la solución con BFS: siempre explora primero el camino más corto."""
    # FIFO 
    cola = deque([(ESTADO_INICIAL, [])])
    visitados = {ESTADO_INICIAL}
    intentos_fallidos = []

    while cola:
        estado, camino = cola.popleft()

        if estado == ESTADO_META:
            return camino, intentos_fallidos

        for accion, indice_objeto in ACCIONES:
            nuevo_estado, motivo = aplicar_accion(estado, indice_objeto)

            if motivo:
                intentos_fallidos.append((estado, accion, motivo))
                continue

            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                nuevo_camino = camino + [(accion, nuevo_estado)]
                cola.append((nuevo_estado, nuevo_camino))

    return None, intentos_fallidos


def lado(nombre_lado):
    return "izquierda" if nombre_lado == IZQUIERDA else "derecha"


def mostrar_estado(estado):
    return ", ".join(
        f"{nombre}: {lado(posicion)}"
        for nombre, posicion in zip(NOMBRES, estado)
    )


def mostrar_intentos_fallidos(intentos_fallidos):
    print("\nCruces descartados (estado | acción | motivo):")
    for estado, accion, motivo in intentos_fallidos:
        print(f"{mostrar_estado(estado)} | {accion} | {motivo}")


if __name__ == "__main__":
    solucion, intentos_fallidos = buscar_en_anchura()

    if solucion is None:
        print("No se encontró una solución.")
    else:
        print(f"Solución encontrada con {len(solucion)} cruces:")
        print(f"Inicio: {mostrar_estado(ESTADO_INICIAL)}")

        for numero, (accion, estado) in enumerate(solucion, start=1):
            print(f"{numero}. El arriero {DESCRIPCION_ACCION[accion]}.")
            print(f"   {mostrar_estado(estado)}")

    mostrar_intentos_fallidos(intentos_fallidos)
