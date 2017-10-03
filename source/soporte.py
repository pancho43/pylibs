# -*- coding: utf-8 -*-

import os
import time
import zipfile

import fechas as fe
# ---------------------------------------------------------------------------
# Funciones de archivos
# ---------------------------------------------------------------------------


def listFiles(ruta, recurse=1, tipo=None):
    """ Regresa una lista de todos los archivos con tamaño y ruta.

    :param ruta: Ruta de la carpeta a leer.
    :param recurse: Si 1, procesa recursivamente subdirectorios.
    :param tipo: Filtra el tipo de contenido a regresar.

    El parámetro tipo puede ser: "f" para archivos, "d" para directorios,
    "x" para otros. Si es None, regresa todo.

    """
    lista = []
    try:
        l = os.listdir(ruta)
    except:
        return []
    for x in l:
        nm = os.path.join(ruta, x)
        if os.path.isfile(nm):
            t = "f"
        elif os.path.isdir(nm):
            t = "d"
        else:
            t = "x"
        lista.append([ruta, x, t, os.stat(nm).st_size])
        if t == "d" and recurse == 1:
            lista += listFiles(nm, recurse)
    if tipo:
        return [x for x in lista if x[2] == tipo]
    else:
        return lista


def carpetas(ruta):
    """ Versión alternativa para directorioas.
    """
    lista = []
    try:
        l = os.listdir(ruta)
    except:
        return []
    for x in l:
        nm = os.path.join(ruta, x)
        if os.path.isdir(nm):
            lista.append([ruta, x, "d", os.stat(nm).st_size])
            lista += carpetas(nm)
    return lista


def listArchivos(ruta, recurse=1):
    """ Regresa una lista de archivos en la ruta.
    """
    return listFiles(ruta, recurse, tipo="f")


def listDirectorios(ruta, recurse=1):
    """ Regresa una lista de subdirectorios en la ruta.
    """
    return listFiles(ruta, recurse, tipo="d")


def nomArchivo(archivo):
    """ Regresa el nombre completo de archivo.

    :param archivo: Es un registro regresado por listFiles.
    """
    # return os.path.join(archivo[0], archivo[1])
    return os.path.join(archivo[0], archivo[1]).replace("\\", "/")


def leerTexto(archivo, code="utf-8"):
    """ Lee un archivo de texto.
    """
    return open(archivo, mode="r", encoding=code).read()


def leerLista(archivo, borrar="", code="utf-8"):
    """ Lee un archivo como lista de líneas.

    :param archivo: archivo a leer.
    :param borrar: lista de caracteres a eliminar de cada línea.
    :param code: encoding a utilizar al leer.
    """
    if not borrar:
        return [x.strip()
                for x in open(archivo, "r", encoding=code).readlines()]
    else:
        return [x.strip(borrar)
                for x in open(archivo, "r", encoding=code).readlines()]


def leerDatos(archivo, sep="|", code="utf-8"):
    """ Lee registros de un archivo, grabados como texto delimitado.

    :param archivo: Archivo a leer.
    :param sep: Separador usado en los registros.
    :param code: Encoding a utilizar al leer el archivo.
    """
    if sep:
        return [x.strip().split(sep)
                for x in open(archivo, "r", encoding=code).readlines()]
    else:
        return [x.strip().split()
                for x in open(archivo, "r", encoding=code).readlines()]


def leerDict(archivo, sep="|", llave=0):
    return {x[llave]: x[:llave] + x[llave + 1:]
            for x in leerDatos(archivo, sep)}


def leerDictSimple(archivo, sep="|", llave=0, dato=1):
    return {x[llave]: x[dato] for x in leerDatos(archivo, sep)}


def saveDatos(datos, archivo, sep="|", code="utf-8"):
    """Salva una lista de listas como texto separado por "sep".
       Asume que los elementos de cada dato ya son texto.
    """
    open(archivo, "w", encoding="UTF-8").write("\n".join([sep.join(x)
                                                          for x in datos]))


def saveLista(lista, archivo, code="utf-8"):
    """ Salva una lista de textos.
    """
    open(archivo, mode="w", encoding=code).write("\n".join(lista))


def saveTexto(texto, archivo, code="utf-8"):
    """ Salva un archivo de texto.
    """
    open(archivo, mode="w", encoding=code).write(texto)


def unzipFile(zf, archivo):
    z = zipfile.ZipFile(zf)
    if archivo in z.namelist():
        return z.read(archivo)
    else:
        return ""


def joinText(archivos, salida):
    open(salida, "w", encoding="utf-8").write("\n".join(
        [open(nomArchivo(a)).read() for a in archivos]))

