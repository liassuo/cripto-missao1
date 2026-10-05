def ler_int(texto, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(texto))
        except ValueError:
            print("  precisa ser um número inteiro")
            continue
        if minimo is not None and valor < minimo:
            print("  precisa ser pelo menos %d" % minimo)
            continue
        if maximo is not None and valor > maximo:
            print("  no máximo %d" % maximo)
            continue
        return valor


def ler_texto(texto, padrao=""):
    valor = input(texto).strip()
    if not valor:
        print("  (usando: %s)" % padrao)
        return padrao
    return valor
