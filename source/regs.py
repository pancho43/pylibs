# -*- coding: utf-8 -*-


def products(tx, digs):
    ds = digs
    while len(ds) < len(tx):
        ds += digs
    return [int(tx[i]) * int(ds[i]) for i in range(len(tx))]


def sumDigitos(num):
    s = num
    while s > 10:
        s1 = 0
        while num > 10:
            s1 += num % 10
            num = num // 10
        s = s1 + num
    return s


def dvCard(card):
    prs = products(card[:-1], "12")
    prs = [sumDigitos(x) for x in prs]
    d = (sum(prs) - 1) % 10 + 1
    return 10 - d


def dvClabe(clabe):
    prs = products(clabe[:-1], "371")
    prs = [x % 10 for x in prs]
    return (10 - sum(prs) % 10) % 10


def valClabe(clabe):
    return dvClabe(clabe) == clabe[-1]


def myIndex(dato, c):
    """Como el método index, pero no falla si el dato no existe."""
    if c in dato:
        return dato.index(c)
    else:
        return -1


def segCons(tx):
    """ Regresa la segunda consonante del texto."""
    for c in tx[1:]:
        if c not in vocales:
            if c == "Ñ":
                return "X"
            else:
                return c
    return "X"


def chgFirst(texto, dato, nuevo):
    """Checa si el texto empieza con dato y reeemplaza con nuevo."""
    if texto.startswith(dato):
        return nuevo + texto[len(nuevo) + 1:]
    else:
        return texto


def normaliza(texto, wrongchars, rightchars):
    """ Reemplaza los caracteres en wrongchars con los de rightchars.
    """
    for i in range(len(wrongchars)):
        texto = texto.replace(wrongchars[i], rightchars[i])
    return texto


def valFecha(fecha):
    """ Valida si una fecha en formato aaaammdd es válida."""
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if not fecha:
        return False
    a, m, d = int(fecha[:4]), int(fecha[4:6]), int(fecha[6:])
    if min(a, m, d) <= 0:
        return False
    if m > 12:
        return False
    if m != 2:
        if d > dias[m - 1]:
            return False
    else:
        if a == 2000 or a % 4 == 0:
            if d > 29:
                return False
        else:
            if d > 28:
                return False
    return True


def mkRfc(apellido1, apellido2, nombre, fecha, curp=""):
    """ Construye el RFC a partir de apellidos, nombre y fecha.
    """
    apellido1 = normaliza(apellido1.strip().upper(), "áéíóúÁÉÍÓÚüÜ",
                          "aeiouAEIOUuU")
    apellido2 = normaliza(apellido2.strip().upper(), "áéíóúÁÉÍÓÚüÜ",
                          "aeiouAEIOUuU")
    nombre = normaliza(nombre.strip().upper(), "áéíóúÁÉÍÓÚüÜ",
                       "aeiouAEIOUuU")
    ap1 = apellido1
    ap2 = apellido2
    nom = nombre

    if len(nom) == 0:
        return ""

    if valFecha(fecha):
        nacim = fecha[2:]
    else:
        # print("Fecha incorrecta")
        return ""

    if len(" ".join((ap1, ap2, nom))) < 6 or (len(ap1) == 0 and len(ap2) == 0):
        # print("Nombre incorrecto")
        return ""

    # eliminar conectores de los nombres y apellidos
    for w in mods:
        ap1 = ap1.replace(w, "")
        ap2 = ap2.replace(w, "")
        nom = nom.replace(w, "")

    if " " in nom:
        for nomb in comunes:
            if nomb in nom:
                nom = nom.replace(nomb, "")

    ap1 = chgFirst(ap1, "CH", "C")
    ap1 = chgFirst(ap1, "LL", "L")
    ap2 = chgFirst(ap2, "CH", "C")
    ap2 = chgFirst(ap2, "LL", "L")
    nom = chgFirst(nom, "CH", "C")
    nom = chgFirst(nom, "LL", "L")

    letras = calcLetras(ap1, ap2, nom)
    if letras in evitar:
        if curp:
            letras = letras[0] + "X" + letras[2:]
        else:
            letras = letras[:3] + "X"
    rfc = letras + nacim
    rfc += homonimo(apellido1, apellido2, nombre)
    rfc += digito(rfc)
    return rfc


