""" Funciones para calcular claves de indentifiación. Manejo de dígitos de
verificación. RFC, CURP, IMSS, etc.
"""


""" Cálculo del RFC, implantando directamente del documento encontrado en
línea.
"""


def reemplaza(texto, antes, despues):
    tx = texto
    for i in range(len(antes)):
        tx = tx.replace(antes[i], despues[i])
    return tx


def normaliza(texto):
    tx = texto.lower()
    tx = reemplaza(tx, "áéíóúü", "aeiouu")
    l = tx.upper().split()
    l = [x for x in l if x not in omitir]
    txt = " ".join(l)
    sal = ""
    for c in txt:
        if c in "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ ":
            sal += c
    return sal


def primeraVocal(tx):
    for c in tx:
        if c in "AEIOU":
            return c
    return ""


def dosLetras(texto):
    return texto[0] + primeraVocal(texto[1:])


def letrasPf(apellido1, apellido2, nombre):
    noms = list(map(normaliza, [apellido1, apellido2, nombre]))
    ns = noms[2].split()
    if len(ns) > 1:
        if ns[0] in ["JOSE", "MARIA"]:
            noms[2] = ns[1]
    if len(noms[0]) < 3:
        letras = noms[0][0] + noms[1][0] + noms[2][:2]
    elif not noms[1]:
        letras = noms[0][:2] + noms[2][:2]
    else:
        letras = dosLetras(noms[0]) + noms[1][0] + noms[2][0]

    if letras in malas:
        letras[3] = "X"
    return letras


""" Fecha: Se tomará la fecha en formato aammdd y se agregará a las letras.
"""


def fechaRfc(fecha):
    return fecha[2:]


def homonimia(apellido1, apellido2, nombre):
    noms = map(normaliza, [apellido1, apellido2, nombre])
    nom = " ".join(noms)
    s = "0" + "".join([chars[c] for c in nom])

    t = sum([int(s[i: i + 2]) * int(s[i + 1])
             for i in range(len(s) - 1)]) % 1000
    d = t // 34
    r = t % 34
    return hchrs[d] + hchrs[r]


def calcDv(rfc):
    l = [int(dvchrs[c]) for c in rfc]
    k = 13
    s = 0
    for x in l:
        s += k * x
        k -= 1
    r = s % 11
    r = 11 - r
    if r == 0:
        return "0"
    elif r == 10:
        return "A"
    else:
        return r


def calcRfc(apellido1, apellido2, nombre, fecha):
    r = letrasPf(apellido1, apellido2, nombre) \
        + fechaRfc(fecha) \
        + homonimia(apellido1, apellido2, nombre)
    r += str(calcDv(r))
    return r


malas = ["BUEI", "BUEY", "CACA", "CACO", "CAGA", "CAGO", "CAKA", "COGE",
         "COJA", "COJE", "COJI", "COJO", "CULO", "FETO", "GUEY", "JOTO",
         "KACA", "KACO", "KAGA", "KAGO", "KOGE", "KOJO", "KAKA", "KULO",
         "MAME", "MAMO", "MEAR", "MEON", "MION", "MOCO", "MULA", "PEDA",
         "PEDO", "PENE", "PUTA", "PUTO", "QULO", "RATA", "RUIN"]

chars = {" ": "00", "0": "00", "1": "01", "2": "02", "3": "03", "4": "04",
         "5": "05", "6": "06", "7": "07", "8": "08", "9": "09", "&": "10",
         "A": "11", "B": "12", "C": "13", "D": "14", "E": "15", "F": "16",
         "G": "17", "H": "18", "I": "19", "J": "21", "K": "22", "L": "23",
         "M": "24", "N": "25", "O": "26", "P": "27", "Q": "28", "R": "29",
         "S": "32", "T": "33", "U": "34", "V": "35", "W": "36", "X": "37",
         "Y": "38", "Z": "39", "Ñ": "40"}

hchrs = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8",
         8: "9", 9: "A", 10: "B", 11: "C", 12: "D", 13: "E", 14: "F",
         15: "G", 16: "H", 17: "I", 18: "J", 19: "K", 20: "L", 21: "M",
         22: "N", 23: "P", 24: "Q", 25: "R", 26: "S", 27: "T", 28: "U",
         29: "V", 30: "W", 31: "X", 32: "Y", 33: "Z"}

dvchrs = {"0": "00", "1": "01", "2": "02", "3": "03", "4": "04", "5": "05",
          "6": "06", "7": "07", "8": "08", "9": "09", "A": "10", "B": "11",
          "C": "12", "D": "13", "E": "14", "F": "15", "G": "16", "H": "17",
          "I": "18", "J": "19", "K": "20", "L": "21", "M": "22", "N": "23",
          "&": "24", "O": "25", "P": "26", "Q": "27", "R": "28", "S": "29",
          "T": "30", "U": "31", "V": "32", "W": "33", "X": "34", "Y": "35",
          "Z": "36", " ": "37", "Ñ": "38"}

omitir = ["DEL", "DE", "LAS", "LA", "MC", "VON", "LOS", "Y", "MAC",
          "VAN", "MI"]
