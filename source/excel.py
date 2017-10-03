# -*- coding: latin-1 -*-

# import os
from xlrd import open_workbook as ow
import xlsxwriter as xlw


""" Funciones para lectura y escritura simple de archivos de excel."""


# -----------------------------------------------------------------------------
# Lectura
# -----------------------------------------------------------------------------


def archivoXl(archivo):
    """ Abre un archivo de excel por nombre."""
    return ow(archivo)


def archivoXlFormateado(archivo):
    """ Abre un archivo de excel por nombre."""
    return ow(archivo, formatting_info=True)


def nombresHojas(libro):
    """ Regresa la lista de nombres de las hojas del libro."""
    return [sh.name for sh in libro.sheets()]


def obtenerHoja(libro, nombre):
    """ Regresa un objeto hoja. """
    return libro.sheet_by_name(nombre)


def obtenerHojaNum(libro, num):
    """ Regresa un objeto hoja. """
    return libro.sheet_by_index(num)


def leeHoja(hoja):
    """ Regresa el contenido de la hoja en una matriz."""
    return [renglon(hoja, r) for r in range(hoja.nrows)]


def renglon(hoja, r):
    """ Regresa el contenido del renglón dado del objeto hoja"""
    return [hoja.cell(r, i).value for i in range(hoja.ncols)]


def anchuras(hoja):
    """ Regresa las anchuras de cada columna usada en la hoja"""
    return [hoja.computed_column_width(i) for i in range(hoja.ncols)]


def xlDatos(archivo, hoja):
    """ Obtiene el contenido de una hoja de un archivo excel.

    Los parámetros son los nombres del archivo y de la hoja.
    La diferencia es que los objetos libro y hoja usados son
    temporales.
    """
    bk = ow(archivo)
    return leeHoja(obtenerHoja(bk, hoja))


# -----------------------------------------------------------------------------
# Escritura
# -----------------------------------------------------------------------------


def creaXl(nombre):
    """ Crea un objeto libro con el nombre de archivo dado."""
    return xlw.Workbook(nombre)


def agregaHoja(libro, nombre):
    """ Crea un objeto hoja en el libro dado con el nombre dado."""
    return libro.add_worksheet(nombre)


def mkAnchos(hoja, anchos):
    """ Asigna los anchos dados a las primeras columnas de la hoja."""
    for i in range(len(anchos)):
        hoja.set_column(i, i, anchos[i])
    return hoja


def writeRenglon(hoja, renglon, datos):
    """ Escribe una lista de valores en una hoja.

    :param hoja: objeto hoja en el que se va a escribir.
    :param renglon: número del renglón en que se escribe. Empieza en cero.
    :param datos: lista de los valores a escribir.
    """
    hoja.write_row(renglon, 0, datos)


def writeRenglonFormat(hoja, renglon, datos, formatos):
    """ Escribe una lista de valores formateados en una hoja.

    :param hoja: objeto hoja en el que se va a escribir.
    :param renglon: múmero del renglón en que se va a escribir.
    :param datos: lista de valores a escribir.
    :param formatos: lista de formatos correspondientes a cada valor.

    La lista de parámetros debe tener la misma longitud o mayor que la
    de valores.
    """
    for i in range(len(datos)):
        # print(renglon, i, datos[i],formatos[i])
        writeCell(hoja, renglon, i, datos[i], formatos[i])


def writeCell(hoja, fila, columna, dato, formato=''):
    """ Escribe un dato en una hoja.

    :param hoja: objeto hoja en el que se va a escribir.
    :param fila: fila de la hoja para el dato.
    :param columna: columna de la hoja para el dato.
    :param dato: dato que va a escribirse.
    :param formato: formato a utilizarse.

    """
    if formato:
        hoja.write(fila, columna, dato, formato)
    else:
        hoja.write(fila, columna, dato)


