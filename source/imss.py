# -*- coding: utf-8 -*-

# import os

import soporte as Sp
import zipfile as Zf


# ---------------------------------------------------------------------------
# Funciones de SUA
# ---------------------------------------------------------------------------


def mkHeader(texto):
    """ Separa una línea de texto en longitudes específicas.

    :param texto: Texto a procesar. Se llama con la primera línea (virtual)
                  de un archivo sua.
    """
    lns = (2, 11, 13, 4, 2, 6, 50, 102, 7, 50, 1, 13, 7)
    return Sp.splitLens(texto, lns)


def mkCuotas(datos):
    """ Analiza las líneas de tipo 2 de un archivo sua.

    :param datos: Lista de líneas de texto.

    Se llama con las líneas virtuales del archivo sua que empiezan con "02.
    """

    lns = (26, 4, 2, 11, 13, 18, 10, 8, 2, 50, 7, 2, 2, 2, 2, 7, 7, 7, 7, 7,
           7, 7, 7, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7)
    l = [Sp.splitLens(x, lns) for x in datos]
    l = [mkCuotasTrab(x) for x in l]
    d = {}
    for x in l:
        d[x["afil"]] = x
    return d


def mkCuotasTrab(l):
    """ Convierte una línea de cuotas en un diccionario.

    :param l: lista de valores de cuotas.
    :returns: diccionario con los datos de este renglón de cuotas.

    Se llama con las listas generadas por mkCuotas.
    """

    dat = Sp.list2dict(l, ("afil", "nombre", "rfc", "cred", "sbc", "dias",
                                "inc", "aus", "diasb", "incb", "ausb"),
                            (3, 9, 4, 6, 10, 12, 13, 14, 23, 24, 25))
    dat["sbc"] = int(dat["sbc"]) / 100.0
    mensual = {}
    mensual["cf"] = int(l[15]) / 100.0
    mensual["exc"] = int(l[16]) / 100.0
    mensual["pd"] = int(l[17]) / 100.0
    mensual["gmp"] = int(l[18]) / 100.0
    mensual["rt"] = int(l[19]) / 100.0
    mensual["iv"] = int(l[20]) / 100.0
    mensual["gps"] = int(l[21]) / 100.0
    mensual["ayr"] = int(l[22]) / 100.0
    mensual["subt"] = (mensual["cf"] + mensual["exc"] + mensual["pd"] +
                       mensual["gmp"] + mensual["rt"] + mensual["iv"] +
                       mensual["gps"])
    mensual["total"] = mensual["subt"] + mensual["ayr"]

    rcv = {}
    rcv["retiro"] = int(l[26]) / 100.0
    rcv["cyv"] = (int(l[28]) + int(l[29])) / 100.0
    rcv["ayr"] = (int(l[27]) + int(l[30])) / 100.0
    rcv["subt"] = rcv["retiro"] + rcv["cyv"]
    rcv["total"] = rcv["subt"] + rcv["ayr"]

    infonavit = {}
    infonavit["aport"] = int(l[32]) / 100.0
    infonavit["amort"] = int(l[33]) / 100.0
    infonavit["total"] = infonavit["aport"] + infonavit["amort"]

    dat["mensual"] = mensual
    dat["rcv"] = rcv
    dat["infonavit"] = infonavit
    dat["subt"] = mensual["subt"] + rcv["subt"] + infonavit["total"]
    dat["ayr"] = mensual["ayr"] + rcv["ayr"]
    dat["total"] = mensual["total"] + rcv["total"] + infonavit["total"]

    return dat


