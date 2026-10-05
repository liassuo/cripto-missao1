import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_classica import vigenere, hill, fluxo
from securedocs_classica.frequencia import indice_coincidencia
from securedocs_classica.criptoanalise import ic_por_tamanho, kasiski, quebrar_vigenere, reuso_de_fluxo
from textos import MENSAGEM, CONTRATO


def main():
    print("=== 11. AS CIFRAS \"MAIS FORTES\" TAMBÉM CAEM ===\n")

    print("--- Vigenère (precisa de texto maior, usamos o contrato) ---")
    cifrado = vigenere.cifrar(CONTRATO, "SEGREDO")
    print("IC do português ~0,078 | IC do cifrado = %.3f (parece aleatório)"
          % indice_coincidencia(cifrado))

    print("\n1) Kasiski: trechos repetidos e quantas distâncias cada m divide")
    distancias, votos = kasiski(cifrado)
    print("   %d repetições, ex.: %s" % (len(distancias), distancias[:4]))
    mais_votados = sorted(votos.items(), key=lambda par: -par[1])[:3]
    print("   mais votados: %s" % mais_votados)

    print("\n2) IC médio separando em m colunas:")
    for m, ic in ic_por_tamanho(cifrado, 10):
        print("   m = %2d  IC = %.3f %s" % (m, ic, "<- volta a parecer português" if ic > 0.06 else ""))

    chave, texto = quebrar_vigenere(cifrado)
    print("\n3) cada coluna é um César, quebra por frequência -> chave = %s" % chave)
    print("   %s..." % texto[:70])

    print("\n--- Hill: é tudo linear (ataque de texto conhecido) ---")
    k = [[3, 3], [2, 5]]
    cifrado = hill.cifrar(MENSAGEM, k)
    print("interceptado: %s" % cifrado)
    print("o atacante sabe que as mensagens começam com 'TRANSF'")
    print("(com só 'TRAN' não dá: a matriz [[T, A], [R, N]] tem det = 13, sem inversa)")
    achada = hill.ataque_texto_conhecido("TRANSF", cifrado[:6])
    print("  K = C * P^-1 (mod 26) = %s" % achada)
    print("  decifrando o resto: %s" % hill.decifrar(cifrado, achada))

    print("\n--- Fluxo: a mesma chave usada em duas mensagens ---")
    outra = "PAGAR FORNECEDOR ATE SEXTA FEIRA HOJE"
    c1 = fluxo.cifrar(MENSAGEM, 40213)
    c2 = fluxo.cifrar(outra, 40213)
    print("C1 xor C2 = P1 xor P2; quem conhece P1 lê P2 sem a chave:")
    print("  %s" % reuso_de_fluxo(c1, c2, MENSAGEM))

    print("\nsó o one-time pad resiste, e só se a chave nunca for reutilizada")


def interativo():
    texto = ler_texto("texto longo (vazio = contrato): ", CONTRATO)
    chave = ler_texto("chave da Vigenère: ", "SEGREDO")
    cifrado = vigenere.cifrar(texto, chave)
    print("\ncifrado: %s..." % cifrado[:60])
    achada, decifrado = quebrar_vigenere(cifrado)
    print("chave encontrada: %s" % achada)
    print("texto: %s..." % decifrado[:60])
    if achada != "".join(c for c in chave.upper() if c.isalpha()):
        print("(errou? com texto curto a análise de frequência não tem letra suficiente)")


if __name__ == "__main__":
    main()