def writeExcel(archivo, datos, hoja="Hoja1", titulo="", subtitulo="",
               encabezados=[], anchos=[], formatos=[]):
    """ Crea un archivo con una hoja y lo llena con los datos dados.

    Además usa los títulos, encabezados, anchos y formatos dados.
    El resultado es un reporte estándard con columnas y encabezados.
    Utiliza formatos estándard.

    :param archivo: nombre del archivo.
    :param datos: lista de registros con el contenido del archivo.
    :param hoja: nombre de la hoja a crearse.
    :param titulo: Texto a escribirse en el primer renglón.
    :param subtitulo: Texto para el segundo renglón.
    :param encabezados: Lista de encabezados para las columnas del reporte.
    :param anchos: Lista de anchos para las columnas.
    :param formatos: Lista de formatos. Codificada.

    TO DO: Adaptar a las funciones ya incluidas en este archivo.
    """

    bk = creaXl(archivo)
    sh = bk.add_worksheet(hoja)
    title = bk.add_format()
    title.set_font_size(14)
    title.set_bold()
    subtitle = bk.add_format()
    subtitle.set_font_size(12)
    subtitle.set_bold()
    numb = bk.add_format({'num_format': '#,##0.00'})
    bld = bk.add_format()
    bld.set_bold()

    fmts = {}
    fmts["n"] = numb
    fmts["b"] = bld

    for i in range(len(anchos)):
        sh.set_column(i, i, anchos[i])

    pos = 0
    if titulo:
        sh.write(pos, 0, titulo, title)
        pos += 1
    if subtitulo:
        if subtitle:
            sh.write("A2", subtitulo, subtitle)
            pos += 2
    if encabezados:
        writeRenglon(sh, pos, encabezados)
        pos += 2

    cols = max([len(x) for x in datos])
    while len(formatos) < cols:
        formatos.append("")
    for x in datos:
        # writeRenglonFormat(sh, pos, x, formatos, fmts)
        writeRenglonFormat(sh, pos, x, formatos)
        pos += 1

    bk.close()

# ----------------------------------------------------------------------------
# Interfaz de lectura.
# ----------------------------------------------------------------------------


def readSheet(archivo, nombre="", num=0):
    """ Lee una hoja de un archivo de excel.

    :param archivo: nombre del archivo.
    :param nombre: nombre de la hoja.
    :param num: número de la hoja.

    :returns: Lista de renglones de la hoja.

    Se usa el número de hoja solamente si el nombre es nulo.
    """
    if nombre:
        return leeHoja(archivoXl(archivo).sheet_by_name(nombre))
    else:
        return leeHoja(archivoXl(archivo).sheet_by_index(num))


def readXl(archivo):
    """ Regresa el contenido de un libro de excel, hoja por hoja.

    :param archivo: nombre del archivo.

    :returns: Diccionario con las hojas del libro.

    Los nombres de las hojas son las llaves del dicionario y el valor es
    la lista de renglones generada por readSheet.

    """
    bk = archivoXl(archivo)
    hjs = nombresHojas(bk)
    d = {}
    for h in hjs:
        sh = obtenerHoja(bk, h)
        li = leeHoja(sh)
        d[h] = li
    return d


def readXlNum(archivo):
    """ Regresa una lista del contenido de las hojas del archivo de excel.

    :param archivo: nombre del archivo.
    :returns: Lista de los contenidos de las hojas.

    Los índices de la lista corresponde a los índices de las hojas.
    """
    return [leeHoja(sh) for sh in archivoXl(archivo).sheets()]


def readXlDet(archivo):
    """ Regresa el contenido del archivo excel, en forma detallada.

    :param archivo: nombre del archivo a leer.

    Por el momento, "detallada" significa tres listas de hojas:
    nombre, anchuras y contenido. Tal vez se agreguen cosas después.
    """
    bk = archivoXlFormateado(archivo)
    datos, anchos, nombres = [], [], []
    for sh in bk.sheets():
        datos.append(leeHoja(sh))
        nombres.append(sh.name)
        anchos.append(anchuras(sh))
    return (nombres, anchos, datos)