def mkTotales(texto):
    """ Obtiene los totales de un archivo sua.

    :param texto: Línea de texto tipo 4 de un archivo sua.
    """
    lns = (58, 9, 9, 9, 9, 9, 9, 9, 11, 9, 9, 9, 9, 11, 9, 9, 11, 9, 9,
           9, 9, 9)
    l = Sp.splitLens(texto, lns)
    l = [l[0]] + [int(x) / 100.0 for x in l[1:]]
    mensual = Sp.list2dict(l,
                                ("cf", "exc", "pd", "gmp", "rt", "iv",
                                 "gps", "subt", "act", "rec"),
                                (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    mensual["total"] = sum(l[1:11]) - l[8]
    rcv = Sp.list2dict(l,
                            ("retiro", "cyv", "subt", "act", "rec"),
                            (11, 12, 13, 14, 15))
    rcv["total"] = sum(l[14:16]) + rcv["subt"]
    infonavit = Sp.list2dict(l,
                                  ("sin", "con", "amort", "act", "rec"),
                                  (17, 18, 19, 20, 21))
    infonavit["subt"] = sum(l[17:20])
    infonavit["total"] = sum(l[17:22])
    d = {}
    d["total"] = mensual["total"] + rcv["total"] + infonavit["total"]
    d["mensual"] = mensual
    d["rcv"] = rcv
    d["infonavit"] = infonavit
    return d


def mkMovs(datos):
    """ Procesa las línesa tipo 3 de un archivo sua.

    :param datos: Lista de líneas de texto.
    :returns: Lista de movimientos.
    La longitud de un campo de movimientos es 38.
    """
    lnRec = 38
    lns = (11, 2, 8, 8, 2, 7)
    mvs = [x[13:].strip() for x in datos]
    movs = []
    for x in mvs:
        l = Sp.splitEqual(x, lnRec)
        movs += [Sp.splitLens(r, lns) for r in l]
    return movs


def leePagoSua(archivo):
    """ Lee un archivo SUA y regresa un diccionario con los datos.


    Las llaves son: rp,ej,totales,rfc,mes,prima,raz,movs,cuotas
    El contenido es:

    rp
      registro patronal

    ej
      ejercicio

    mes
      mes

    raz
      razón social

    prima
      Prima de riesgo

    rfc
      rfc!

    totales
      Diccionario de diccionarios con los totales del archivo. Las llaves son
      las siguientes y se explican solas.

      mensual
        Con las llaves: cf, exc, pd, gmp, iv, rt, gps, subt, act, rec, total

      rcv
        Con las llaves: retiro, cyv, subt, act, rec, total

      infonavit
        Con las llaves: sin, con, amort, subt, act, rec, total

      total
        Importe total.
    """
    lnRec = 295
    texto = Sp.leerTexto(archivo)
    sua = Sp.splitEqual(texto, lnRec)
    h = mkHeader(sua[0])
    cts = mkCuotas([x for x in sua if x[:2] == "03"])
    tots = mkTotales([x for x in sua if x[:2] == "05"][0])
    mvs = mkMovs([x for x in sua if x[:2] == "04"])
    d = {}
    d["archivo"] = archivo.replace('\\', '/')
    d["rp"] = h[1]
    d["rfc"] = h[2]
    d["ej"] = h[3]
    d["mes"] = h[4]
    d["raz"] = h[6]
    d["prima"] = h[8]
    d["totales"] = tots
    d["cuotas"] = cts
    d["movs"] = mvs
    return d


def detallePago2(pago):
    c = pago["cuotas"]
    l = []
    for afil in c.keys():
        ct = c[afil]
        cm = ct["mensual"]
        info = ct["infonavit"]
        rcv = ct["rcv"]
        l.append([afil, ct["nombre"].strip(),
                  str(ct["dias"]), str(ct["inc"]), str(ct["aus"]),
                  str(ct["sbc"]), str(cm["cf"]), str(cm["exc"]),
                  str(cm["pd"]), str(cm["gmp"]), str(cm["rt"]),
                  str(cm["iv"]), str(cm["gps"]), str(ct["diasb"]),
                  str(ct["incb"]), str(ct["ausb"]),
                  str(rcv["retiro"]), str(rcv["cyv"]),
                  str(info["aport"]), str(info["amort"])])
    return l


def detallePago(pago):
    """ Regresa una lista de los renglones de cuotas, separados en campos.

    :param pago: Diccionario obtenido con leePagoSua
    :returns: Lista de cuotas.
    """
    c = pago["cuotas"]
    l = []
    for afil in c.keys():
        ct = c[afil]
        info = ct["infonavit"]
        rcv = ct["rcv"]
        l.append([pago["rp"], afil, ct["nombre"].strip(),
                  str(ct["dias"]), str(ct["inc"]), str(ct["aus"]),
                  str(ct["sbc"]), str(ct["mensual"]["subt"]),
                  str(ct["mensual"]["gps"]), str(ct["diasb"]),
                  str(ct["incb"]), str(ct["ausb"]), str(rcv["retiro"]),
                  str(rcv["cyv"]), str(rcv["subt"]), str(info["aport"]),
                  str(info["amort"]), str(info["total"])])
    return l


def readSuas(ruta):
    """ Lee los archivos sua de una ruta.

    :param ruta: Ruta que contiene los archivos de pago.
    :returns: lista de diccionarios de pago.
    """
    archivos = [x for x in Sp.listFiles(ruta)
                if x[1].upper().endswith(".SUA")]
    suas = [leePagoSua(Sp.nomArchivo(x)) for x in archivos]
    suas.sort(key=lambda x: x["rp"])
    return suas


def resumenSua(s):
    """ Obtiene totales de un pago. Para despliegue.

    :param s: Diccionario de pago.
    :returns: Lista con datos del pago.

    Contiene:

    + registro patronal
    + año y mes
    + subtotal mensual
    + subtotal rcv
    + subtotal aportaciones
    + subtotal infonavit
    + total de actualización y recargos
    + total general
    + ruta y nombre del archivo.
    """
    l = [s["rp"],
         s["ej"] + s["mes"],
         s["totales"]["mensual"]["subt"],
         s["totales"]["rcv"]["subt"],
         s["totales"]["infonavit"]["con"] + s["totales"]["infonavit"]["sin"],
         s["totales"]["infonavit"]["amort"],
         (s["totales"]["mensual"]["act"] + s["totales"]["rcv"]["act"] +
          s["totales"]["infonavit"]["act"] + s["totales"]["mensual"]["rec"] +
          s["totales"]["rcv"]["rec"] + s["totales"]["infonavit"]["rec"]),
         s["totales"]["total"],
         s["archivo"]]
    return l


def textoSua(s, archivo=0):
    """ Resumen de Sua en texto.

    :param s: Diccionario de pago.
    :param archivo: Decide si se agrega el archivo. Default es no.
    :returns: Texto formateado con el resumen del pago.
    """
    l = resumenSua(s)
    if archivo:
        ar = l[8]
    else:
        ar = ""
    tx = ("{}   {}   {:>15,.2f}    {:>15,.2f}   {:>15,.2f}   {:>15,.2f}   "
          "{:>15,.2f}   {:>15,.2f}")
    return tx.format(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7]) + ar


def leeEmision(archivo):
    """ Obtiene los datos de una emisión en formato visor, comprimida.
    """
    nm = Sp.nomArchivo(archivo)
    zf = Zf.ZipFile(nm)
    tots = zf.read("CDCOBRA/Tempo/CDEMPA99.txt")
    dats = zf.read("CDCOBRA/Tempo/CDEMMO99.txt").decode("utf-i").split("/n")
    dats = [x.strip() for x in dats]
    return totalEmision(tots), movsEmision(dats)


def totalEmision(texto):
    rp = texto[23:34]
    ms = texto[95:97]
    año = texto[97:101]
    ss = texto[120:252]
    imss = sum([int(x) for x in Sp.splitEqual(ss, 12, True)]) / 100.0
    return [rp, ms, año, imss]


def movsEmision(datos):
    return [mkMovImss(x) for x in datos]


def mkMovImss(mov):
    rp = mov[:11]
    fe = mov[36:46]
    dias = mov[46:48]
    sbc = mov[48:54]
    ss = mov[54:]
    imss = [int(x) / 100 for x in Sp.splitEqual(ss, 8, True)]
    total = sum(imss)
    return [rp, fe, dias, sbc, total] + imss


if __name__ == '__main__':
    suas = [x for x in Sp.listFiles(
        "c:/despacho/imss2015/archivo/pagados")
        if x[1].upper().endswith(".SUA")]

    print(len(suas), "suas")
    for x in suas:
        p = leePagoSua(Sp.nomArchivo(x))
        print(resumenSua(p))