def digito(rfc):
    """ Calcula el dígito verificador del rfc.
    """
    txt = ""
    for c in rfc:
        if c == " ":
            c = "*"
        pos = myIndex(anex31, c)
        if pos > 0:
            txt += anex32[pos]
        else:
            txt += "00"
    sumas = 0
    factor = 13
    for i in range(12):
        sumas += int(txt[2 * i: 2 * i + 2]) * factor
        factor -= 1
    residuo = sumas % 11
    if residuo == 0:
        d = 0
    else:
        d = 11 - residuo
        if d == 10:
            d = "A"
    return str(d)


def digitoCurp(curp):
    """ Calcula el dígito verificador de la CURP.
    """
    txt = ""
    for c in curp:
        if c == " ":
            c = "*"
        pos = myIndex(anex31, c)
        if pos > 0:
            txt += anex32[pos]
        else:
            txt += "00"
    sumas = 0
    factor = 18
    for i in range(17):
        sumas += int(txt[2 * i: 2 * i + 2]) * factor
        factor -= 1
    residuo = sumas % 10
    if residuo == 0:
        d = 0
    else:
        d = 10 - residuo
        if d == 10:
            d = "A"
    return str(d)


def calcLetras(ap1, ap2, nombre):
    """ Calcula las cuatro letras iniciales de RFC y CURP.
    """
    if len(ap1) == 0:
        lets = ap2[:2] + nombre[:2]
    elif len(ap2) == 0:
        lets = ap1[:2] + nombre[:2]
    elif len(ap1) < 3:
        lets = ap1[0] + ap2[0] + nombre[:2]
    else:
        lets = ap1[0]
        for c in ap1[1:]:
            if c in vocales:
                break
        lets += c
        lets += ap2[0] + nombre[0]
    return lets


def homonimo(ap1, ap2, nom):
    """ Calcula los dos caracteres de la homoclave del rfc.
    """
    txt = " ".join((ap1, ap2, nom))
    txt = txt.replace(" ", "*")
    valores = "0"
    for c in txt:
        pos = myIndex(anex11, c)
        if pos > 0:
            valores += anex12[pos]
        else:
            valores += "00"
    sumas = 0
    i = 0
    while i < len(valores) - 1:
        sumas += int(valores[i: i + 2]) * int(valores[i + 1])
        i += 1
    # num = int(str(sumas).ljust(4)[-3:])
    num = sumas % 1000
    cociente = num // 34
    residuo = num % 34
    k1 = str(cociente).rjust(2, "0")
    k2 = str(residuo).rjust(2, "0")
    pos1 = myIndex(anex21, k1)
    if pos1 > 0:
        homo = anex22[pos1]
    else:
        homo = "1"
    pos2 = myIndex(anex21, k2)
    if pos2 > 0:
        homo += anex22[pos2]
    else:
        homo += "1"
    return homo


def homon2(ap1, ap2, nom):
    """ Calcula los dos caracteres de la homoclave del rfc.
    """
    txt = " ".join((ap1, ap2, nom))
    txt = txt.replace(" ", "*")
    valores = "0"
    for c in txt:
        pos = myIndex(anex11, c)
        if pos > 0:
            valores += anex12[pos]
        else:
            valores += "00"
    sumas = 0
    i = 0
    print(valores)
    while i < len(valores) - 1:
        sumas += int(valores[i: i + 2]) * int(valores[i + 1])
        i += 1
    # num = int(str(sumas).ljust(4)[-3:])
    print(sumas)
    num = sumas % 1000
    cociente = num // 34
    residuo = num % 34
    print(cociente, residuo)
    k1 = str(cociente).rjust(2, "0")
    k2 = str(residuo).rjust(2, "0")
    pos1 = myIndex(anex21, k1)
    if pos1 > 0:
        homo = anex22[pos1]
    else:
        homo = "1"
    pos2 = myIndex(anex21, k2)
    if pos2 > 0:
        homo += anex22[pos2]
    else:
        homo += "1"
    return homo