# ----------------------------------------------------------------------------
# Interfaz de escritura.
# ----------------------------------------------------------------------------


def writeBook(hojas, formatos, nombre):
    """ Crea un archivo de excel con el nombre y hojas dados.

    :param hojas: lista de diccionarios con la descripción de las hojas.
    :param formatos: diccionario donde los valores especifican un formato.
    :param nombre: ruta y nombre del archivo a crear.


    """
    if nombre.upper().endswith(".XLS"):
        nombre += "x"
    bk = creaXl(nombre)
    # Formatos
    dFmts = {}
    if "default" not in formatos.keys():
        formatos["default"] = makeXlFormat(borde="")
    for k in formatos.keys():
        dFmts[k] = bk.add_format(formatos[k])

    # Hojas
    for h in hojas:
        writeSheet(bk, h, dFmts)
    bk.close()


def writeSheet(book, hoja, dFmts):
    """ Crea una hoja en el objeto libro dado.

    :param book: objeto libro en el que se va a esribir.
    :param hoja: especificación de una hoja.
    :param dFmts: diccionario de formatos.
    """
    sh = agregaHoja(book, hoja["nombre"])
    pos = 0
    if "titulos" not in hoja.keys():
        hoja["titulos"] = ""
    if "anchos" not in hoja.keys():
        hoja["anchos"] = ""
    if "header" not in hoja.keys():
        hoja["header"] = ""
    if "datos" not in hoja.keys():
        hoja["datos"] = ""
    if "footer" not in hoja.keys():
        hoja["footer"] = ""
    if "celdas" not in hoja.keys():
        hoja["celdas"] = ""

    if hoja["anchos"]:
        sh = mkAnchos(sh, hoja["anchos"])
    if hoja["titulos"]:
        tits = hoja["titulos"]
        sh = addTitles(sh, tits, dFmts)
        pos = tits["fila"]+len(tits["datos"])+tits["despues"]
    if hoja["header"]:
        sh = addHeader(sh, hoja["header"], pos, dFmts)
        pos += hoja["header"]["despues"]+1
    if hoja["datos"]:
        sh = addDatos(sh, hoja["datos"], pos, dFmts)
        if "despues" in hoja["datos"].keys():
            pos += len(hoja["datos"]["renglones"]) + \
                hoja["datos"]["despues"] + 1
        else:
            pos += 1
    if hoja["footer"]:
        sh = addFooter(sh, hoja["footer"], pos, dFmts)
    if hoja["celdas"]:
        sh = addCeldas(sh, hoja["celdas"], dFmts)


def addCeldas(hoja, celdas, formatos):
    pass


def addTitles(hoja, titulos, formatos):
    """ Agregar títulos a una hoja.

    :param hoja: objeto hoja a modificar.
    :param titulos: diccionario con los títulos para la hoja.
    :param formatos: formatos para los títulos.

    :returns objeto hoja modificado.

    """
    if "fila" in titulos.keys():
        fila = titulos["fila"]
    else:
        fila = 0
    if "columna" in titulos.keys():
        columna = titulos["columna"]
    else:
        columna = 0
    if "datos" in titulos.keys():
        if "formatos" not in titulos.keys():
            titulos["formatos"] = []
        while len(titulos["formatos"]) < len(titulos["datos"]):
            titulos["formatos"].append("default")
        for i in range(len(titulos["datos"])):
            writeCell(hoja, fila+i, columna, titulos["datos"][i],
                      formatos[titulos["formatos"][i]])
    return hoja


def addHeader(hoja, header, renglon, formatos):
    """ Agrega encabezados a la hoja.

    :param hoja: objeto hoja a modificar.
    :param header: lista de etiquetas para columnas.
    :param renglon: renglón para colocar los encabezados.
    :param formatos: lista de formatos para las columnas.

    :returns Objeto hoja modificado.
    """
    if "formato" not in header.keys():
        header["formato"] = "default"
    for i in range(len(header["renglon"])):
        writeCell(hoja, renglon, i, header["renglon"][i],
                  formatos[header["formato"]])
    return hoja


