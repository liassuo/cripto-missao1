import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_simetrica import rc5, modos, vetores
from securedocs_simetrica.blocos import para_hex, de_hex
from textos import MENSAGEM, CHAVE_RC5


def mostrar(chave, w, r, texto):
    cifra = rc5.Cifra(chave, w, r)
    p, q = rc5.CONSTANTES[w]
    digitos = w // 4
    print("%s: palavra de %d bits, bloco de %d bits, %d rodadas, chave de %d bytes"
          % (cifra.nome, w, 2 * w, r, len(chave)))
    print("constantes: P = %0*X (vem de e)   Q = %0*X (vem da razão áurea)"
          % (digitos, p, digitos, q))
    print("tabela S com 2(r + 1) = %d palavras, as 4 primeiras:" % len(cifra.S))
    print("  " + " ".join("%0*X" % (digitos, s) for s in cifra.S[:4]))

    bloco = texto.encode("utf-8")[:cifra.tamanho_bloco].ljust(cifra.tamanho_bloco, b" ")
    passos = []
    cifrado = cifra.cifrar_bloco(bloco, passos)
    print("\nprimeiro bloco: %r = %s" % (bloco.decode("utf-8", "replace"), para_hex(bloco)))
    print("rodada   A                    B")
    for i, a, b in passos:
        print("  %2d     %0*X%s%0*X" % (i, digitos, a, " " * (21 - digitos), digitos, b))
    print("cifrado  : %s" % para_hex(cifrado))
    print("decifrado: %s" % cifra.decifrar_bloco(cifrado).decode("utf-8", "replace"))

    iv, tudo = modos.cifrar_cbc(cifra, texto.encode("utf-8"))
    print("\nmensagem inteira em CBC: %s" % para_hex(tudo, cifra.tamanho_bloco))
    print("decifrada              : %s" % modos.decifrar_cbc(cifra, tudo, iv).decode("utf-8"))


def main():
    print("=== 2. RC5 (Rivest, 1994) ===\n")
    print("só usa soma mod 2^w, xor e rotação (ARX). Em cada rodada:")
    print("  A = ((A xor B) <<< B) + S[2i]")
    print("  B = ((B xor A) <<< A) + S[2i + 1]")
    print("a rotação depende do próprio dado (<<< B), é daí que vem a força\n")

    mostrar(de_hex(CHAVE_RC5), 32, 12, MENSAGEM)

    print("\nvetores de teste do artigo do Rivest:")
    for nome, chave, claro, esperado, obtido, fonte, ok in vetores.conferir("RC5"):
        print("  P = %s -> %s  %s" % (claro, obtido, "OK" if ok else "ERRO"))

    print("\no mesmo bloco com outros parâmetros (a mesma implementação serve para todos):")
    for w, r in ((16, 12), (32, 12), (32, 20), (64, 24)):
        cifra = rc5.Cifra(de_hex(CHAVE_RC5), w, r)
        bloco = b"SECUREDOCS-TECHSECURE"[:cifra.tamanho_bloco]
        print("  %-16s bloco %-3d bits -> %s" % (cifra.nome, 2 * w, para_hex(cifra.cifrar_bloco(bloco))))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    chave = ler_texto("chave (texto): ", "TECHSECURE").encode("utf-8")
    w = 0
    while w not in rc5.CONSTANTES:
        w = ler_int("tamanho da palavra w (16, 32 ou 64): ", 16, 64)
    r = ler_int("rodadas (1 a 255): ", 1, 255)
    print()
    mostrar(chave, w, r, texto)


if __name__ == "__main__":
    main()
