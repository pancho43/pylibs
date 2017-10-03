# -*- coding: latin-1 -*-
import sys
# import os

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd

import soporte as Sp


class ShowPair(ttk.Frame):
    """ Clase que despliega dos etiquetas alineadas.

    Las etiquetas se formatean diferente, una tiene función de etiqueta,
    la otra de dato.
    Se tiene acceso de escritura al dato con el método set.
    No hay acceso a la etiqueta. Está implanada como Label anónima.
    Se puede tener acceso de lectura y escritura al dato vía el miembro
    var que es una StringVar ligada a la Label correspondiente.
    :param master: ventana a la que pertenece.
    :param etiqueta: texto para acompañar la entrada.
    :param dato: valor inicial para la segunda etiqueta.
    :param ancho1: ancho de la etiqueta.
    :param ancho2: ancho del dato. Se ajusta si es necesario.
    :param orient: Indica la posición relativa si "h" etiqueta a la izquierda.
    :param color: Color para el dato.
    :param **args: Parámetros adicionales para conducta tipo Frame.
    """
    def __init__(self, master, etiqueta, dato, ancho1=10, ancho2=15,
                 orient="h", color="linen", **args):
        ttk.Frame.__init__(self, master, **args)
        self.var = tk.StringVar()
        self.var.set(dato)
        self.wid = ancho2
        if ancho1 == 0:
            ancho1 = len(etiqueta) + 2
        if orient == "v":
            tk.Label(self, text=etiqueta, width=ancho1,
                     anchor=tk.W).pack(side=tk.TOP)
        else:
            tk.Label(self, text=etiqueta, width=ancho1,
                     anchor=tk.W).pack(side=tk.LEFT)
        self.etiqueta = tk.Label(self, textvariable=self.var, anchor=tk.W,
                                 relief=tk.SUNKEN, width=ancho2,
                                 background=color)
        self.etiqueta.pack()

    def set(self, dato):
        """ Asigna valor a la segunda etiqueta.

        :param dato: Valor a desplegar.
        """
        self.var.set(dato)
        self.etiqueta.configure(width=max(len(dato) + 2, self.wid))


class EntradaTxt(ttk.Frame):
    """ Clase que despliega una etiqueta y un campo de entrada.

    :param master: ventana a la que pertenece.
    :param texto: texto para la etiqueta.
    :param dato: valor inicial para la entrada. Default es vacía.
    :param ancho1: anchura de la etiqueta.
    :param ancho2: anchura de la entrada.
    :param orient: controla la posición relativa y la alineación de la
     etiqueta.  "h" indica a la izquierda, "v" encima. "l" indica que la
     etiqueta se alínea a la izquierda, "c" centrada y "r" a la derecha.
    :param \**args: argumentos adicionales para conducta tipo Frame.

    El acceso de lectura y escritura a la entrada es con los métodos
    get y set. La etiqueta es una Label anónima, no puede cambiarse.
    Se puede acceder al campo de entrada con el miembro var de la clase.

    """
    def __init__(self, master, texto, dato="", ancho1=15, ancho2=15,
                 orient="hl", **args):
        ttk.Frame.__init__(self, master, **args)
        self.var = tk.StringVar()
        self.var.set(dato)

        if "h" in orient:
            cords = ((0, 0), (0, 1))
        elif "v" in orient:
            cords = ((0, 0), (1, 0))

        if "l" in orient:
            st = tk.W
        elif "r" in orient:
            st = tk.E
        elif "c" in orient:
            st = tk.EW
        else:
            st = tk.W

        self.etiqueta = tk.Label(self, text=texto, width=ancho1, anchor=st)
        self.etiqueta.grid(row=cords[0][0], column=cords[0][1],
                           sticky=st)
        self.ent = tk.Entry(self, textvariable=self.var, width=ancho2)
        self.ent.grid(row=cords[1][0], column=cords[1][1], sticky=tk.W)

    def get(self):
        return self.var.get()

    def set(self, valor):
        self.var.set(valor)


