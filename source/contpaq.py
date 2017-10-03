# -*- coding: utf-8 -*-

# import os

import soporte as sp

def ajustar(texto, ancho, filler=" "):
    """ Regresa texto ajustado a ancho, truncando a agregando filler."""
    if len(texto) > ancho:
        return texto[:ancho]
    else:
        return texto.ljust(ancho, filler)


def cents2text(cents):
    """ Regresa el importe dado formateado con dos decimales."""
    tx = str(cents)
    while len(tx) < 3:
        tx = "0" + tx
    return tx[:-2] + "." + tx[-2:]


def mkPoliza(fecha, tipo, folio, concepto, movs):
    """Regresa el texto de una póliza en formato de contpaq.

    fecha debe estar en fomrato aaaammdd.
    tipo es: 1=ingresos, 2=egresos, 3=diario.
    folio es un número > 1.
    movs es una lista de (cuenta, ref, tipo, importe, concepto).
    importe es un valor entero en centavos.
    """
    if not len(movs):
        print("Error en creación de póliza: no hay movimientos", fecha, folio,
              tipo, concepto)
        return ""
    l = [mkHeader(fecha, folio, tipo, concepto)]
    l += [mkMov(*x) for x in movs]
    return '\n'.join(l)


def mkPolizaCfdi(fecha, tipo, folio, concepto, uids, movs):
    """ Regresa el texto de una póliza con cfdis asociados.
    """
    if not len(movs):
        print("Error en creación de póliza: no hay movimientos", fecha, folio,
              tipo, concepto)
        return ""
    l = [mkHeader(fecha, folio, tipo, concepto)]
    for x in uids:
        l.append("AD " + x)
    l += [mkMov(*x) for x in movs]
    return '\n'.join(l)


def mkHeader(fecha, folio, tipo, concepto):
    """Regresa el texto del registro de póliza del formato contpaq."""
    rec = ("P ", fecha, tipo.rjust(4), str(folio).rjust(9), "1",
           "0" + " " * 9, ajustar(concepto, 100), "11", "0", "0 ")
    return " ".join(rec)


def mkMov(cuenta, ref, tipo, importe, concepto):
    """Regresa el texto de un movmiento de póliza en formato contpaq."""
    # print("cq.mkMov",(cuenta,ref,tipo,importe,concepto))
    rec = ("M ", cuenta.ljust(30), ref.ljust(10), tipo,
           cents2text(importe).rjust(20), "0".ljust(10),
           "0.0".ljust(20), ajustar(concepto, 100), " " * 5)
    return " ".join(rec)


def mkCobro(c_bco, c_ing, c_iva, fecha, importe):
    total = int(100 * round(importe, 2))
    ingresos = int(round(total / 1.16, 0))
    iva = total - ingresos
    movs = ((c_bco, "", '0', total, ""),
            (c_ing, "", '1', ingresos, ""),
            (c_iva, "", '1', iva, ""))
    return (fecha, '1', 1, "Pago de factura", movs)


def main():
    """ Principalmente para ejemplificar proceso a seguir.
    """
    cobros = sp.leerDatos("cobros.dat")
    pols = [mkCobro(*x) for x in cobros]

    tx = "\n".join([mkPoliza(*x) for x in pols])
    open("polizas.txt", "w", encoding="latin-1").write(tx)


if __name__ == '__main__':
    main()
