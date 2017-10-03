# -*- coding: utf-8 -*-

# import os
import time


def primero(n):
    if n == 1:
        return "°"
    else:
        return ""


def getYear(fe):
    """ Regresa el año de la fecha dada, a partir de 1900."""
    if len(fe) < 8:
        return 0
    else:
        ye = int(fe[:4])
        if ye >= 1900:
            return ye
        else:
            return ""


def getMonth(fe):
    """ Regresa elmes de la fecha dada,validando"""
    if len(fe) < 8:
        return 0
    mo = int(fe[4:6])
    if mo < 13 and mo > 0:
        return mo
    else:
        return ""


def getDay(fe):
    """ Regresa el día de la fecha dada, validando."""
    if len(fe) < 8:
        return 0
    ye = getYear(fe)
    mo = getMonth(fe)
    if mo == "" or ye == "":
        return ""
    else:
        da = int(fe[6:])
        if da > 0 and da <= 28:
            return da
        elif mo != 2 and da <= 30:
            return da
        elif mo in [1, 3, 5, 7, 8, 10, 12] and da == 31:
            return da
        elif mo == 2 and da == 29 and isLeap(ye):
            return da
        else:
            return ""


def getWeekDay(fe):
    """Regresa el día de la semana. Domingo = 0
    """
    return fe2int(fe) % 7


def getDayName(fe):
    """Regresa el nombre en español del día de la semana.
    """
    return dias[fe2int(fe) % 7]


def isLeap(ye):
    """ Regresa True si el año es bisiesto."""
    return (ye % 400 == 0 or (ye % 4 == 0 and ye % 100 != 0))


def mkFecha(a, m, d):
    """" Toma enteros para año, mes y día y regresa la fecha."""
    tx = str(a).rjust(4, "0") + str(m).rjust(2, "0") + str(d).rjust(2, "0")
    if getDay(tx) != "":
        return tx
    else:
        return ""


def daysMonth(a, m):
    """Regresa cuántos días tuvo un mes en un año dado."""
    if m in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif m in [4, 6, 9, 11]:
        return 30
    elif m == 2:
        if isLeap(a):
            return 29
        else:
            return 28


def fe2int(fe):
    """ Calcula los días hasta una fecha a partir de 01/01/1900"""
    ye = getYear(fe)
    mo = getMonth(fe)
    da = getDay(fe)
    if da == "":
        return ""
    else:
        c = 0
        for i in range(1900, ye):
            if isLeap(i):
                c += 366
            else:
                c += 365
        for i in range(mo-1):
            c += daysMonth(ye, i+1)
        return c + da


def int2fe(i):
    """ Convierte un número de días en fecha a partir de 01/01/1900"""
    y = 1900
    while i > 0:
        if isLeap(y):
            i -= 366
        else:
            i -= 365
        y += 1
    y = y - 1
    if isLeap(y):
        i += 366
    else:
        i += 365
    m = 1
    while i > 0:
        i -= daysMonth(y, m)
        m += 1
    m = m-1
    i += daysMonth(y, m)
    return mkFecha(y, m, i)


def sumFecha(fecha, dias):
    """ Calcula la fecha un número de días después de la fecha dada."""
    return int2fe(fe2int(fecha) + dias)


def difFechas(f1, f2):
    """ Calcula los días entre dos fechas"""
    return fe2int(f2) - fe2int(f1)


def intFechas(f1, f2, f3, f4):
    """ Dados dos períodos f1 a f2, f3 a f4, regresa los días en ambos"""
    fechas = [max(f1, f3), min(f2, f4)]
    if fechas[0] > fechas[1]:
        return ['', '']
    else:
        return fechas


def intPeriodos(p, q):
    """ Dados dos pares de fechas regresa los días en ambos intervalos"""
    return intFechas(p[0], p[1], q[0], q[1])


def difYears(f1, f2):
    """ Regresa el número de años completos entre dos fechas?"""
    f3 = mkFecha(getYear(f2), getMonth(f1), getDay(f2))
    years = getYear(f2) - getYear(f1)
    if f3 > f2:
        years -= 1
    return years


def fechasMes(y, m):
    """ Devuelve el principio y fin de un mes en un año dado."""
    return [mkFecha(y, m, 1), mkFecha(y, m, daysMonth(y, m))]


def fechasBim(y, m):
    if m % 2 == 0:
        m1 = m-1
        m2 = m
    else:
        m1 = m
        m2 = m+1
    return [mkFecha(y, m, 1), mkFecha(y, m, daysMonth(y, m)),
            mkFecha(y, m1, 1), mkFecha(y, m2, daysMonth(y, m2))]


def valFecha(f):
    return not (getDay(f) == "" or getMonth(f) == "" or getYear(f) == "")


def dispFecha(f, fmt=0):
    if not valFecha or fmt not in [0, 1, 2, 3]:
        return ""

    if fmt == 0:
        return "%d/%d/%d" % (getDay(f), getMonth(f), getYear(f))
    elif fmt == 1:
        return "%d/%s/%d" % (getDay(f), nombres[getMonth(f) - 1][:3],
                             getYear(f))
    elif fmt == 2:
        return "%d/%s/%d" % (getDay(f), nombres[getMonth(f) - 1], getYear(f))
    elif fmt == 3:
        return "%d%s de %s de %d" % (getDay(f), primero(getMonth(f)),
                                     nombres[getMonth(f) - 1], getYear(f))


def hoy():
    c = time.ctime().split()
    return c[4] + mesesE[c[1].lower()] + c[2].rjust(2, "0")


def previousDay(fecha, dia):
    """ Regresa el último dia de la semana igual a dia, incluyendo fecha.
    """
    f = sumFecha(fecha, dia - getWeekDay(fecha))
    if f > fecha:
        f = sumFecha(f, -7)
    return f


def existeDia(f1, f2, dia):
    """ Checa si el dia dado existe en el período. Asume f1<=f2.
    """
    f = f1
    while f <= f2:
        if getWeekDay(f) == dia:
            return True
        f = sumFecha(f, 1)
    return False


def testFechas():
    f1 = "19000301"
    f2 = "19580725"
    f3 = hoy()
    print("Fechas:", f1, f2, f3)
    print("Números:", fe2int(f1), fe2int(f2), fe2int(f3))
    print("Sanity:", int2fe(fe2int(f1)), int2fe(fe2int(f2)),
          int2fe(fe2int(f3)))
    print("Meses y días:", getMonth(f1), daysMonth(getYear(f1), getMonth(f1)),
          getMonth(f2), daysMonth(getYear(f2), getMonth(f2)),
          getMonth(f3), daysMonth(getYear(f3), getMonth(f3)))


meses = {"ene": "01", "feb": "02", "mar": "03", "abr": "04", "may": "05",
         "jun": "06", "jul": "07", "ago": "08", "sep": "09", "oct": "10",
         "nov": "11", "dic": "12"}
mesesE = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05",
         "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10",
         "nov": "11", "dec": "12"}
nombres = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre")
dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes",
        "Sábado"]

if __name__ == '__main__':
    testFechas()
