# -*- coding: utf-8 -*-

import os
import soporte as Sp


def prsBteRespHdr(txt):
    return Sp.subLista(Sp.splitLens(txt, (1, 5, 40, 2, 6, 95)),
                       (1, 2, 3, 4))


def prsBteRespDet(txt):
    lens = (1, 10, 20, 20, 20, 5, 13, 2, 1, 16, 4, 3, 2, 18, 4, 2, 8)
    rec = Sp.subLista(Sp.splitLens(txt, lens),
                      (1, 2, 3, 4, 5, 6, 7, 9, 13, 15))
    rec[0] = str(int(rec[0]))
    rec[1:4] = list(map(lambda x: x.strip(), rec[1:4]))
    rec[8] = rec[8][-10:]
    rec[4] = str(int(rec[4]))
    return rec


def prsBteEnvioHdr(txt):
    return Sp.subLista(Sp.splitLens(txt, (1, 2, 8, 5, 40, 2, 6)),
                       (3, 4, 5, 6))


def prsBteEnvioDet(txt):
    lens = (1, 10, 20, 20, 20, 5, 2, 19, 2, 24, 7, 2, 2, 2, 4, 40, 3,
            2, 5, 12, 1, 8, 3, 1, 1, 3, 3, 2, 13, 18, 2, 1, 16, 4, 3,
            2, 18, 4, 1, 15, 16, 10)
    rec = Sp.subLista(Sp.splitLens(txt, lens),
                      (1, 2, 3, 4, 5, 28, 29, 32, 30))
    rec[0] = str(int(rec[0]))
    rec[1:4] = list(map(lambda x: x.strip(), rec[1:4]))
    rec[4] = str(int(rec[4]))
    return rec


if __name__ == '__main__':
    os.chdir("c:/despacho/tarjetas")
    ruta = "movs/0901"
    archivos = Sp.listArchivos(ruta)
    archivos = [x for x in archivos if x[1].upper().endswith(".ALT")]
    d = {}
    for a in archivos:
        tx = Sp.leerLista(Sp.nomArchivo(a), code="latin-1")
        emisora = prsBteEnvioHdr(tx[0])[0]
        if emisora not in d.keys():
            d[emisora] = []
        for x in tx[1:]:
            d[emisora].append(prsBteEnvioDet(x))
    envios = []
    for k in d.keys():
        for x in d[k]:
            envios.append([k] + x)

    recibos = Sp.listArchivos("dls", recurse=0)
    dRecibos = {}
    for a in recibos:
        datos = Sp.leerLista(Sp.nomArchivo(a))
        fecha = a[1][10:14] + a[1][8:10] + a[1][6:8]
        emisrec = prsBteRespHdr(datos[0])[0]
        if emisrec not in dRecibos.keys():
            dRecibos[emisrec] = []
        for x in datos[1:]:
            dRecibos[emisrec].append([fecha] + prsBteRespDet(x))
    respuestas = []
    for k in d.keys():
        for x in dRecibos[k]:
            respuestas.append([k] + x)
    print(len(envios), "envíos", len(respuestas), "respuestas")
    errs = list(set([x[-1] for x in respuestas if x[-1] != "00"]))
    print("Errores:", errs)
    for e in errs:
        le = [x for x in respuestas if x[-1] == e]
        for m in le:
            lr = [x for x in envios if x[1] == m[2]]
            print("Error:", e, m)
            Sp.listList(lr)
        print("")
