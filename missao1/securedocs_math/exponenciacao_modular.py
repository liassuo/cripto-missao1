from .aritmetica_modular import mod


def exp_mod(base, expoente, n):
    """base^expoente mod n percorrendo os bits do expoente."""
    if n == 0:
        raise ValueError("módulo não pode ser zero")
    n = abs(n)
    if n == 1:
        return 0
    if expoente < 0:
        from .inverso_multiplicativo import inverso_multiplicativo
        base = inverso_multiplicativo(base, n)
        expoente = -expoente

    resultado = 1
    base = mod(base, n)
    while expoente > 0:
        if expoente % 2 == 1:
            resultado = (resultado * base) % n
        base = (base * base) % n
        expoente //= 2
    return resultado


def exp_mod_ingenua(base, expoente, n):
    """Multiplica uma vez para cada unidade do expoente."""
    if expoente < 0:
        raise ValueError("só expoente >= 0")
    resultado = 1 % abs(n)
    base = mod(base, n)
    for _ in range(expoente):
        resultado = (resultado * base) % n
    return resultado


def exp_mod_passos(base, expoente, n):
    passos = ["Calculando %d^%d mod %d" % (base, expoente, n)]
    passos.append("Expoente em binário: " + bin(expoente)[2:])
    resultado = 1
    b = mod(base, n)
    e = expoente
    i = 0
    while e > 0:
        if e % 2 == 1:
            novo = (resultado * b) % n
            passos.append("  bit %d = 1 -> resultado = %d * %d mod %d = %d" % (i, resultado, b, n, novo))
            resultado = novo
        else:
            passos.append("  bit %d = 0 -> resultado continua %d" % (i, resultado))
        b = (b * b) % n
        e //= 2
        i += 1
    passos.append("Resultado final: %d" % resultado)
    return passos
