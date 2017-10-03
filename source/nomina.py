# -*- coding="utf-8" -*-

import fechas as Fe
import support as Sp


def reverse(s):
    return s[-1::-1]


def fmtNumber(num):
    s = str(int(100*round(toFloat(num), 2)))
    while len(s) < 3:
        s = "0" + s
    return comas(s[:-2])+"."+s[-2:]


def comas(s):
    s = reverse(s)
    t = ""
    while len(s) > 3:
        t += s[:3] + ","
        s = s[3:]
    t += s
    return reverse(t)


def toInt(num):
    if not num:
        return 0
    elif isinstance(num, str):
        return int(num.replace(",", "").replace(" ", ""))
    else:
        return int(num)


def toFloat(num):
    if not num:
        return 0.0
    else:
        if isinstance(num, str):
            return float(num.replace(",", ""))
        else:
            return float(num)


def calculaIsr(base):
    """ Calcula el impuesto correspondiente a un ingreso mensual.

    :param base: importe gravado mensual.
    :return: ISR correspondiente.

    El resultado se redondea a pesos.
    Utiliza la tabla global tarifaISR.
    """
    global tarifaIsr
    for x in tarifaIsr:
        if x[0] <= base:
            return round((base - x[0]) * x[2] / 100 + x[1], 2)
    return 0


def calculaSem(base):
    """ Calcula el subsidio al empleo de un ingreso mensual.

    :param base: importe gravado mensual.
    :return: Subsidio al empleo correspondiente.

    Se redondea a pesos, utiliza tabla global tarifaSem
    """
    global tarifaSem
    for x in tarifaSem:
        if x[0] <= base:
            return x[1]
    return 0


def cuotaObrera(sbc, dias, inc=0, aus=0):
    """ Calcula la cuota obrera correspondiente.

    :param sbc: salario base de cotización.
    :param dias: días del período de cuotas.
    :param inc: días de incapacidad.
    :param aus: días de ausentismo.
    :return: El importe de la cuota obrera.

    Calcula las tres bases de cálculo y aplica los factores globales.
    """
    global tarifaImss, smza
    bases = (max(0, sbc-3*smza) * (dias - inc) / 100,
             sbc * (dias - inc) / 100,
             sbc * (dias - inc - aus) / 100)
    return round(Sp.dotProduct(bases, tarifaImss), 2)


def calculaAnt(alta, fecha):
    """ Calcula el año de antigüedad corriendo a la fecha, a partir de alta.

    :param alta: La fecha incial para la antigüedad.
    :param fecha: La fecha de cálculo para la antigüedad.
    :return: El año de antigüedad que está transcurriendo.

    Regresa 1 si la fecha es menor al mismo día del siguiente año del alta,
    2, a partir del mismo día del siguiente año, y así sucesivamente.
    """
    fe = fecha[:4]+alta[4:]
    dif = int(fecha[:4]) - int(alta[:4])
    if fe < fecha:
        return dif + 1
    else:
        return dif


def diasDespues(alta, fecha):
    """ Calcula los días transcurridos del año de antigüedad en curso.

    :param alta: Fecha inicial de cálculos.
    :param fecha: Fecha final de cálculos.
    :return: Regresa el número de días transcurridos desde el último
             cierre de año de antigüedad.
    """
    fe = fecha[:4]+alta[4:]
    if fe > fecha:
        fe = str(int(fecha[:4])-1)+alta[4:]
    return Fe.difFechas(fe, fecha) + 1


def diasPasados(fecha):
    """ Regresa los días del año transcurridos a la fecha dada, incluido.

    :param fecha: La fecha a la que se cuenta.
    :return: días transcurridos en el año a la fecha dada, inclusive.
    """
    return Fe.difFechas(fecha[:4]+"0101", fecha) + 1


def diasVacaciones(antig):
    """ Regresa los días de vacaciones correspondintes a la antigüedad dada.

    :param antig: Antigüedad.
    :return: Dias de vacaciones correspondientes, prestaciones de ley.

    Aplica criterio de SCJ, benéfico al trabajador.
    """
    if antig < 6:
        return (antig - 1) * 2 + 6
    else:
        return (antig - 5) // 5 * 2 + 14