def addDatos(hoja, datos, renglon, formatos):
    """ Agrega contenido a la hoja.

    :param hoja: objeto hoja a modificar.
    :param header: lista de registros para los renglones.
    :param renglon: renglón inicial para los datos.
    :param formatos: lista de formatos.

    :returns Objeto hoja modificado.
    """
    # print(datos)
    if "formatos" not in datos.keys():
        datos["formatos"] = []
    columnas = max([len(x) for x in datos["renglones"]])
    while len(datos["formatos"]) < columnas:
        datos["formatos"].append("default")

    for x in datos["renglones"]:
        # print("renglon",x,datos["formatos"])
        for i in range(len(x)):
            # print("addDatos",i,end=" ")
            # print(datos["formatos"][i],end=" ")
            # print(x[i])
            writeCell(hoja, renglon, i, x[i], formatos[datos["formatos"][i]])
        renglon += 1
    return hoja


def addFooter(hoja, footer, renglon, formatos):
    """ Agrega contenido a una hoja después de los datos.

    :param hoja: objeto hoja a modificar.
    :param footer: especificación del footer.
    :param renglon: renglón inicial para los datos.
    :param formatos: lista de formatos.

    :returns Objeto hoja modificado.
    """
    if "antes" in footer.keys():
        renglon += footer["antes"]
    addHeader(hoja, footer, renglon, formatos)


def makeXlFormat(font="Arial", size=10, tipo=0, btipo=0, numero="0",
                 fontcolor="black", color="", align="", borde=""):
    """ Crea un objeto de formato.

    :param font: nombre del font para el parámetro.
    :param size: tamaño del font.
    :param tipo:
    :param borde:
    :param btipo:
    :param numero:
    :param fontcolor:
    :param color:
    :param align:

    :returns diccionario con la especificación del formato.
    """
    d = {"font_name": font, "font_size": size, "font_color": fontcolor,
         "align": align, "num_format": numero}
    if color:
        d["bg_color"] = color
    if tipo == 1:
        d["bold"] = True
    elif tipo == 2:
        d["italic"] = True
    elif tipo == 3:
        d["bold"] = True
        d["italic"] = True

    if borde == "":
        pass
    elif borde == "all":
        d["border"] = btipo
    elif borde != "":
        while len(borde) < 4:
            borde += "0"
        d["left"] = int(borde[0])
        d["right"] = int(borde[1])
        d["bottom"] = int(borde[2])
        d["top"] = int(borde[3])
    # print(d)
    return d


def writeSheet0(book, hoja):
    """ Book es un objeto creado with creaXl, hoja una estructura de hoja.
    """
    if "titulos" in hoja.keys() and hoja["titulos"]:
        hoja["titulos"]["formatos"] = [formatos[x]
                                       for x in hoja["titulos"]["formatos"]]
    if "datos" in hoja.keys():
        for i in range(len(hoja["datos"][1])):
            hoja["datos"][1][i] = [formatos[x] for x in hoja["datos"][1][i]]
    sh = agregaHoja(book, hoja["nombre"])
    if "anchos" in hoja.keys() and hoja["anchos"]:
        sh = mkAnchos(sh, hoja["anchos"])
    if "titulos" in hoja.keys() and hoja["titulos"]:
        sh = addTitles(sh, hoja["titulos"])
    if "titulos" in hoja.keys() and hoja["titulos"] and \
       "fila" in hoja["titulos"].keys():
        fila = hoja["titulos"]["fila"]+len(hoja["titulos"]["textos"])+1
    else:
        fila = 0
    if "datos" in hoja.keys() and "titulos" in hoja.keys() and hoja["datos"]:
        sh = addDatos(sh, hoja["datos"], fila)


def addTitles0(sh, titulos):
    global formatos
    for i in range(len(titulos["textos"])):
        writeCell(sh, titulos["fila"] + i,
                  titulos["columna"],
                  titulos["textos"][i],
                  titulos["formatos"][i])
    return sh