class EntradaStripedTxt(EntradaTxt):
    """ Entrada de texto que elimina blancos al principio y al final.

    Acepta únicamente texto como argumento posicional. Los demás
    argumentos de EntradaTxt pueden usarse con nombre.
    """

    def __init__(self, master, texto, **args):
        EntradaTxt.__init__(self, master, texto, **args)
        self.ent.bind("<FocusOut>", self.limpia)

    def limpia(self, event=None):
        texto = self.get().strip()
        self.set(texto)


class EntradaFecha(EntradaTxt):
    """ Acepta una fecha como entrada.

    Valida que los datos de entrada formen una fecha válida. Si es así
    la convierte a formato "aaaammdd". Si no, borra los datos y reinicia.
    """
    def __init__(self, master, texto, **args):
        EntradaTxt.__init__(self, master, texto, **args)

        self.ent.bind("<FocusOut>", self.valFecha)

    def valFecha(self, event=None):
        texto = self.var.get()
        v = Sp.valFecha(texto)
        print("V:", v)
        self.var.set(v)
        if not v:
            self.ent.focus_set()

    def set(self, valor):
        self.var.set(valor)


class Seleccion(ttk.Frame):
    """ Implanta un OptionMenu en un Frame.

    Recibe una etiqueta, un valor inicial y una lista de opciones. Puede
    colocarse la etiqueta a la izquierda o arriba del menú.
    """
    def __init__(self, master, texto, valor, opciones, orient="h", **args):
        ttk.Frame.__init__(self, master, **args)
        self.var = tk.StringVar(self)
        self.var.set(valor)
        self._opciones = opciones
        if orient == "h":
            ttk.Label(self, text=texto).pack(side=tk.LEFT)
        else:
            ttk.Label(self, text=texto).pack(side=tk.TOP)

        self.opc = tk.OptionMenu(self, self.var, self.var.get(),
                                 *self._opciones)
        self.opc.pack()

    def get(self):
        """ Regresa el valor actual del menú."""
        return self.var.get()

    def reset(self, opciones, indice=None):
        """ Reinicializa los valores en el menú.

        Si se da un indice, se asigna el valor del menú a la opción
        que corresponde a ese indice.
        """
        self._opciones = opciones
        menu = self.opc["menu"]
        menu.delete(0, "end")
        for texto in self._opciones:
            menu.add_command(label=texto,
                             command=lambda value=texto: self.var.set(value))
        if indice is not None:
            self.var.set(self._opciones[indice])
        else:
            self.var.set(self._opciones[0])

    def set(self, index):
        self.var.set(self._opciones[index])


class OptionWithKeyb(Seleccion):
    def __init__(self, master, texto, valor, opciones, orient="h", **args):
        Seleccion.__init__(self, master, texto, valor, opciones, orient,
                           **args)

        self.opc.configure(takefocus=1)
        self.opc.bind('<Key>', self.navigate)
        print(dir(self.opc))
        print(self.opc.tkraise.__doc__)

    def navigate(self, event=None):
        c = event.char.upper()
        C = event.char.upper()
        s = event.keysym
        pos = self._opciones.index(self.get())
        print((c, C, s, self.get(), pos))
        if s == 'Down':
            if pos + 1 < len(self._opciones):
                self.set(pos+1)
            print(self.get())
        if s == "Up":
            if pos > 0:
                self.set(pos-1)
            print(self.get())


class SeleccionTeclado(Seleccion):
    """ Implantar un option Menu controlado con el teclado."""
    def __init__(self, master, texto, valor, opciones, orient="h", **args):
        Seleccion.__init__(self, master, texto, valor, opciones,
                           orient="h", **args)

        self.opc.configure(takefocus=1)

        self.opc.bind('<Key>', self.navigate)

    def navigate(self, event=None):
        c = event.char.upper()
        choices = self.opciones
        actual = self.get()
        print("Navegando:", event.char, c, actual, choices)
        if c.isalpha():
            print("is alfa")
            if actual[0] == c:
                print("actual coincide")
                pos = choices.index(actual)
                while pos+1 < len(choices):
                    pos += 1
                    if choices[pos][0] == c:
                        self.set(pos)
                        break

            else:
                for i in range(len(choices)):
                    if choices[i][0] == c:
                        self.set(i)
        print("---------------")


