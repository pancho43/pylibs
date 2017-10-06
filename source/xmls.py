# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

import soporte as Sp


def pruneTag(e):
    """ Elimina la dirección web que precede algunos tags.

    No estoy seguro de sus efectos fuera del contexto actual.
    En otras palabras, no sé la función de dicha dirección web.
    """
    return e.tag.split("}")[1]


def imprimeXml(archivo, full=1):
    """ Imprime el árbol completo dado el nombre de archivo.

    :param archivo: Nombre del archivo xml a imprimir.
    :param full: Abreviado o completo.
    """
    t = getXml(Sp.nomArchivo(archivo))
    printXml(t, full)


def printXml(arbol, full=1):
    """ Imprime el árbol.

    :param arbol: un árbol generado pro xmls.getXml
    :param full: indica impresión completa o abreviada.
    """
    if full == 0:
        print("\n".join(listXml(arbol)))
    else:
        print("\n".join(listXmlFull(arbol)))


def listXml(root, l=[], inicio=""):
    """ Construye una lista de las tags en el archivo.

    La lista incluye tabs a la izquierda para que al imprimir muestre
    la subordinación de los tags.
    """
    l.append(inicio + pruneTag(root))
    inicio += "\t"
    for c in root.getchildren():
        l += listXml(c, [], inicio)
    return l


def listXmlFull(root, inicio=""):
    """ Construye una lista de tags y su contenido.

    Incluye formateo para impresión.
    """
    l = []
    l.append(inicio + pruneTag(root))
    for k in root.attrib.keys():
        l.append(inicio + "." + k + ":   " + root.attrib[k][:50])
    inicio += "\t"
    for c in root.getchildren():
        l += listXmlFull(c, inicio)
    return l


def getXmlFull(arbol):
    """ Fallido. No lee listas de tags iguales.
    """
    d = {}
    k1 = pruneTag(arbol)
    d[k1] = [arbol.attrib, {}]
    for st in arbol.getchildren():
        k2 = pruneTag(st)
        d[k1][1][k2] = getXmlFull(st)[k2]
    return d


def getXml(archivo):
    """ Regresa el contenido del archivo en formato de ElementTree.
    """
    try:
        tree = ET.parse(archivo)
        return tree.getroot()
    except:
        return ""


def getElem(et, nombre):
    try:
        return [x for x in et.iter() if x.tag.endswith(nombre)]
    except:
        return ""


def leeAtributo(arbol, elemento, atributo):
    """ Regresa el valor del atributo dado en el elemento dado.

    :param arbol: Arbol generado por getXml (ElementTree)
    :param elemento: Tag del elemento buscado.
    :param atributo: atributo cuyo valor se busca.
    :returns: Valor del atributo en el elemento dado.
    Si hay más de un elemento con el mismo nombre, regresa el valor
    correspondiente al primero que tenga el atributo.
    Si no existe el atributo regresa "".
    """
    if pruneTag(arbol) == elemento:
        if atributo in arbol.attrib.keys():
            return arbol.attrib[atributo]
    for child in arbol.getchildren():
        r = leeAtributo(child, elemento, atributo)
        if r:
            return r
    return ""


def buscaAtributo(arbol, atributo):
    """ Regresa el valor del atributo en el árbol dado.

    :param arbol: Arbol generado por getXml
    :param atributo: Atributo que se busca.
    :returns: Valor del atributo en el primer elemento que lo tenga.
    Regresa "" si no encuentra el atributo.
    """
    if isinstance(arbol, str):
        return ""
    if atributo in arbol.attrib.keys():
        return arbol.attrib[atributo]
    for child in arbol.getchildren():
        r = buscaAtributo(child, atributo)
        if r:
            return r
    return ""


def buscaElemento(arbol, atributo, valor="", elemento=""):
    """ Buscar el elemento con el atributo y valor dados.

    :param arbol: Element a procesar.
    :param atributo: Nombre del atribuo buscado.
    :param valor: El valor del atributo que se busca.
    :param elemento: Nombre del elemento a buscar.
    :returns: Sub-árbol que contiene el atributo.
    Si valor=="" regresa el primer elemento con el atributo. Si tiene
    un valor regresa el elemento con ese valor.
    Si elemento=="" regresa cualquier elemento con el atributo.
    """

    def conElem():
        l = getElem(arbol, elemento)
        l = [x for x in l if atributo in x.attrib.keys()]
        if valor:
            l = [x for x in l if x.attrib[atributo] == valor]
        if l:
            return l[0]
        else:
            return ""

    def sinElem():
        l = [x for x in arbol.iter() if atributo in x.attrib.keys()]
        if valor:
            l = [x for x in l if x.attrib[atributo] == valor]
        return l[0]

    if elemento:
        return conElem()
    else:
        return sinElem()


# --------------------------------------------------------------
# Nueva interfaz
# ------------------------------------------------------------------------
def convTree(root):
    """ Convierte un árbol de CFDI en un diccionario para acceso standard.

    :param root: árbol a procesar.
    :returns: diccionario con los tag del árbol como llaves y los subárboles
    y atributos como subdiccionarios.
    """
    d = {}
    tag = pruneTag(root)
    d[tag] = buildDict(root)
    return d


def buildDict(tree):
    """ Recursivamente lee subárboles y los convierte en diccionarios anidados.

    :param tree: árbol o sub-árbol a procesar.
    :returns: diccionario.
    Cada par atributo:valor se convierte en un elemento llave:valor en el
    diccionario. Cada subárbol se convierte en un nuevo sub-diccionario
    con el tag como llave.
    Para llaves que se repiten se crea un diccionario con llaves "tipo" y
    "valores", con tipo = "1" y valores una lista de diccionarios.
    """
    d = {}
    for a in tree.attrib.keys():
        d[a] = tree.attrib[a]
    for c in tree.getchildren():
        tg = pruneTag(c)
        if tg in d.keys():
            d1 = d[tg]
            if d[tg].get("tipo", "") == "l":
                d[tg]["valores"].append(buildDict(c))
            else:
                rec = buildDict(c)
                d[tg] = {"tipo": "l", "valores": [d1, rec]}
        else:
            d[pruneTag(c)] = buildDict(c)
    return d


def evaluate(d, kis):
    """ Obtiene el valor detrás de una lista de llaves, en el diccionario.

    :param d: diccionario obtenido de un XML.
    :param kis: lista, cada elemento es una llave. La primera es una llave
    de d, y las siguientes lo son de los subdiccionarios respectivos.
    """
    if not kis:
        return d
    else:
        return evaluate(d[kis[0]], kis[1:])


if __name__ == '__main__':
    pass
