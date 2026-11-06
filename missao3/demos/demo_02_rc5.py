import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_simetrica import rc5, vetores
from securedocs_simetrica.blocos import para_hex, de_hex
from textos import MENSAGEM, CHAVE_RC5
from tela import mostrar_mensagem_inteira


def mostrar(chave, w, r, texto):
    cifra = rc5.Cifra(chave, w, r)
    p, q = rc5.CONSTANTES[w]
    d = w // 4                      # dígitos hex de uma palavra
    m = cifra.mascara
    print("%s: palavra de %d bits, bloco de %d bits (2 palavras), %d rodadas, chave de %d bytes"
          % (cifra.nome, w, 2 * w, r, len(chave)))

    print("\nPASSO 1 - expansão da chave: a tabela S (as subchaves)")
    print("  começa com as constantes P = %0*X (vem de e)" % (d, p))
    print("                       e   Q = %0*X (vem da razão áurea)" % (d, q))
    print("  S[0] = P, S[i] = S[i-1] + Q, depois a chave é misturada 3 vezes na tabela")
    print("  S tem 2(r + 1) = %d palavras; as 4 primeiras:" % len(cifra.S))
    print("  " + " ".join("%0*X" % (d, s) for s in cifra.S[:4]))

    bloco = texto.encode("utf-8")[:cifra.tamanho_bloco].ljust(cifra.tamanho_bloco, b" ")
    a, b = cifra._palavras(bloco)
    print("\nPASSO 2 - o texto claro vira duas palavras, A e B")
    print("  texto claro: %r = %s" % (bloco.decode("utf-8", "replace"), para_hex(bloco)))
    print("  A = %0*X   B = %0*X   (bytes ao contrário: little-endian)" % (d, a, d, b))
    a, b = (a + cifra.S[0]) & m, (b + cifra.S[1]) & m
    print("  A = A + S[0] = %0*X   B = B + S[1] = %0*X" % (d, a, d, b))

    print("\nPASSO 3 - as %d rodadas" % r)
    print("  A = ((A xor B) <<< B) + S[2i]     B = ((B xor A) <<< A) + S[2i+1]")
    x = a ^ b
    giro = b % w
    novo_a = (rc5.girar_esq(x, giro, w) + cifra.S[2]) & m
    print("  rodada 1 em detalhe:")
    print("    A xor B          = %0*X" % (d, x))
    print("    <<< B            = gira %d casas (B mod %d) = %0*X" % (giro, w, d, rc5.girar_esq(x, giro, w)))
    print("    + S[2]           = A novo = %0*X   (o B faz o mesmo usando o A novo)" % (d, novo_a))
    passos = []
    cifrado = cifra.cifrar_bloco(bloco, passos)
    print("\n  rodada   A%sB" % (" " * (d + 5)))
    for i, a, b in passos:
        print("    %2d     %0*X     %0*X" % (i, d, a, d, b))

    print("\nPASSO 4 - texto cifrado = A e B no fim: %s" % para_hex(cifrado))
    print("\nPASSO 5 - decifrar: tudo ao contrário, da rodada %d até a 1" % r)
    print("  subtrai S, gira para a direita e faz o xor; no fim tira S[0] e S[1]")
    print("  texto decifrado: %r" % cifra.decifrar_bloco(cifrado).decode("utf-8", "replace"))

    mostrar_mensagem_inteira(cifra, texto)


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