def minimoZona(zona):
    """ Regresa el salario mínimo correspondiente.

    :param zona: zona geográfica aplicable.
    :return: salario mínimo correspondiente.
    """
    global smza, smzb
    if zona.upper() == "A":
        return smza
    else:
        return smzb


def mesAsemana(importe):
    """ Convierte un importe mensual al correspondiente semanal.

    :param importe: importe a convertir
    """
    return round(7 * importe / 30.4, 2)


def semanaAmes(importe):
    """ Convierte un importe mensual al correspondiente semanal.

    :param importe: importe a convertir
    """
    return round(30.4 * importe / 7, 2)


def elevar(importe, completo, parte):
    """ Convierte un importe según una proporción.
    """
    return round(parte * importe / completo, 2)


def isrSemanal(base):
    """ Calcula el impuesto correspondiente a un ingreso semanal.

    :param base: base del impuesto a calcular.
    """
    return mesAsemana(calculaIsr(semanaAmes(base)))


def semSemanal(base):
    """ Calcula el subsidio al empleo de un ingresos semanal.

    :param base: base del subsidio a calcular.
    """
    return mesAsemana(calculaSem(semanaAmes(base)))


def semQuincenal(base):
    """ Calcula el subsidio al empleo de un ingreso quincenal.
    """
    return elevar(calculaSem(elevar(base, 15, 30)), 30.4, 15)


def isrQuincenal(base):
    """ Calcula el impuesto de un ingreso quincenal.
    """
    return elevar(calculaIsr(elevar(base, 30.4, 15)), 15, 30.4)


def ordinarioSemanal(salario, dias):
    """ Calcula el salario ordinario semanal.
    """
    return elevar(salario * dias, 6, 7)


def ordinarioSemanal5(salario, dias):
    """ Calcula el salario ordinal semanal en semana de cinco días.
    """
    return elevar(salario * dias, 7, 5)


def ordinarioMensual(salario, dias):
    """ Calcula el salario mensual con ajuste a 365 días.
    """
    return elevar(salario * dias, 30, 30.4)


def ordinarioQuincenal(salario, dias):
    """ Calcula el salario quincenal con ajuste a 365 días.
    """
    return elevar(salario * dias, 30, 30.4)


def extraDoble(salario, horas):
    """ Calcula el tiempo extra doble.
    """
    return elevar(salario, 4, horas)


def extraTriple(salario, horas):
    """ Calcula el tiempo extra triple.
    """
    return elevar(salario * 3, 8, horas)


def extraDescanso(salario, horas):
    """ Calcula el salario por día de descanso trabajado.
    """
    return extraDoble(salario, horas)


def extraFestivo(salario, horas):
    """ Calcula el pago por día festivo trabajado.
    """
    return extraDoble(salario, horas)


def primaDominical(salario, primas):
    """ Calcula el importe de la prima dominical.
    """
    return round(salario * 0.25 * primas, 2)


def aguinaldo(salario, dias, faltas=0):
    """ Calcula el aguinaldo anual completo.
    """
    return round((salario * dias) * (365 - faltas) / 365, 2)


def vacaciones(salario, dias):
    """ Calcula las vacaciones.
    """
    return round(salario * dias, 2)


def vacacionesSemanal(salario, dias):
    return elevar(vacaciones(salario, dias), 6, 7)


def primaVac(salario, dias, prima):
    """ Calcula la prima vacacional.
    """
    return round(vacaciones(salario, dias) * prima, 2)


def vacacionesParcial(salario, anual, dias):
    """ Calcula partes proporcionales de vacaciones.
    """
    return elevar(vacaciones(salario, anual), 365, dias)


def primaVacParcial(salario, anual, dias, prima):
    return round(vacacionesParcial(salario, anual, dias) * prima, 2)


def vacacionesParcialSemanal(salario, anual, dias):
    return elevar(vacacionesParcial, 6, 7)


def aguinaldoParcial(salario, anual, dias):
    """ Calcula partes proporcionales de aguinaldo.
    """
    return elevar(aguinaldo(salario, anual), 365, dias)