# ---------------------------------------------------------------------------
# Funciones de texto y listas
# ---------------------------------------------------------------------------


def splitEqual(texto, ln, last=False):
    """ Divide texto en partes iguales de longitud ln. Si last es True y hay
        un remanente menor, lo agrega tambien.
    """
    l = []
    while len(texto) >= ln:
        l.append(texto[:ln])
        texto = texto[ln:]
    if len(texto) > 0 and last:
        l.append(texto)
    return l


def splitLens(texto, lns):
    """ Divide texto en porciones con las longitudes dadas en lens.
        Se asume que la suma de lns no sobrepasa la longitud de texto.
    """
    l = []
    p = 0
    for x in lns:
        l.append(texto[p:p+x])
        p += x
    return l


def splitPosLen(texto, poss):
    """ poss son pares indicando inicio y longitud.
    """
    return [texto[x[0]:x[0]+x[1]] for x in poss]


def list2dict(l, kis, poss):
    d = {}
    for i in range(len(kis)):
        d[kis[i]] = l[poss[i]]
    return d


def isSubList(s, l, may=0):
    if may:
        return isSubList([x.upper() for x in s],
                         [x.upper() for x in l])
    else:
        for x in s:
            if x not in l:
                return False
        return True


def sublistIndexes(s, l, may=0):
    if not isSubList(s, l, may):
        return []
    if may:
        return sublistIndexes([x.upper() for x in s],
                              [x.upper() for x in l])
    else:
        return [l.index(x) for x in s]


def subLista(lista, indices):
    return [lista[i] for i in indices]


def listList(lista):
    """ Imprime una lista, registro por registro."""
    for x in lista:
        print(x)


def listDict(dic):
    """ Imprime un diccionario, llave por llave."""
    for k in dic.keys():
        print(k, " : ", dic[k])


def dispTwo(r, s):
    """ Despliega dos listas, lado a lado.
    """
    for i in range(max(len(r), len(s))):
        if i < len(r):
            print(r[i], end='\t')
        else:
            print("", end='\t')
        if i < len(s):
            print(s[i])
        else:
            print("")

# ---------------------------------------------------------------------------
# Funciones de fecha y hora
# ---------------------------------------------------------------------------


def fechaYhora():
    """Regresa una dupla con la fecha y hora del sistema.

    La fecha en formato (a,m,d) y la hora en formato (h,m,s)
    """
    t = time.localtime()[:6]
    return ([str(x) for x in t[:3]], [str(x) for x in t[3:]])


def hoy():
    """ Regresa la fecha del sistema en formato aaaammdd"""
    f = fechaYhora()[0]
    return f[0] + f[1].rjust(2, "0") + f[2].rjust(2, "0")


def today():
    """ Regresa la fecha del sistema en formato d/m/a"""
    return "/".join(fechaYhora()[0][-1::-1])


def now():
    return ":".join([x. rjust(2, "0") for x in fechaYhora()[1]])


# ---------------------------------------------------------------------------
# Funciones de presentación de números.
# ---------------------------------------------------------------------------


def str2float(s):
    if s:
        return float(s)
    else:
        return 0.0


def float2cents(imp):
    """Regresa el número de centavos en un importe.

    """
    s = str(imp)
    pos = s.find(".")
    if pos == -1:
        return int(s + "00")
    else:
        while len(s) < pos + 4:
            s += "0"
        if int(s[pos+3]) > 4:
            return int(s[:pos+3].replace(".", "")) + 1
        else:
            return int(s[:pos+3].replace(".", ""))


def float2centsstr(imp):
    """ Regresa un importe convertido a string con dos decimales.
    """
    x = str(float2cents(imp))
    while len(x) < 3:
        x = "0" + x
    return insertChar(x, ".", 2)


def cents2str(cents):
    s = str(cents)
    if s[0] == '-':
        return '-' + cents2str(s[1:])
    while len(s) < 3:
        s = "0" + s
    return insertChar(s, ".", 2)


def str2cents(s):
    return float2cents(float(s))


def str2centsstr(s):
    return float2centsstr(float(s))


def insertChar(txt, c, pos):
    """ Inserta un caracter en un texto en la posición dada.
    """
    return txt[:-pos] + c + txt[-pos:]


def dotProduct(l, m):
    """Producto punto clásico de dos vectores.
    """
    return sum([l[i]*m[i] for i in range(len(m))])


