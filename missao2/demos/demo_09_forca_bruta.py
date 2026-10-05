import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int, ler_texto
from securedocs_classica import cesar, afim, fluxo, substituicao
from securedocs_classica.criptoanalise import ranking_cesar, quebrar_afim, quebrar_semente
from textos import MENSAGEM


def main():
    print("=== 9. FORÇA BRUTA ===\n")
    print("o invasor não sabe a chave, então testa todas\n")

    cifrado = cesar.cifrar(MENSAGEM, 3)
    print("--- César: só 25 chaves ---")
    print("interceptado: %s" % cifrado)
    for k, texto in cesar.forca_bruta(cifrado)[:6]:
        print("  k = %2d: %s" % (k, texto))
    print("  ... (mais 19 tentativas)")

    print("\nnem precisa ler as 25: o qui-quadrado compara com o português")
    print("(quanto menor, mais parece português)")
    for k, q, texto in ranking_cesar(cifrado, 3):
        print("  k = %2d  qui-quadrado = %7.1f  %s" % (k, q, texto))

    print("\n--- Afim: 312 chaves ---")
    cifrado = afim.cifrar(MENSAGEM, 5, 8)
    print("interceptado: %s" % cifrado)
    chave, texto = quebrar_afim(cifrado)
    print("achou (a, b) = %s: %s" % (chave, texto))

    print("\n--- Fluxo com semente de 16 bits: 65536 chaves ---")
    cifrado = fluxo.cifrar(MENSAGEM, 40213)
    print("interceptado: %s..." % fluxo.para_hex(cifrado)[:40])
    print("sabendo só que a mensagem começa com 'TRANSF'...")
    semente = quebrar_semente(cifrado, "TRANSF")
    print("achou a semente %d: %s" % (semente, fluxo.decifrar(cifrado, semente)))

    print("\n--- Substituição: 26! chaves ---")
    print("26! = %.1e -> testando 1 bilhão por segundo levaria ~10^10 anos"
          % substituicao.tamanho_espaco_chaves())
    print("força bruta não funciona aqui... mas a análise de frequência sim (opção 10)")


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    k = ler_int("chave do César (1 a 25): ", 1, 25)
    cifrado = cesar.cifrar(texto, k)
    print("\ninterceptado: %s" % cifrado)
    print("testando as 25 chaves, as 3 que mais parecem português:")
    for chave, q, decifrado in ranking_cesar(cifrado, 3):
        print("  k = %2d  qui-quadrado = %7.1f  %s" % (chave, q, decifrado))


if __name__ == "__main__":
    main()