class SelectKey(ttk.Frame):
    def __init__(self, master, texto, opciones, direccion="h", **args):
        ttk.Frame.__init__(self, master, **args)
        self.datos = {x[1]: x[0] for x in opciones}
        self.kis = [x[1] for x in opciones]

        self.opc = Seleccion(self, texto, self.kis[0], self.kis,
                             orient=direccion)
        self.opc.pack()

    def get(self):
        return self.datos[self.opc.get()]

    def set(self, valor):
        self.opc.set(self.kis.index(valor))  # ?????


class TestSelectKey(ttk.Frame):
    def __init__(self, master, **args):
        ttk.Frame.__init__(self, master, **args)
        self.opciones = SelectKey(self, "Opciones",
                                  [["1", "uno"], ["2", "dos"],
                                   ["3", "tres"], ["4", "cuatro"]])
        self.opciones.pack()
        self.disp = ShowPair(self, "Seleccionada:", self.opciones.get())
        self.sel()
        self.disp.pack()
        self.b = tk.Button(self, text="Select", command=self.sel)
        self.b.pack()

    def sel(self):
        self.disp.set(self.opciones.get())


class SelectPair(ttk.Frame):
    """Dos menús relacionados.

    Maneja un diccionario donde las llaves son las opcione del primer
    menú y los valores correspondientes son las opciones del segundo
    menú.
    """
    def __init__(self, master, nombre1, nombre2, datos, valor1, valor2,
                 direccion="v", **args):
        """ Inicia una instancia de SelectPair.

        :param nombre1: Etiqueta para el primer menú.
        :param nombre2: Etiqueta para el segundo menú.
        :param datos: Diccionario con las opciones para ambos menús.
        :param valor1: Valor inicial del primer menú.
        :param valor2: Valor inicial del segundo menú.
        :param direccion: Si "v" un menú se coloca sobre el otro. En
                          cualquier otro caso uno al lado del otro.
        """
        ttk.Frame.__init__(self, master, **args)
        self.datos = datos
        self.kis = list(datos.keys())
        self.kis.sort()
        if valor1 not in self.kis:
            valor1 = self.kis[0]
        if valor2 not in self.datos[valor1]:
            valor2 = self.datos[valor1][0]
        self.vals = self.datos[valor1]

        self.s1 = SeleccionTeclado(self, nombre1, valor1, self.kis)
        if direccion == "v":
            self.s1.pack(side=tk.TOP)
        else:
            self.s1.pack(side=tk.LEFT)

        self.s2 = SeleccionTeclado(self, nombre2, valor2, self.vals)
        self.s2.pack()
        self.s1.var.trace("w", self.actualiza)

        # self.s1.opc.configure()

    def actualiza(self, *args):
        """ Actualiza el segundo menú según la selección del primero."""
        self.vals = self.datos[self.s1.get()]
        self.s2.reset(self.vals)
        print("actualiza", self.s1.get, self.vals)

    def getFirst(self):
        """ Regresa la selección del primer menú."""
        return self.s1.get()

    def getSecond(self):
        """ Regesa la selección del segundo menú."""
        return self.s2.get()


class RadioPanel(ttk.LabelFrame):
    def __init__(self, master, titulo, etiquetas, lado=tk.TOP, **args):
        ttk.LabelFrame.__init__(self, master, text=titulo, **args)
        self.var = tk.StringVar()
        self.var.set(etiquetas[0][0])
        self.posibles = [x[0] for x in etiquetas]

        # if titulo:
        #   ttk.Label(self,text=titulo,).pack(anchor=tk.W)
        # self.inner = ttk.Frame(self)

        # self.inner.pack(padx=3,pady=3,ipadx=1)
        self.botones = []
        for x in etiquetas:
            b = ttk.Radiobutton(self, text=x, variable=self.var, value=x[0])
            b.pack(side=lado, anchor=tk.W)
            self.botones.append(b)

    def get(self):
        return self.var.get()

    def set(self, valor):
        if valor in self.posibles:
            self.var.set(valor)


