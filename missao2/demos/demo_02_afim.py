import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from missao1.securedocs_math.inverso_multiplicativo import inverso_passos
from securedocs_classica import afim
from textos import MENSAGEM


def main():
    print("=== 2. CIFRA AFIM ===\n")
    print("C = (a*P + b) mod 26   e   P = a^-1 * (C - b) mod 26\n")

    a, b = 5, 8
    cifrado = afim.cifrar(MENSAGEM, a, b)
    print("chave (a, b) = (%d, %d)" % (a, b))
    print("texto claro: %s" % MENSAGEM)
    print("cifrado    : %s" % cifrado)

    print("\npara decifrar precisa do inverso de a - biblioteca da missão 1:")
    for linha in inverso_passos(a, 26):
        print("  " + linha)
    print("decifrado  : %s" % afim.decifrar(cifrado, a, b))

    print("\nnem todo 'a' serve: com a = 13, A e N viram a mesma letra")
    print("  mdc(13, 26) = 13 -> chave_valida(13) = %s" % afim.chave_valida(13))
    validos = sorted(set(a for a, _ in afim.chaves_validas()))
    print("  valores de a que funcionam: %s" % validos)
    print("  total de chaves: %d x 26 = %d" % (len(validos), len(afim.chaves_validas())))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    while True:
        a = ler_int("a (coprimo com 26): ", 1, 25)
        if afim.chave_valida(a):
            break
        print("  %d não é coprimo com 26, escolha outro (1, 3, 5, 7, 9, 11, 15...)" % a)
    b = ler_int("b (0 a 25): ", 0, 25)
    cifrado = afim.cifrar(texto, a, b)
    print("\ncifrado  : %s" % cifrado)
    print("decifrado: %s" % afim.decifrar(cifrado, a, b))


if __name__ == "__main__":
    main()
