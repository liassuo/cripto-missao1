import secrets

from .mdc import mdc

PRIMOS_PEQUENOS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                   67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
                   139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]


def eh_primo_forca_bruta(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def crivo_eratostenes(limite):
    if limite < 2:
        return []
    eh_primo = [True] * (limite + 1)
    eh_primo[0] = eh_primo[1] = False
    p = 2
    while p * p <= limite:
        if eh_primo[p]:
            for multiplo in range(p * p, limite + 1, p):
                eh_primo[multiplo] = False
        p += 1
    return [i for i in range(limite + 1) if eh_primo[i]]


def miller_rabin(n, rodadas=40):
    """Teste probabilístico. Chance de errar menor que 4^-rodadas."""
    if n < 2:
        return False
    for p in PRIMOS_PEQUENOS:
        if n == p:
            return True
        if n % p == 0:
            return False

    # escreve n - 1 como 2^r * d, com d ímpar
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(rodadas):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composto = True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                composto = False
                break
        if composto:
            return False
    return True


def eh_primo(n):
    if n < 1000000:
        return eh_primo_forca_bruta(n)
    return miller_rabin(n)


def gerar_primo(bits=512, rodadas=40):
    # secrets no lugar de random porque o random é previsível
    if bits < 8:
        raise ValueError("use pelo menos 8 bits")
    while True:
        candidato = secrets.randbits(bits)
        candidato |= (1 << (bits - 1))   # garante o tamanho
        candidato |= 1                   # garante que é ímpar
        if miller_rabin(candidato, rodadas):
            return candidato


def proximo_primo(n):
    candidato = max(2, n + 1)
    if candidato % 2 == 0 and candidato != 2:
        candidato += 1
    while not eh_primo(candidato):
        if candidato == 2:
            candidato = 3
        else:
            candidato += 2
    return candidato


def fatorar(n):
    if n < 2:
        return {}
    fatores = {}
    while n % 2 == 0:
        fatores[2] = fatores.get(2, 0) + 1
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            fatores[f] = fatores.get(f, 0) + 1
            n //= f
        f += 2
    if n > 1:
        fatores[n] = fatores.get(n, 0) + 1
    return fatores


def pollard_rho(n):
    """Acha um fator de n. Bem mais rápido que dividir um por um."""
    if n % 2 == 0:
        return 2
    if eh_primo(n):
        return n
    while True:
        x = secrets.randbelow(n - 2) + 2
        y = x
        c = secrets.randbelow(n - 1) + 1
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = mdc(abs(x - y), n)
        if d != n:
            return d
