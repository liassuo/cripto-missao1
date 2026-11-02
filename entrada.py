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
        if padrao:
            print("  (usando: %s)" % padrao)
        return padrao
    return valor


def ler_hex(texto, n_bytes, padrao):
    while True:
        valor = input(texto).strip().replace(" ", "")
        if not valor:
            print("  (usando: %s)" % padrao)
            return bytes.fromhex(padrao)
        try:
            dados = bytes.fromhex(valor)
        except ValueError:
            print("  use só 0-9 e A-F")
            continue
        if len(dados) != n_bytes:
            print("  precisa ter %d bytes (%d dígitos hex)" % (n_bytes, 2 * n_bytes))
            continue
        return dados
