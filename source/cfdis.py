# -*- coding: utf-8 -*-

# import soporte as Sp
import xmls as Xm


# Accesors.
# Escribir funciones de acceso para todos los campos conocidos.
# ---------------------------------------------------------------------

def readTipo(tree):
    return tree.attrib["tipoDeComprobante"]


def readMoneda(tree):
    return tree.attrib.get("Moneda", "")


def readFechayHora(tree):
    return tree.attrib["fecha"].split("T")


def readFecha(tree):
    return readFechayHora(tree)[0]


def readHora(tree):
    return readFechayHora(tree)[1]


def readFolio(tree):
    try:
        return tree.attrib["folio"]
    except:
        return ""


def readSerie(tree):
    try:
        return tree.attrib["serie"]
    except:
        return ""


def readFolioFiscal(tree):
    return Xm.buscaAtributo(tree, "UUID")


def readSubtotal(tree):
    return tree.attrib["subTotal"]


def readTotal(tree):
    return tree.attrib["total"]


def readTC(tree):
    # return tree.attrib["TipoCambio"]
    return tree.attrib.get("TipoCambio", "")


def readReceptor(tree):
    st = Xm.getElem(tree, "Receptor")[0]
    return [st.attrib.get("nombre", "").strip(), st.attrib["rfc"]]


def readEmisor(tree):
    st = Xm.getElem(tree, "Emisor")[0]
    return [st.attrib.get("nombre", "Sin Nombre").strip(), st.attrib["rfc"]]


def readDescuento(tree):
    return tree.attrib.get("descuento", "0.00")


def getRetenciones(tree):
    rets = Xm.getElem(tree, "Retencion")
    d = {}
    for t in rets:
        d[t.attrib["impuesto"]] = t.attrib["importe"]
    return d


def getTraslados(tree):
    tras = Xm.getElem(tree, "Traslado")
    d = {}
    for t in tras:
        if t.attrib["impuesto"] not in d.keys():
            d[t.attrib["impuesto"]] = "0.0"
        d[t.attrib["impuesto"]] = str(float(d[t.attrib["impuesto"]]) +
                                      float(t.attrib["importe"]))
    return d


def getTrasladosDet(tree):
    imps = Xm.getElem(tree, "Impuestos")[0]
    # tras = Xm.getElem(tree, "Traslado")
    tras = Xm.getElem(imps, "Traslado")
    d = {}
    for t in tras:
        r = [t.attrib["impuesto"], t.attrib["tasa"], t.attrib["importe"]]
        if r[0] not in d.keys():
            d[r[0]] = []
        d[r[0]].append(r[1:])
    return d


def getConceptos(tree):
    conc = Xm.getElem(tree, "Concepto")
    d = {}
    for c in conc:
        ki = c.attrib["descripcion"].strip()
        if ki in d.keys():
            d[ki] = [d[ki]]
            d[ki].append(c.attrib["importe"])
        else:
            d[ki] = c.attrib["importe"]
    return d


def getTasaIeps(tree):
    tras = Xm.getElem(tree, "Traslado")
    tasa = "0.00"
    for t in tras:
        if t.attrib.get("impuesto", " ") == "IEPS":
            tasa = t.attrib.get("tasa", "0.00")
    return tasa


def readIva(tree):
    return getTraslados(tree).get("IVA", '0')


def readIeps(tree):
    return getTraslados(tree).get("IEPS", '0')


def readIvaRet(tree):
    return getRetenciones(tree).get("IVA", '0')


def readIsrRet(tree):
    return getRetenciones(tree).get("ISR", '0')


# Generación
# --------------------------------------------------------------------


def cfdiSimple(tree):
    """ Regresa información básica de un cfdi.
    """
    uid = readFolioFiscal(tree)
    em = readEmisor(tree)
    re = readReceptor(tree)
    datos = [readFecha(tree), readSerie(tree), readFolio(tree),
             readSubtotal(tree), readIva(tree), readTotal(tree)]
    return [uid] + em + re + datos


def facturaSimple(tree):
    """ Regresa información básica de una factura.
    """
    uid = readFolioFiscal(tree)
    em = readEmisor(tree)
    re = readReceptor(tree)
    datos = [readFecha(tree), readSerie(tree), readFolio(tree),
             readMoneda(tree), readTC(tree),
             readSubtotal(tree), readIva(tree), readTotal(tree)]
    return [uid] + em + re + datos


