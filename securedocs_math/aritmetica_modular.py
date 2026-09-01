def mod(a, n):
    """Resto sempre positivo. Em C e Java -7 % 3 dá -1, aqui dá 2."""
    if n == 0:
        raise ValueError("módulo não pode ser zero")
    return a % abs(n)


def soma_mod(a, b, n):
    return mod(a + b, n)


def sub_mod(a, b, n):
    return mod(a - b, n)


def mult_mod(a, b, n):
    return mod(a * b, n)


def congruentes(a, b, n):
    return mod(a - b, n) == 0


def tabela_mod(n, operacao="*"):
    tabela = []
    for a in range(n):
        linha = []
        for b in range(n):
            if operacao == "+":
                linha.append(soma_mod(a, b, n))
            else:
                linha.append(mult_mod(a, b, n))
        tabela.append(linha)
    return tabela


def ordem_multiplicativa(a, n):
    """Menor k > 0 com a^k = 1 (mod n)."""
    from .mdc import mdc

    if mdc(a, n) != 1:
        raise ValueError("a e n precisam ser coprimos")
    if abs(n) == 1:
        return 1
    a = mod(a, n)
    k = 1
    atual = a
    while atual != 1:
        atual = (atual * a) % n
        k += 1
    return k
