import os
import random
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from securedocs_classica import cesar, afim, vigenere, substituicao
from securedocs_classica.frequencia import qui_quadrado
from securedocs_classica.criptoanalise import (identificar_cifra, quebrar_cesar, quebrar_afim,
                                               quebrar_vigenere)
from textos import CONTRATO


def atacante(cifrado):
    ic, q, tipo = identificar_cifra(cifrado)
    print("  IC = %.3f -> %s" % (ic, tipo))
    tentativas = [
        ("César", lambda: quebrar_cesar(cifrado)),
        ("afim", lambda: quebrar_afim(cifrado)),
        ("Vigenère", lambda: quebrar_vigenere(cifrado)),
    ]
    melhor = None
    for nome, ataque in tentativas:
        chave, texto = ataque()
        nota = qui_quadrado(texto)
        print("  tentando %-9s chave = %-10s qui-quadrado = %8.1f" % (nome, chave, nota))
        if melhor is None or nota < melhor[0]:
            melhor = (nota, nome, chave, texto)
    return melhor


def main():
    print("=== 12. PRINCÍPIO DE KERCKHOFFS ===\n")
    print("\"O sistema não deve exigir segredo e pode cair nas mãos do inimigo")
    print(" sem inconveniente\" (Kerckhoffs, 1883)\n")

    escolhas = [
        ("César", lambda t: cesar.cifrar(t, 19)),
        ("afim", lambda t: afim.cifrar(t, 11, 4)),
        ("Vigenère", lambda t: vigenere.cifrar(t, "TECHSECURE")),
    ]
    nome, cifra = random.choice(escolhas)
    cifrado = cifra(CONTRATO)
    print("a TechSecure escolheu um algoritmo 'secreto' e cifrou o contrato.")
    print("o atacante interceptou: %s...\n" % cifrado[:60])

    nota, achou, chave, texto = atacante(cifrado)
    print("\nresultado: era %s com chave %s" % (achou, chave))
    print("  %s..." % texto[:70])
    print("(algoritmo realmente usado: %s)" % nome)

    print("\nconclusão:")
    print("  - esconder o algoritmo só atrasou o atacante alguns milissegundos;")
    print("  - o que protegeria é uma CHAVE com espaço grande E uma cifra sem padrão;")
    print("  - substituição tem 26! = %.1e chaves e mesmo assim cai por frequência,"
          % substituicao.tamanho_espaco_chaves())
    print("    então chave grande não basta: a cifra não pode vazar a estatística do texto;")
    print("  - algoritmo público (AES, RSA) é analisado por todo mundo; o segredo fica só na chave.")


def interativo():
    main()


if __name__ == "__main__":
    main()