def reciboNomina(tree):
    """ Regresa información básica de un recibo en cfdi.

    :param tree: generado por Xm.getXml
    :returns: lista con receptor (nombre y rfc), fecha timbrado,
              UUID, periodo, total percs, total deds, neto,
              diccionario de percepciones y diccionario de deducciones.
    """
    rc = cfdiSimple(tree)
    stn = Xm.getElem(tree, "Nomina")[0]
    fechas = [stn.attrib[k] for k in ["FechaPago", "FechaInicialPago",
                                      "FechaFinalPago"]]
    percs = (float(Xm.leeAtributo(tree, "Percepciones", "TotalGravado")) +
             float(Xm.leeAtributo(tree, "Percepciones", "TotalExento")))

    if Xm.leeAtributo(tree, "Deducciones", "TotalGravado"):
        deds = (float(Xm.leeAtributo(tree, "Deducciones", "TotalGravado")) +
                float(Xm.leeAtributo(tree, "Deducciones", "TotalExento")))
    else:
        deds = 0.0
    ps = Xm.getElem(tree, "Percepcion")
    ds = Xm.getElem(tree, "Deduccion")
    dPs = {x[0]: x[1:] for x in [mkPercDed(p) for p in ps]}
    dDs = {x[0]: x[1:] for x in [mkPercDed(d) for d in ds]}
    return [rc[6], rc[7], rc[0], rc[5], rc[3], rc[4]] + fechas \
        + [percs, deds, dPs, dDs]


def mkPercDed(st):
    """ Convierte un elemento percepcion en una lista.
    """
    return [st.attrib["Clave"], st.attrib.get("Concepto", ""),
            float(st.get("ImporteGravado", 0)) +
            float(st.get("ImporteExento", 0))]


def reciboHonorarios(tree):
    """ Regresa información básica de una factura.
    """
    uid = readFolioFiscal(tree)
    em = readEmisor(tree)
    re = readReceptor(tree)
    rets = getRetenciones(tree)
    riva = rets.get("IVA", "0.0")
    risr = rets.get("ISR", "0.0")
    datos = [readFecha(tree), readSerie(tree), readFolio(tree),
             readMoneda(tree), readTC(tree), readSubtotal(tree),
             readIva(tree), readTotal(tree), riva, risr]

    return [uid] + em + re + datos


def makeCfdi0(tree):
    # rc = cfdiSimple(tree)
    rc = facturaSimple(tree)
    if float(rc[10]) + float(rc[11]) - float(rc[12]) > 0:
        dRets = getRetenciones(tree)
        dcto = readDescuento(tree)
        rets = [dRets.get("IVA", "0.00"), dRets.get("ISR", "0.00")]
        ieps = "0.00"
    elif float(rc[10]) + float(rc[11]) - float(rc[12]) < 0:
        dcto = "0.00"
        ieps = readIeps(tree)
    else:
        dcto = "0.00"
        rets = ["0.00", "0.00"]
        ieps = "0.00"
    return rc[:11] + [dcto, ieps] + [rc[11]] + rets + [rc[12]]


def makeCfdi(tree):
    # rc = cfdiSimple(tree)
    rc = facturaSimple(tree)
    tipo = readTipo(tree)
    dRets = getRetenciones(tree)
    dcto = readDescuento(tree)
    rets = [dRets.get("IVA", "0.00"), dRets.get("ISR", "0.00")]
    ieps = readIeps(tree)
    tasaIeps = getTasaIeps(tree)
    val = float(rc[10]) - float(dcto) + float(ieps) + float(rc[11]) \
        - float(rets[0]) - float(rets[1]) - float(rc[12])
    if val != 0:
        # print(rc[0], val, dcto)
        if abs(abs(val) - float(dcto)) <= 0.01:
            dcto = "0.00"
    return rc[:11] + [dcto, tasaIeps, ieps] + [rc[11]] + rets + [rc[12], tipo]


def makeCfdiPm(tree):
    f = facturaSimple(tree)
    if float(f[10]) + float(f[11]) - float(f[12]) > 0:
        dcto = readDescuento(tree)
    else:
        dcto = "0.00"
    return f[:11] + [dcto] + [f[11]] + [f[12]]
