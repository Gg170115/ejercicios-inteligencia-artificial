import random
import time
import tkinter as tk


def jugar():
    secreto = random.randint(1, 100)
    minimo, maximo = 1, 100
    intento = (minimo + maximo) // 2
    veces = 0

    numero.config(text=f"Número: {secreto}")
    historial.delete(0, tk.END)

    while intento != secreto:
        veces += 1
        if intento < secreto:
            minimo = intento + 1
            pista = "el secreto es mayor"
        else:
            maximo = intento - 1
            pista = "el secreto es menor"

        historial.insert(tk.END, f"{veces}. {intento}: {pista}")
        ventana.update()
        time.sleep(0.4)
        intento = (minimo + maximo) // 2
    veces += 1
    historial.insert(tk.END, f"{veces}. {intento}: Encontrado")


ventana = tk.Tk()
numero = tk.Label(ventana, text="Número: -")
numero.pack(padx=20, pady=10)
historial = tk.Listbox(ventana, width=35, height=8)
historial.pack(padx=20, pady=5)
boton = tk.Button(ventana, text="Empezar", command=jugar)
boton.pack(pady=10)
ventana.mainloop()