def extraExento(importe, sm, salario):
    """ Calcula el importe de tiempo extra exento de ISR.

    :param importe: Importe del tiempo extra y descansos.
    :param sm: salario mínimo de la zona.
    """
    if salario == sm:
        return extraDoble(importe)
    else:
        return min(5 * sm, round(importe / 2, 2))


def primaDomExenta(importe, primas, sm):
    return min(importe, sm) * primas


def aguinaldoExento(importe, sm):
    """ Calcula el importe del aguinaldo exento de ISR.
    """
    return min(importe, 30 * sm)


def primaVacExenta(importe, sm):
    """ Calcula el importe de prima vacacional exenta de ISR.
    """
    return min(15 * sm, importe)


def partesProporcionales(salario, fecha, alta, faltas_ag, faltas_vac,
                         prima, anual_ag, anual_vac):
    """ Calcula las partes proporcionales a pagar con las fechas dadas.

    :param salario: El salario diario del trabajador.
    :param fecha: Fecha del cálculo.
    :param alta: Fecha de alta del trabajador.
    :param faltas_ag: Días a descontar por ausentismo en aguinaldo.
    :param fatas_vac: Días a descontar en vacaciones.
    :param prima: Factor de prima vacacional.
    :param anual_ag: días de aguinaldo anual.
    :param anual_vac: días de vacaciones anuales.
    :return: (aguinaldo, vacaciones, prima vacacional)
    """
    dias_vac = diasDespues(alta, fecha) - faltas_vac
    dias_ag = min(diasPasados(fecha), diasDespues(alta, fecha)) - faltas_ag
    ag = aguinaldoParcial(salario, anual_ag, dias_ag)
    vc = vacacionesParcial(salario, anual_vac, dias_vac)
    pv = round(vc * prima, 2)
    return (ag, vc, pv)


def calcNominaQuincenal(tiempos, pars):
    global smza
    nom = {}
    nom["errores"] = []
    claves = ""
    exentas = 0
    total = 0
    # ds = pars.get("ds", 15)
    # sm = pars.get("sm", smza)
    if "dt" in tiempos.keys():
        salario = pars.get("sd", 0)
        if salario == 0:
            nom["errores"].append("No se da salario")
            claves += "s"
        else:
            nom["ord"] = ordinarioQuincenal(salario, tiempos["dt"])
            total += nom["ord"]

    base = total - exentas
    t_sem = semQuincenal(base)
    t_isr = isrQuincenal(base)
    nom["sem"] = max(0, t_sem - t_isr)
    nom["isr"] = max(0, t_isr - t_sem)
    nom["imss"] = cuotaObrera(pars["si"], 15, tiempos.get("aus", 0),
                              tiempos.get("inc", 0))
    return nom


