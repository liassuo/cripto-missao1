from .mdc import mdc, mmc
from .primos import fatorar, eh_primo


def phi_contagem(n):
    """Conta um por um quantos são coprimos com n."""
    if n < 1:
        raise ValueError("n precisa ser positivo")
    total = 0
    for k in range(1, n + 1):
        if mdc(k, n) == 1:
            total += 1
    return total


def phi(n):
    if n < 1:
        raise ValueError("n precisa ser positivo")
    if n == 1:
        return 1
    # phi(n) = n * (1 - 1/p) para cada primo p que divide n
    resultado = n
    for p in fatorar(n):
        resultado = resultado - resultado // p
    return resultado


def phi_de_primos(p, q):
    if not eh_primo(p) or not eh_primo(q):
        raise ValueError("p e q precisam ser primos")
    if p == q:
        raise ValueError("p e q precisam ser diferentes")
    return (p - 1) * (q - 1)


def phi_ate(limite):
    tabela = list(range(limite + 1))
    for i in range(2, limite + 1):
        if tabela[i] == i:          # i é primo
            for j in range(i, limite + 1, i):
                tabela[j] -= tabela[j] // i
    return tabela


def teorema_euler(a, n):
    """a^phi(n) = 1 (mod n) quando mdc(a, n) = 1."""
    if mdc(a, n) != 1:
        raise ValueError("o teorema exige mdc(a, n) = 1")
    return pow(a, phi(n), n) == 1


def pequeno_teorema_fermat(a, p):
    if not eh_primo(p):
        raise ValueError("p precisa ser primo")
    if a % p == 0:
        raise ValueError("p não pode dividir a")
    return pow(a, p - 1, p) == 1


def carmichael(n):
    """Menor L com a^L = 1 (mod n) para todo a coprimo com n."""
    if n < 1:
        raise ValueError("n precisa ser positivo")
    if n == 1:
        return 1
    resultado = 1
    for p, k in fatorar(n).items():
        if p == 2 and k >= 3:
            termo = 2 ** (k - 2)
        else:
            termo = (p - 1) * p ** (k - 1)
        resultado = mmc(resultado, termo)
    return resultado
