# -*- coding: utf-8 -*-

import os
import filecmp

import soporte as Sp


def equal(a1, a2):
    """ Compara dos archivos, checando el contenido.

    :param a1: Primer archivo a comparar.
    :param a2: Segundo archivo.
    :returns: True si los archivos son iguales, False si no lo son.
    Los valores a1 y a2 son los registros que produce Sp.listFiles.
    """
    return filecmp.cmp(Sp.nomArchivo(a1), Sp.nomArchivo(a2),
            shallow=False)


def findDuplicados(listaDups):
    """ Obtiene los archivos duplicados en una lista.

    :param listaDups: Lista de archivos a comparar.
    :returns: Lista de archivos que tienen duplicados.
    Los elementos de la lista son registros generados por listFiles
    Al registro de cada duplicado se le agrega un entero que identifica
    los archivos que son iguales.
    """

    # Ordenar por tamaño.
    ds = []
    llave = 1
    listaDups.sort(key=lambda x: -x[3])
    sizes = list(set([x[3] for x in listaDups]))
    d = {sz: [x for x in listaDups if x[3] == sz] for sz in sizes}
    kis = list(d.keys())
    kis.sort(key=lambda x: -x)
    for k in kis:
        # print(k, end="/")
        if len(d[k]) > 1:
            tl = dsList(d[k])
            if len(tl):
                ds += [x + [llave] for x in tl]
                llave += 1
    return ds


def dsList(listaDups):
    """ Compara los archivos de una lista.

    :param lista: Lista de archivos a comparar.
    :returns: Lista de archivos duplicados.
    """

    ds = []
    while len(listaDups):
        a = listaDups[0]
        inds = []
        for i in range(1, len(listaDups)):
            if equal(a, listaDups[i]):
                inds.append(i)

        if len(inds):
            ds.append(a)
            ds += [listaDups[i] for i in inds]
            listaDups = [listaDups[i] for i in range(1, len(listaDups))
                     if i not in inds]
        else:
            listaDups = listaDups[1:]
    return ds


def getTag(dup):
    return dup[4]


def dupsRuta(ruta):
    """ Encuentra los archivos duplicados en una ruta.
    """
    return findDuplicados(Sp.listArchivos(ruta))


def dups2Rutas(ruta1, ruta2):
    """ Encuentra los archivos duplicados en dos rutas.
    """
    l = Sp.listArchivos(ruta1)
    for x in Sp.listArchivos(ruta2):
        if x not in l:
            l.append(x)
    return findDuplicados(l)


def compDirs(source, target):
    """ Regresa una lista de los archivos duplicados y los no duplicados.
    """
    ls = Sp.listArchivos(source)
    lt = Sp.listArchivos(target)
    lens0 = [len(ls), len(lt)]
    ds = [[], []]
    df = [[], []]
    lens = [0, 0, 0, 0]
    for x in ls:
        a = [x[0].replace(source, target)] + x[1:]
        if a in lt:
            if equal(x, a):
                ds[0].append(x)
                ds[1].append(a)
                lens[0] += 1
                lens[1] += 1
            else:
                df[0].append(x)
                df[1].append(x)
                lens[2] += 1
                lens[3] += 1
            # ls.remove(x)
            lt.remove(a)
        else:
            df[0].append(x)
            lens[2] += 1
    df[1] += lt
    lens[3] += len(lt)

    return lens0 + lens, ds, df


def dupsInRuta(ruta, listaDups):
    """ Encuentra en la lista de duplicados los que están en una ruta.
    """
    return [x for x in listaDups if chkDir(ruta, x)]


def dupsInside(ruta, listaDups):
    """ Encuentra los archivos dentro de la ruta con duplicado afuera.
    """
    marcas = list(set([getTag(x) for x in listaDups if not
                       chkDir(ruta, x)]))
    return [x for x in listaDups if getTag(x) in marcas and chkDir(ruta, x)]


def dupsOutside(ruta, listaDups):
    """ Encuentra los duplicados fuera de una ruta con dups dentro.
    """
    marcas = list(set([getTag(x) for x in listaDups if chkDir(ruta, x)]))
    return [x for x in listaDups if getTag(x) in marcas and not
            chkDir(ruta, x)]


def chkDir(ruta, archivo):
    """ Regresa True si el archivo x está en la ruta p.
    """
    return archivo[0].replace("\\", "/").startswith(ruta.replace("\\", "/"))


def selDups(archivo, listaDups):
    """ Regresa los duplicados del archivo en listaDups.
    """
    if archivo not in listaDups:
        return []
    else:
        l = [x for x in listaDups if getTag(x) == getTag(archivo)]
        return [x for x in l if x != archivo]


def borraLista(sels, listaDups):
    """ Elimina los archivos en sels.
    """
    for x in sels:
        ds = borraDuplicado(x, listaDups)
    return ds


def borraDuplicado(archivo, ds):
    """ Borra un archivo de la lista de duplicados, revisando la lista.
    """
    if archivo not in ds:
        return ds
    else:
        dm = selDups(archivo, ds)
        if len(dm) == 0:
            ds.remove(archivo)
        elif len(dm) > 0:
            # print("borrando", archivo)
            os.remove(Sp.nomArchivo(archivo))
            ds.remove(archivo)
            if len(dm) == 1:
                ds.remove(dm[0])
    return ds