def testRfc(rfc):
    """ Verifica el dígito verificador.

    Pendiente checar la fecha, y que las letras sean viables.
    """
    return digito(rfc[:12]) == rfc[13]


def testCurp(curp):
    """ Checa el dígito verificador.

    Pendiente checar el resto.
    """
    return digitoCurp(curp[:17]) == curp[17]


def mkCurp(apellido1, apellido2, nombre, fecha, estado, sexo,
           rfc="", digito="0"):
    """Curp incompleta.

    Siempre con cero en el penúltimo dígito.
    No tenemos acceso a la base de datos.
    """
    apellido1 = apellido1.strip().upper()
    apellido2 = apellido2.strip().upper()
    nombre = nombre.strip().upper()
    estado = estado.strip().upper()
    sexo = sexo.strip().upper()

    ap1 = apellido1
    ap2 = apellido2
    _nom = nombre

    for w in mods:
        ap1 = ap1.replace(w, "")
        ap2 = ap2.replace(w, "")
        _nom = _nom.replace(w, "")

    if " " in _nom:
        for nomb in comunes:
            if nomb in _nom:
                _nom = _nom.replace(nomb, "")

    if not estado:
        return ""

    if not sexo:
        return ""

    if len(estado) > 2:
        estado = dEstados[estado]

    if not rfc or not testRfc(rfc):
        tx = mkRfc(apellido1, apellido2, nombre, fecha)
        if not tx:
            return ""
        else:
            tx = mkRfc(apellido1, apellido2, nombre, fecha)[:10]
    else:
        tx = rfc[:10]

    noms = nombre.split()
    if len(noms) > 1:
        if noms[0] + " " in comunes:
            nom = noms[1]
        else:
            nom = noms[0]
    else:
        nom = nombre
    # tx += sexo + estado + segCons(ap1)+segCons(ap2)+segCons(_nom)+digito
    tx += sexo + estado + segCons(ap1) + segCons(ap2) + segCons(nom) + digito
    tx += digitoCurp(tx)
    return tx


def calcDv(text):
    """ Calcula el dígito verificador de un NSS.

    Para uso por chkDv
    """
    # f = 1
    p = 1
    suma = 0
    for c in text:
        s = int(c) * p
        if s > 9:
            s = s // 10 + s % 10
        suma += s
        if p == 1:
            p = 2
        else:
            p = 1
    dig = str(10 - suma % 10)
    if dig == "10":
        return "0"
    else:
        return dig


def chkDv(text):
    """ Verifica un NSS, checando el dv.
    """
    if len(text) != 11:
        return False
    else:
        return calcDv(text[:10]) == text[10]


def mkNombre(texto):
    """ Separa los componentes de un nombre.

    Separa el parámetro en partes, tomando en cuenta las partículas
    usuales. Regresa una lista de elementos, múltiples nombres aparecen
    separados.
    """
    texto = "/" + " ".join(texto.split())
    texto = texto.replace(" ", "/")
    texto = texto.upper()
    particulas = ("/DE/LA/", "DE/LOS/", "/DE/", "/DEL/", "/Y/", "/SAN/",
                  "/VON/", "/SANTA/")
    for x in particulas:
        texto = texto.replace(x, x[0] + x[1:].replace("/", " "))
    texto = texto[1:]
    return texto.split("/")