def extraeDato(datos, llaves, col_llave, col_dato):
    """ Obtiene los valores correspondientes a una lista de llaves.

        Datos contiene una serie de registros y llaves los valores de
        referencia a buscar. col_llave y col_dato son las columnas
        correspondientes.
        Regresa una lista de los valores en col_dato en los registros
        con llaves en col_llave.
        Falla si alguna de las llaves no aparece en los registros.
    """
    d = {x[col_llave]: x[col_dato] for x in datos}
    return [d[x] for x in llaves]


def extraeDatos(datos, labels, clave):
    """Extraer datos de una lista de registros etiquetados.

    Dada una lista de registros donde hay un renglón con etiquetas,
    se localiza el renglón que contenga las pasadas como parámetro y
    se determina la columna correspondiente a cada una.
    Se regresa la lista de registros formados por estas columnas a partir
    del renglón siguiente al encabezado y que tienen un valor no nulo
    en la columna etiquetada con clave.
    """
    poss = []
    renglon = 0
    for x in datos:
        if isSubList(labels, x):
            poss = sublistIndexes(labels, x)
            renglon = datos.index(x)
            ki = datos[renglon].index(clave)
            break
    if not poss:
        return []

    return[[x[i] for i in poss] for x in datos[renglon + 1:] if x[ki]]


def conteo(l):
    d = {}
    for x in l:
        if x not in d.keys():
            d[x] = 0
        d[x] += 1
    return [[k, d[k]] for k in d.keys()]


def promedio(l):
    return sum(l)/len(l)


def closer2mean(l):
    av = promedio(l)
    d = abs(l[0]-av)
    for x in l:
        e = abs(l[0]-av)
        if e < d:
            d = e
    return x


def relev(pares):
    s = pares[0][0]
    c = pares[0][1]
    for x in pares:
        if x[1] > c:
            c = x[1]
            s = x[0]
    return s


# --------------------------------------------------------------------------
# Funciones de archivos con selector.
# --------------------------------------------------------------------------


def cargarDatos(archivo, selector, sep="|"):
    return [x[1:] for x in leerDatos(archivo, sep) if int(x[0]) == selector]


# --------------------------------------------------------------------------
# Funciones de infraestructura.
# --------------------------------------------------------------------------


def leerConfig(archivo):
    """ Lee un archivo de configuración y crea un diccionario de opciones.

    :param archivo: Archivo con la configuración.
    :return: diccionario de opciones.
    El separador en las líneas de texto es "=", se quitan espacios de las
    llaves y los valores se incluyen entre comillas, que deben retirarse.
    """

    def mkPair(x):
        k = x[0].strip()
        pos = x[1].find('"')
        if pos == -1:
            pos = x[1].find("'")
            fin = x[1].find("'", pos + 1)
        else:
            fin = x[1].find('"', pos + 1)
        v = x[1][pos + 1: fin]
        return (k, v)

    l = leerDatos(archivo, sep="=")
    l = [mkPair(x) for x in l]
    d = {x[0]: x[1] for x in l}
    return d


# --------------------------------------------------------------------------
# Otras funciones.
# --------------------------------------------------------------------------


def isInt(tx):
    for c in tx:
        if c not in "0123456789":
            return False
    return True


def isDecimal(tx):
    if "." in tx:
        if tx.count(".") > 1:
            return False
        tx = tx.replace(".","")
    return isInt(tx)


def expandListNums(tx):
    """ Convierte una lista abreviada de números enteros en la lista completa.

    :param tx: texto con la lista abreviada.

    La lista abreviada es un texto  con elementos separados con comas.
    Cada elemento es un número o un rango. Un rango es una parega de números
    separados con un signo : o -. Solamente se puede usar un signo en cada
    texto.
    """
    if ":" in tx:
        sep = ":"
    elif "-" in tx:
        sep = "-"
    else:
        sep = "|"          # No se recomienda.

    l = tx.split(",")
    s = []
    for x in l:
        if sep in x:
            ft, lt = x.split(sep)
            if isInt(ft) and isInt(lt):
                s += list(range(int(ft), int(lt)+1))
        else:
            if isInt(x):
                s.append(int(x))
    return s


def compressListNums(ns, sep=":"):
    """ Comprime una lista de números usando el separador dado.

    :param ns: Lista de enteros.
    :param sep: Separador para rangos. Sólo se admiten - o \|.

    Se ordena la lista, se valida el separador, se aplica el default si
    no es válido.
    """

    tx = ""
    ns.sort()
    fst = -1
    act = -1
    for n in ns:
        if fst == -1:
            fst = n
            act = n
        elif n == act + 1:
            act = n
        elif fst == act:
            tx += str(fst) + ","
            fst = n
            act = n
        else:
            tx += str(fst)+sep+str(act)+","
            fst = n
            act = n
    if fst == act:
        tx += str(fst)
    else:
        tx += str(fst)+sep+str(act)
    return tx


