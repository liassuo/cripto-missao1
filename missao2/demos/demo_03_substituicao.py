import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_classica import substituicao
from securedocs_classica.alfabeto import ALFABETO, normalizar, so_letras
from textos import MENSAGEM


def chave_marcada(chave, n):
    # └─PALAVRA─┘ └── resto do alfabeto ──┘ embaixo das letras (cada letra ocupa 2 colunas)
    def trecho(letras, rotulo):
        largura = 2 * len(letras) - 1
        if largura < 3:
            return "^" * largura
        if len(rotulo) > largura - 2:
            rotulo = ""
        return "└" + rotulo.center(largura - 2, "─") + "┘"

    return trecho(chave[:n], chave[:n]) + " " + trecho(chave[n:], " resto do alfabeto ")


def mostrar(texto, chave, origem, palavra=""):
    print("cada letra vira outra, seguindo uma permutação do alfabeto (a chave)\n")

    print("chave %s:" % origem)
    print("  claro: %s" % " ".join(ALFABETO))
    print("  cifra: %s" % " ".join(chave))
    if palavra:
        n = len(set(so_letras(palavra)))
        print("         %s" % chave_marcada(chave, n))

    cifrado = substituicao.cifrar(texto, chave)
    print("\ntexto claro: %s" % normalizar(texto))
    print("cifrado    : %s" % cifrado)
    print("decifrado  : %s" % substituicao.decifrar(cifrado, chave))


def main():
    print("=== 3. SUBSTITUIÇÃO MONOALFABÉTICA ===\n")
    mostrar(MENSAGEM, substituicao.chave_por_palavra("SEGURANCA"), "a partir da palavra SEGURANCA",
            "SEGURANCA")

    print("\ntambém dá para gerar a chave aleatória:")
    print("  %s" % substituicao.chave_aleatoria())
    print("\nquantidade de chaves possíveis: 26! = %d" % substituicao.tamanho_espaco_chaves())


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    while True:
        palavra = ler_texto("palavra-chave (vazio = chave aleatória): ", "")
        if not palavra:
            break
        if not so_letras(palavra):
            print("  a palavra-chave precisa ter letras (ex.: SEGURANCA)")
        elif substituicao.chave_por_palavra(palavra) == ALFABETO:
            print("  essa palavra não muda nada (a tabela fica igual ao alfabeto), escolha outra")
        else:
            break
    print()
    if palavra:
        mostrar(texto, substituicao.chave_por_palavra(palavra),
                "a partir da palavra %s" % so_letras(palavra), palavra)
    else:
        mostrar(texto, substituicao.chave_aleatoria(), "aleatória")


if __name__ == "__main__":
    main()