class RadioPanelSinFoco(ttk.LabelFrame):
    """Todo: herencia?"""
    def __init__(self, master, titulo, etiquetas, lado=tk.TOP, **args):
        ttk.LabelFrame.__init__(self, master, text=titulo, **args)
        self.var = tk.StringVar()
        self.var.set(etiquetas[0][0])
        self.posibles = [x[0] for x in etiquetas]

        self.botones = []
        for x in etiquetas:
            b = ttk.Radiobutton(self, text=x, variable=self.var, value=x[0])
            b.pack(side=lado, anchor=tk.W)
            b.configure(takefocus=0)
            self.botones.append(b)

    def get(self):
        return self.var.get()

    def set(self, valor):
        if valor in self.posibles:
            self.var.set(valor)


class Lista(ttk.Frame):
    """ Despliega una lista desplazable.

    Lista simple.
    """
    def __init__(self, master=None, ancho=40, alto=20, datos=[], **args):
        ttk.Frame.__init__(self, master, **args)
        self.datos = datos
        self.vbar = tk.Scrollbar(self)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.lista = tk.Listbox(self, height=alto, width=ancho,
                                selectmode=tk.SINGLE)
        self.lista.pack(expand=1, fill=tk.BOTH, ipadx=3)
        self.lista.config(yscrollcommand=self.vbar.set)
        self.lista.config(xscrollcommand=self.hbar.set)
        self.vbar.config(command=self.lista.yview)
        self.hbar.config(command=self.lista.xview)
        for x in datos:
            self.lista.insert(tk.END, x)
        self.lista.activate(0)

    def reInit(self, dat):
        self.lista.delete(0, tk.END)
        self.datos = dat
        for x in self.datos:
            self.lista.insert(tk.END, x)
        self.lista.activate(0)

    def get(self):
        return self.lista.get(int(self.lista.curselection()[0]))


class Info(ttk.Frame):
    def __init__(self, master, fijo="", inicial=" "*20, **args):
        ttk.Frame.__init__(self, master, **args)
        if not fijo:
            fijo = "Python " + sys.version.split()[0]
        self.vl = tk.Label(self, text=fijo, background="linen",
                           font=("Helvetica", 10, "italic"))
        # self.vl.pack(side=RIGHT,expand=1,fill=BOTH)
        self.vl.pack(side=tk.RIGHT)
        self.dato = tk.StringVar()
        self.dato.set(inicial)
        tk.Label(self, textvariable=self.dato, background="bisque",
                 font=("Helvetica", 10, "normal")).pack(side=tk.LEFT,
                                                        expand=1, fill=tk.X)

    def set(self, dato):
        self.dato.set(dato)


class Quitter(ttk.Frame):
    def __init__(self, master=None, **args):
        ttk.Frame.__init__(self, master, **args)
        self.q = ttk.Button(self, text='Salir', command=self.quit)
        self.q.pack()

    def quit(self):
        ans = mb.askokcancel('Confirmar Salida', "Está seguro?")
        if ans:
            ttk.Frame.quit(self)


class FindFiles(ttk.Frame):
    def __init__(self, master, ruta=".", **args):
        ttk.Frame.__init__(self, master, **args)
        ars = Sp.listFiles(ruta)
        archivos = [x[1] for x in ars]
        self.ruta = tk.StringVar()
        self.ruta.set(ruta)
        self.f = ttk.Frame(self, borderwidth=2, relief=tk.RIDGE)
        self.f.pack(side=tk.TOP, padx=3, pady=3, anchor=tk.W, expand=1,
                    fill=tk.X)
        self.lbl = ShowPair(self.f, etiqueta="Ruta:", dato=ruta, ancho1=4,
                            ancho2=15)
        self.lbl.pack(side=tk.LEFT, anchor=tk.NW)
        self.buscar = tk.Button(self.f, text="Examinar", width=10,
                                command=self.buscar)
        self.buscar.pack(side=tk.LEFT)
        self.lf = Lista(self, datos=archivos, ancho=30, alto=15)
        self.lf.pack(side=tk.TOP, anchor=tk.NW, padx=3, expand=1, fill=tk.BOTH)

    def buscar(self):
        r = fd.askdirectory(initialdir=self.ruta.get())
        self.ruta.set(r)
        lf = Sp.listFiles(r)
        archivos = [x[1] for x in lf]
        self.lf.reInit(archivos)
        self.lbl.set(r)

if __name__ == '__main__':
    pass