def valRango(valor, rango, abierto=0):
    if abierto:
        return (valor < rango[1] and valor > rango[0])
    else:
        return (valor <= rango[1] and valor >= rango[0])


def valRangos(valor, rangos, abierto=0):
    for x in rangos:
        if valRango(valor, x, abierto):
            return True
    return False


def valFecha(texto):
    texto = texto.strip()
    fecha = []
    curr = ""
    for c in texto:
        if c in "0123456789":
            curr += c
        else:
            fecha.append(int(curr))
            curr = ""
    fecha.append(int(curr))
    if len(fecha) == 3:
        l = [[fecha[2], fecha[1], fecha[0]], [fecha[0], fecha[1], fecha[2]],

             [fecha[2], fecha[0], fecha[1]]]
    elif len(fecha) == 1:
        fecha = str(fecha[0])
        if len(fecha) == 8:
            l = [[int(fecha[4:]), int(fecha[2:4]), int(fecha[:2])],
                 [int(fecha[:4]), int(fecha[4:6]), int(fecha[6:])],
                 [int(fecha[4:]), int(fecha[:2]), int(fecha[2:4])]]
        elif len(fecha) == 6:
            l = [[int(fecha[4:]), int(fecha[2:4]), int(fecha[:2])],
                 [int(fecha[:2]), int(fecha[2:4]), int(fecha[4:])],
                 [int(fecha[4:]), int(fecha[:2]), int(fecha[2:4])]]
        else:
            return ""
    else:
        return ""
    for x in l:
        f = mkFecha(x)
        if fe.valFecha(f) and f:
            return f
    return ""


def mkFecha(l):
    if len(l) != 3:
        return ""
    l = [int(x) for x in l]
    if l[0] < 30:
        a = l[0]+2000
    elif l[0] < 99:
        a = l[0] + 1900
    elif l[0] > 1900:
        a = l[0]
    else:
        return ""
    return str(a) + str(l[1]).rjust(2, "0") + str(l[2]).rjust(2, "0")


def mkHora():
    return ":".join(map(lambda x: x.rjust(2, "0"), fechaYhora()[1]))


def mkHeadersTxt(groups, headers):
    """ Crea renglones de texto con los encabezados adecuadamente espaciados.

    :param groups: Textos para primer renglón, incluye texto y alineación.
    :param headers: Listas de textos para cada grupo, incluye texto, ancho y
     alineación.
    """
    while len(groups) < len(headers):
        groups.append(["", "l"])
    while len(groups) > len(headers):
        headers.append([["", "l", 1]])

    # Calcular ancho de los grupos.
    for i in range(len(groups)):
        groups[i].append(max(len(groups[i][0])+2,
                             sum([x[2] for x in headers[i]])))

    s = []
    r = []
    for g in groups:
        if g[1] == "c":
            r.append(g[0].center(g[2]))
        elif g[1] == "r":
            r.append(g[0].rjust(g[2]))
        else:
            r.append(g[0].ljust(g[2]))
    s.append(" ".join(r))
    s.append(" ".join(["-" * len(x) for x in r]))

    r = []
    for h in headers:
        tx = ""
        for x in h:
            if x[1] == "c":
                tx += x[0].center(x[2])
            elif x[1] == "r":
                tx += x[0].rjust(x[2])
            else:
                tx += x[0].ljust(x[2])
        r.append(tx)
    s.append(" ".join(r))
    s.append("=" * len(s[-1]))

    return s


def includeOnly(tx, chars):
    s = ""
    for x in tx:
        if x in chars:
            s += x
    return s


def chkDigito(afil):
    if len(afil) != 11:
        return False
    return dv(afil[:10]) == int(afil[10])


def dv(tx, deb=0):
    if len(tx) != 10:
        return ""

    f = 1
    s = 0
    for x in tx:
        n = int(x) * f
        if n > 9:
            n -= 9
        s += n
        if f == 1:
            f = 2
        else:
            f = 1
        if deb:
            print(x, n, s)
    if deb:
        print("Suma:", s)
    return (10 * (s // 10 + 1) - s) % 10


def remplazo(modelo, datos):
    """ Reemplaza los campos en modelo con los elementos en datos.

    :param modelo: linea de texto con marcadores para substituir.
    :param datos: lista de valores para sustituir en modelo.
    :returns: linea de texto con datos incrustado en modelo.
    """
    i = 1
    tx = modelo
    for x in datos:
        tx = tx.replace("<<" + str(i) + ">>", str(x))
        i += 1
    return tx