def calcNominaSemanal(tiempos, pars):
    """ Calcula una nómina completa en base a dos diccionarios de datos.

    :param tiempos: diccionario con los tiempos trabajados.
    :param pars: diccionario con los datos de salario, prestaciones y fechas.
    :return: diccionario con los datos de la nómina.
    * tiempos admite las siguientes llaves:
        * dt: días trabajados
        * ed: horas dobles
        * et: horas triples
        * dd: horas en día de descanso
        * df: horas en día festivo
        * pd: primas dominicales
        * dv: días de vacaciones
        * ag: pagar aguinaldo
        * pv: pagar prima vacacional
        * dpv: días prima vacacional
        * fa: faltas aguinaldo
        * fv: faltas vacaciones
        * aus: faltas en la semana
        * inc: incapacidades en la semana
    * pars admite:
        * sd: salario diario
        * si: salario integrado
        * fa: fecha de alta
        * fb: fecha de baja
        * ci: crédito infonavit
        * ds: días del período (6 o 5)
        * pv: factor de prima vacacional
        * da: días aguinaldo anual
        * dv: días vacaciones
    * el diccionario regresado admite:
        * ord: Percepción ordinaria
        * ted: Tiempo extra doble
        * tet: Tiempo extra triple
        * vac: Vacaciones
        * pv: Prima vacacional
        * pvac: Vacaciones proporcionales
        * ppv: Prima vacacional proporcional
        * ag: Aguinaldo
        * pag: Aguinaldo proporcional
        * dd: Día descanso
        * df: Día festivo
        * pd: Prima dominical
        * xte: Tiempo extra exento
        * xv: Prima vacacional exenta
        * xpd: Prima dominical exenta
        * xa: Aguinaldo exento
        * sem: Subsidio al empleo
        * isr: ISR retenido
        * imss: Cuota obrera IMSS
        * ci: Crédito Infonavit
        * errores: Lista de posibles errores.

    Cualquier otro concepto de entrada o salida tiene que agregarse al código.
    Cualquier otra llave que se incluya en los diccionarios de salida será
    ignorada.
    """
    global smza
    nom = {}
    nom["errores"] = []
    claves = ""
    exentas = 0
    total = 0
    ds = pars.get("ds", 6)
    sm = pars.get("sm", smza)
    if "dt" in tiempos.keys():
        salario = pars.get("sd", 0)
        if salario == 0:
            nom["errores"].append("No se da salario")
            claves += "s"
        else:
            if ds == 6:
                nom["ord"] = ordinarioSemanal(salario, tiempos["dt"])
            else:
                nom["ord"] = ordinarioSemanal5(salario, tiempos["dt"])
            total += nom["ord"]

    if "ed" in tiempos.keys() and "s" not in claves:
        nom["ted"] = extraDoble(salario, tiempos["ed"])
        total += nom["ted"]

    if "et" in tiempos.keys() and "s" not in claves:
        nom["tet"] = extraTriple(salario, tiempos["et"])
        total += nom["tet"]

    if "dd" in tiempos.keys() and "s" not in claves:
        nom["dd"] = extraDescanso(salario, tiempos["dd"])
        total += nom["dd"]

    if "df" in tiempos.keys() and "s" not in claves:
        nom["df"] = extraFestivo(salario, tiempos["df"])
        total += nom["df"]

    if "pd" in tiempos.keys() and "s" not in claves:
        nom["pd"] = primaDominical(salario, tiempos["pd"])
        nom["xpd"] = primaDomExenta(nom["pd"], tiempos["pd"], sm)
        total += nom["pd"]
        exentas += nom["xpd"]

    extras = nom.get("ted", 0) + nom.get("dd", 0) + nom.get("df", 0)
    nom["xte"] = extraExento(extras, sm, salario)
    exentas += nom["xte"]
#    print("Exentas 1", exentas, extras, sm, salario)

    if tiempos.get("ag", 0) and "s" not in claves and "fb" not in pars.keys():
        dias_ag = pars.get("da", 15)
        faltas_ag = tiempos.get("fa", 0)
        nom["ag"] = aguinaldo(salario, dias_ag, faltas_ag)
        total += nom["ag"]
        # nom["xa"] = aguinaldoExento(nom["ag"], sm)
        # exentas += nom["xa"]

    if "dv" in tiempos.keys() and "s" not in claves:
        nom["vac"] = vacacionesSemanal(salario, tiempos["dv"])
        total += nom["vac"]

    if "dpv" in tiempos.keys():
        nom["pv"] = round(vacaciones(salario, tiempos["dpv"])
                          * pars.get("pv", 0.25), 2)
    elif pars.get("pv", 0):
        nom["pv"] = round(pars.get("pv", 0.25) * nom.get("vac", 0), 2)
        total += nom["pv"]

    if "fb" in pars.keys():
        if "fa" not in pars.keys():
            nom["errores"].append("No hay fecha de alta y se pide baja")
            claves += "a"
        faltas_vacs = tiempos.get("fv", 0)
        faltas_ag = tiempos.get("fa", 0)
        if "a" not in claves:
            nom["pag"], nom["pvac"], nom["ppv"] = \
                partesProporcionales(salario, pars["fb"], pars["fa"],
                                     faltas_ag, faltas_vacs, pars["pv"],
                                     pars.get("da", 15), pars["dv"])
            total += nom["pag"] + nom["pvac"] + nom["ppv"]
            # nom["xv"] = primaVacExenta(nom["ppv"] + nom.get("pv", 0), sm)
            # nom["xa"] = aguinaldoExento(nom["ag"], sm)
            # exentas += nom["xv"] + nom["xa"]

    t_aguinaldo = nom.get("ag", 0) + nom.get("pag", 0)
    t_prima_vac = nom.get("pv", 0) + nom.get("ppv", 0)
    if t_aguinaldo:
        nom["xa"] = aguinaldoExento(t_aguinaldo, sm)
    if t_prima_vac:
        nom["xv"] = primaVacExenta(t_prima_vac, sm)
    exentas += nom.get("xa", 0) + nom.get("xv", 0)
