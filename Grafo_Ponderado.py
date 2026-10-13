import os
import tkinter as tk


mapa = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras": {"Sibiu": 99, "Bucarest": 211},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucarest": 101},
    "Bucarest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucarest": 90},
    "Urziceni": {"Bucarest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

heuristica = {
    "Arad": 366, "Bucarest": 0, "Craiova": 160, "Drobeta": 242,
    "Eforie": 161, "Fagaras": 178, "Giurgiu": 77, "Hirsova": 151,
    "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
    "Oradea": 380, "Pitesti": 98, "Rimnicu Vilcea": 193, "Sibiu": 253,
    "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374
}

posiciones = {
    "Arad": (95, 239),
    "Sibiu": (273, 291),
    "Rimnicu Vilcea": (314, 365),
    "Pitesti": (449, 431),
    "Bucarest": (572, 493)
}


def buscar_ruta():
    frontera = [(heuristica["Arad"], 0, "Arad", ["Arad"])]
    mejor_distancia = {"Arad": 0}

    while frontera:
        frontera.sort()
        estimado, distancia, ciudad, ruta = frontera.pop(0)

        if distancia > mejor_distancia[ciudad]:
            continue

        if ciudad == "Bucarest":
            return ruta, distancia

        for vecino, costo in mapa[ciudad].items():
            nueva_distancia = distancia + costo
            if nueva_distancia < mejor_distancia.get(vecino, float("inf")):
                mejor_distancia[vecino] = nueva_distancia
                prioridad = nueva_distancia + heuristica[vecino]
                frontera.append((prioridad, nueva_distancia, vecino, ruta + [vecino]))

    return [], 0


def mostrar_ruta(ruta, distancia):
    ventana = tk.Tk()
    ventana.title("Ruta más corta a Bucarest")

    imagen = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "mapa_rumania.png"))

    controles = tk.Frame(ventana, padx=10, pady=8)
    controles.pack()
    estado = tk.Label(controles, text="Pulsa «Siguiente» para recorrer la ruta.")
    estado.pack(side="left", padx=10)

    mapa_visual = tk.Canvas(ventana, width=imagen.width(), height=imagen.height())
    mapa_visual.pack()
    mapa_visual.create_image(0, 0, anchor="nw", image=imagen)

    paso = [0]
    acumulado = [0]

    def marcar(ciudad, color):
        x, y = posiciones[ciudad]
        mapa_visual.create_oval(
            x - 9, y - 9, x + 9, y + 9,
            fill=color, outline="white", width=2, tags="ruta"
        )

    def siguiente():
        origen = ruta[paso[0]]
        destino = ruta[paso[0] + 1]
        x1, y1 = posiciones[origen]
        x2, y2 = posiciones[destino]
        costo = mapa[origen][destino]

        mapa_visual.create_line(x1, y1, x2, y2, fill="white", width=9, tags="ruta")
        mapa_visual.create_line(x1, y1, x2, y2, fill="#e53935", width=5, tags="ruta")
        marcar(destino, "#e53935")

        acumulado[0] += costo
        paso[0] += 1
        estado.config(
            text=f"{origen} a {destino}: {costo} km   "
                 f"Acumulado: {acumulado[0]} km   "
        )

        if paso[0] == len(ruta) - 1:
            estado.config(text=f"Llegaste a Bucarest. Distancia total: {distancia} km.")
            boton.config(state="disabled")

    def reiniciar():
        paso[0] = 0
        acumulado[0] = 0
        mapa_visual.delete("ruta")
        estado.config(text="Pulsa «Siguiente» para recorrer la ruta.")
        marcar("Arad", "#2e7d32")
        boton.config(state="normal")

    marcar("Arad", "#2e7d32")

    boton = tk.Button(controles, text="Siguiente", command=siguiente)
    boton.pack(side="left", padx=5)

    boton_reiniciar = tk.Button(controles, text="Reiniciar", command=reiniciar)
    boton_reiniciar.pack(side="left", padx=5)

    ventana.mainloop()

if __name__ == "__main__":
    ruta, distancia = buscar_ruta()
    if ruta:
        mostrar_ruta(ruta, distancia)
    else:
        print("No se encontro una ruta.")