mods = ("DE ", "DEL ", "LA ", "LOS ", "LAS ", "Y ", "MC ", "MAC ", "VON ",
        "VAN ")
comunes = ("JOSE ", "MARIA ", "J ", "MA ")
vocales = "AEIOUaeiou"
ans = "S"

_malas = "BUEIBUEYCACACACOCAGACAGOCAKACAKOCOGECOJAKOGEKOJOKAKAKULOMAMEMAMO"
_malas += "MEARMEASMEONMIONCOJECOJICOJOCULOFETOGUEYJOTOKACAKACOKAGAKAGOMOCO"
_malas += "MULAPEDAPEDOPENEPUTAPUTOQULORATARUINROBE"
evitar = [_malas[i:i + 4] for i in range(0, len(_malas), 4)]

# anex11 = list("00123456789&\ABCDEFGHIJKLMNOPQRSTUVWXYZ")
anex11 = list(" 0123456789&\ABCDEFGHIJKLMNOPQRSTUVWXYZÑ")
anex12 = ["00", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
          "10", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
          "21", "22", "23", "24", "25", "26", "27", "28", "29", "32", "33",
          "34", "35", "36", "37", "38", "39", "40"]
anex21 = ["00", "", "01", "", "02", "", "03", "", "04", "", "05", "", "06",
          "", "07", "", "08", "", "09", "", "10", "", "11", "", "12", "",
          "13", "", "14", "", "15", "", "16", "", "17", "", "18", "", "19",
          "", "20", "", "21", "", "22", "", "23", "", "24", "", "25", "",
          "26", "", "27", "", "28", "", "29", "", "30", "", "31", "", "32",
          "", "33"]
anex22 = ["1", "", "2", "", "3", "", "4", "", "5", "", "6", "", "7", "",
          "8", "", "9", "", "A", "", "B", "", "C", "", "D", "", "E", "",
          "F", "", "G", "", "H", "", "I", "", "J", "", "K", "", "L", "",
          "M", "", "N", "", "P", "", "Q", "", "R", "", "S", "", "T", "",
          "U", "", "V", "", "W", "", "X", "", "Y", "", "Z"]
anex31 = list("0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ*")
anex32 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
          "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
          "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
          "33", "34", "35", "36", "37"]

estados = [["AGUASCALIENTES", "AS"], ["MORELOS", "MS"],
           ["BAJA CALIFORNIA", "BC"], ["NAYARIT", "NT"],
           ["BAJA CALIFORNIA SUR", "BS"], ["NUEVO LEON", "NL"],
           ["CAMPECHE", "CC"], ["OAXACA", "OC"], ["COAHUILA", "CL"],
           ["PUEBLA", "PL"], ["COLIMA", "CM"], ["QUERETARO", "QT"],
           ["CHIAPAS", "CS"], ["QUINTANA ROO", "QR"], ["CHIHUHUA", "CH"],
           ["SAN LUIS POTOSI", "SP"], ["DISTRITO FEDERAL", "DF"],
           ["SINALOA", "SL"], ["DURANGO", "DG"], ["SONORA", "SR"],
           ["GUANAJUATO", "GT"], ["TABASCO", "TC"], ["GUERRERO", "GR"],
           ["TAMAULIPAS", "TS"], ["HIDALGO", "HG"], ["TLAXCALA", "TL"],
           ["JALISCO", "JC"], ["VERACRUZ", "VZ"], ["MEXICO", "MC"],
           ["YUCATAN", "YN"], ["MICHOACAN", "MN"], ["ZACATECAS", "ZS"],
           ["EXTRANJERO", "NE"]]

dEstados = {x[0]: x[1] for x in estados}
# wrongchars = "áéíóúÁÉÍÓÚüÜ"
# rightchars = "aeiouAEIOUuU"


if __name__ == '__main__':
    tx = mkRfc("González", "Fuentes", "Juan Francisco", "19580725")
    print(tx)