#    print("exentas 2", exentas)

    base = total - exentas
    t_sem = semSemanal(base)
    t_isr = isrSemanal(base)
    print("Base", base, t_sem, t_isr)
    nom["sem"] = max(0, t_sem - t_isr)
    nom["isr"] = max(0, t_isr - t_sem)
    nom["imss"] = cuotaObrera(pars["si"], 7, tiempos.get("aus", 0),
                              tiempos.get("inc", 0))
    imp_ci = pars.get("ci", 0)
    if imp_ci:
        nom["ci"] = imp_ci
    return nom


def nom2list(nomina):
    """ Convierte un diccionario de nómina a un formato desplegable.
    """
    percs = []
    deds = []
    if "ord" in nomina.keys():
        percs.append(("Ordinario", fmtNumber(nomina["ord"])))
    if "ted" in nomina.keys():
        percs.append(("Extra doble", fmtNumber(nomina["ted"])))
    if "tet" in nomina.keys():
        percs.append(("Extra triple", fmtNumber(nomina["tet"])))
    if "vac" in nomina.keys():
        percs.append(("Vacaciones", fmtNumber(nomina["vac"])))
    if "pv" in nomina.keys():
        percs.append(("Prima vacacional",
                      fmtNumber(nomina["pv"] + nomina.get("ppv", 0))))
    if "pvac" in nomina.keys():
        percs.append(("Vacaciones P.P.", fmtNumber(nomina["pvac"])))
    if "ag" in nomina.keys():
        percs.append(("Aguinaldo", fmtNumber(nomina["ag"])))
    if "pag" in nomina.keys():
        percs.append(("Aguinaldo P. P.", fmtNumber(nomina["pag"])))
    if "dd" in nomina.keys():
        percs.append(("Día descanso", fmtNumber(nomina["dd"])))
    if "df" in nomina.keys():
        percs.append(("Día festivo:", fmtNumber(nomina["df"])))
    if "pd" in nomina.keys():
        percs.append(("Prima Dominical", fmtNumber(nomina["pd"])))
    if "sem" in nomina.keys():
        percs.append(("Subsidio al empleo", fmtNumber(nomina["sem"])))

    if "isr" in nomina.keys():
        deds.append(("I. S. R.", fmtNumber(nomina["isr"])))
    if "imss" in nomina.keys():
        deds.append(("I.M.S.S", fmtNumber(nomina["imss"])))
    if "ci" in nomina.keys():
        deds.append(("Crédito Infonavit", fmtNumber(nomina["ci"])))
    totales = [sum([toFloat(x[1]) for x in percs]),
               sum([toFloat(x[1]) for x in deds])]
    totales.append(totales[0] - totales[1])
    return percs, deds, totales


smza = 70.10
smzb = 68.28

tarifaImss = (.4, .625, 1.75)

tarifaIsr = ((250000.01, 78404.23, 35),
             (83333.34, 21737.57, 34),
             (62500.01, 15070.9, 32),
             (32736.84, 6141.95, 30),
             (20770.3, 3327.42, 23.52),
             (10298.36, 1090.61, 21.36),
             (8601.51, 786.54, 17.92),
             (7399.43, 594.21, 16),
             (4210.42, 247.24, 10.88),
             (496.08, 9.52, 6.4),
             (0.00, 0, 1.92))

tarifaSem = ((7382.34, 0),
             (7113.91, 217.61),
             (6224.68, 253.54),
             (5335.43, 294.63),
             (4717.19, 324.87),
             (4446.16, 354.23),
             (3537.88, 382.46),
             (3472.85, 392.77),
             (2653.39, 406.62),
             (1768.97, 406.83),
             (0.01, 407.02),
             (0, 0))
