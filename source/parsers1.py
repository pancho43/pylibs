# -*- coding: utf-8 -*-

import support as Sp
import zipfile as Zp


def splitAseg(archivo):
    """ Analiza la información del archivo de asegurados de la emisión del IMSS

    :param archivo: Nombre del archivo zip que contiene la emisión.
    :returns: Lista de registros con campos significativos obtenidos del
              archivo.
    La emisión a procesar debe ser formato visor, mensual. Presupone la
    estructura interna que actualmente está en uso: carpetas CDCOBRA/Tempo
    y archivos CDEMAS99.txt, CDEMMO99.txt, CDEMPA99.txt que indican asegurados,
    movimientos y patrones, respectivamente.
    Esta función se ocupa del archivo CDEMAS99.txt. Se harán funciones
    específicas para los otros archivos y para la emisión bimestral.
    """
    nm = "CDCOBRA/Tempo/CDEMAS99.txt"
    zf = Zp.ZipFile(archivo)
    entrada = zf.read(nm).decode(encoding="utf-8").split("\n")
    salida = [list(map(lambda x: x.strip(),
                       Sp.subLista(
                           Sp.splitLens(txt,
                                        (11, 3, 8, 1, 11, 1, 50, 3, 18, 3)),
                           (0, 4, 6, 8)))) for txt in entrada]
    return [x for x in salida if x[0]]


def splitAsegBim(archivo):
    """ Analiza la información del archivo de asegurados de emisión bimestral.

    :param archivo: Nombre del archivo zipo que contiene la emisión.
    :returns: Lista de registros obtenidos del archivo.
    """
    nm = "CDCOBRA/Tempo/CDEBAS99.txt"
    zf = Zp.ZipFile(archivo)
    entrada = zf.read(nm).decode(encoding="utf-8").split("\n")
    salida = [list(map(
        lambda x: x.strip(),
        Sp.subLista(
            Sp.splitLens(
                txt,
                (11, 3, 6, 1, 11, 1,  50, 3, 18, 3, 2, 10, 1, 9, 8, 13)),
            (0, 4, 6, 8, 11, 12, 13, 14, 15)))) for txt in entrada]
    return [x for x in salida if x[0]]


def leerCreditos(archivo):
    """ Obtiene los registros con crédito Infonavit de una emisión bimestral.

    :param archivo: Archivo zip a leer.
    :return: Lista de registros con crédito.
    """
    recs = splitAsegBim(archivo)
    return [x for x in recs if int(x[4]) > 0]
