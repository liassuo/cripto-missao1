import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_classica import cesar, substituicao, afim, vigenere, hill, transposicao, fluxo
from securedocs_classica.alfabeto import so_letras

from textos import MENSAGEM


def cifrar_com_todas(texto):
    chave_sub = substituicao.chave_por_palavra("SEGURANCA")
    chave_otp = fluxo.chave_vernam(len(so_letras(texto)))
    return [
        ("César (k = 3)", cesar.cifrar(texto, 3)),
        ("Afim (a = 5, b = 8)", afim.cifrar(texto, 5, 8)),
        ("Substituição (SEGURANCA)", substituicao.cifrar(texto, chave_sub)),
        ("Vigenère (SEGREDO)", vigenere.cifrar(texto, "SEGREDO")),
        ("Hill 2x2 [[3,3],[2,5]]", hill.cifrar(texto, [[3, 3], [2, 5]])),
        ("Transposição (CHAVE)", transposicao.cifrar(texto, "CHAVE")),
        ("Cerca de trilhos (3)", transposicao.cerca_cifrar(texto, 3)),
        ("Fluxo (semente 40213)", fluxo.para_hex(fluxo.cifrar(texto, 40213))[:36] + "..."),
        ("One-time pad", fluxo.vernam_cifrar(texto, chave_otp)),
    ]


def main():
    print("=== 8. A MENSAGEM INTERCEPTADA COM CADA TÉCNICA ===\n")
    print("mensagem original: %s\n" % MENSAGEM)
    for nome, cifrado in cifrar_com_todas(MENSAGEM):
        print("%-26s %s" % (nome, cifrado))


def interativo():
    texto = ler_texto("mensagem: ", MENSAGEM)
    print()
    for nome, cifrado in cifrar_com_todas(texto):
        print("%-26s %s" % (nome, cifrado))


if __name__ == "__main__":
    main()