def addDatos0(hoja, datos, fila):
    global formatos
    f = fila
    for i in range(len(datos[0])):
        writeRenglonFormat(hoja, f, datos[0][i], datos[1][i])
        f += 1
    return hoja


def hojaNueva(nombre="Hoja1"):
    """ Crea un diccionario con el nombre de la hoja para agregar datos.

    :param nombre: nombre de la hoja a crear.

    :returns diccionario con nombre como dato de la llave "nombre"
    Se agregarán llaves predefinidas y los datos correspondientes a este
    diccionario para crear la especificación de una hoja.
    """
    return {"nombre": nombre}


def mkXlSimple(datos, archivo, nombres=[], ancho=40):
    """ Crea un archivo de excel solamente con los renglones.

    :param datos: Lista de listas de renglones.
    :param archivo: Nombre del archivo a crear.
    :param nombres: Lista de nombres para las hojas.
    :param ancho: Ancho máximo para las columnas.

    Modificando para que los números tengan decimales.
    """
    formatos = {}
    f2 = makeXlFormat(numero="#,##0.00", borde="1111")
    formatos["000"] = f2

    i = 1
    while len(nombres) < len(datos):
        nombres.append("Hoja" + str(i))
        i += 1
    hojas = []
    for i in range(len(datos)):
        h = mkHojaSimple(datos[i], nombres[i], ancho)
        hojas.append(h)

    writeBook(hojas, formatos, archivo)


def mkHojaSimple(datos, nombre, ancho):
    """ Crea un diccionario hoja simple.

    :param datos: lista de renglones.
    :param nombre: nombre de la hoja.
    :param ancho: tope para los anchos de las columnas.
    """
    # Calcular los anchos.
    lgo = max([len(str(x)) for x in datos])
    anchos = [10] * lgo
    for x in datos[1:]:
        for i in range(len(x)):
            if len(str(x[i])) > anchos[i]:
                anchos[i] = min(ancho, 1.4 * len(str(x[i])))

    h = {}
    h["nombre"] = nombre
    h["datos"] = {}
    h["datos"]["renglones"] = datos
    h["anchos"] = anchos
    h["datos"]["formatos"] = ["000"] * len(anchos)
    return h


if __name__ == '__main__':
    hoja = {}
    hoja["nombre"] = "Test"
    formatos = {}
    hoja["anchos"] = [11, 11, 11, 11, 25, 25, 11, 11]
    hoja["header"] = {}
    f = makeXlFormat(borde="2222", color="silver", align="center")
    hoja["header"]["formato"] = "hdr"
    formatos["hdr"] = f
    hoja["header"]["renglon"] = ["Serie", "Numero", "Fecha", "Operador",
                                 "Nombre", "Observaciones", "Saldo", "Cuenta"]
    hoja["header"]["despues"] = 0
    hoja["datos"] = {}
    hoja["datos"]["renglones"] = [["A", 1002897, 41843, 294,
                                   "LOZADA LOPEZ SILVESTRE",
                                   "MADERO AGUASCALIENTES", 1700, 18327],
                                  ["A", 1002898, 41843, 241,
                                   "BARBOZA GONZALEZ JOSE",
                                   "CASETAS DE REGRESO", 1200, 18324]]
    hoja["datos"]["despues"] = 0
    f1 = makeXlFormat(numero="dd/mm/yyyy", borde="1111")
    formatos["fecha"] = f1
    f2 = makeXlFormat(numero="#,##0.00", borde="1111")
    formatos["000"] = f2
    f3 = makeXlFormat(borde="1111")
    formatos["bnor"] = f3
    formatos["def"] = {"font_name": "Arial", "font_size": 10}
    hoja["datos"]["formatos"] = ["def", "def", "fecha", "bnor", "bnor",
                                 "bnor", "000", "bnor"]
    print(formatos.keys())
    writeBook([hoja], formatos, "test21.xlsx")
    for k in formatos.keys():
        print(k,formatos[k])
