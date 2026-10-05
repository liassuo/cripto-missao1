import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_classica import cesar, vigenere, transposicao, substituicao
from securedocs_classica.frequencia import (histograma, indice_coincidencia, ranking,
                                            ranking_portugues, IC_PORTUGUES, IC_ALEATORIO)
from securedocs_classica.criptoanalise import identificar_cifra, chute_substituicao, letras_certas
from textos import CONTRATO


def main():
    print("=== 10. ANÁLISE DE FREQUÊNCIA (Al-Kindi, séc. IX) ===\n")

    print("letras mais comuns no português: %s" % "".join(ranking_portugues()[:8]))
    print("letras mais comuns no contrato : %s" % "".join(ranking(CONTRATO)[:8]))

    cifrado = cesar.cifrar(CONTRATO, 7)
    print("\nhistograma do contrato cifrado com César (k = 7):")
    for linha in histograma(cifrado, 30):
        print(linha)
    print("o pico que devia estar no A está no H: H - A = 7 = a chave")

    print("\n--- substituição: 26! chaves, mas a frequência continua a mesma ---")
    cifrado = substituicao.cifrar(CONTRATO, substituicao.chave_aleatoria())
    _, chute = chute_substituicao(cifrado)
    certas, total = letras_certas(chute, CONTRATO)
    print("cifrado (começo)             : %s..." % cifrado[:60])
    print("chute só pela ordem das letras: %s..." % chute[:60])
    print("letras certas: %d de %d (%.0f%%); o resto sai testando palavras (DE, QUE, PARA)"
          % (certas, total, 100.0 * certas / total))

    print("\n--- transposição: as letras são as mesmas, só mudam de lugar ---")
    cifrado = transposicao.cifrar(CONTRATO, "CHAVE")
    print("mais comuns no original: %s" % "".join(ranking(CONTRATO)[:6]))
    print("mais comuns no cifrado : %s" % "".join(ranking(cifrado)[:6]))

    print("\n--- índice de coincidência (chance de duas letras sorteadas serem iguais) ---")
    print("  português ~ %.3f | aleatório ~ %.3f" % (IC_PORTUGUES, IC_ALEATORIO))
    print("  %-14s IC = %.3f" % ("texto claro", indice_coincidencia(CONTRATO)))
    print("  %-14s IC = %.3f" % ("César", indice_coincidencia(cesar.cifrar(CONTRATO, 7))))
    print("  %-14s IC = %.3f" % ("Vigenère", indice_coincidencia(vigenere.cifrar(CONTRATO, "SEGREDO"))))

    print("\nsó olhando o cifrado já dá para chutar o tipo de cifra:")
    amostras = [
        ("César", cesar.cifrar(CONTRATO, 7)),
        ("transposição", transposicao.cifrar(CONTRATO, "CHAVE")),
        ("Vigenère", vigenere.cifrar(CONTRATO, "SEGREDO")),
    ]
    for nome, c in amostras:
        ic, q, tipo = identificar_cifra(c)
        print("  (era %-12s) IC = %.3f -> %s" % (nome, ic, tipo))


def interativo():
    texto = ler_texto("cole um texto (claro ou cifrado): ", CONTRATO)
    for linha in histograma(texto, 30):
        print(linha)
    ic, q, tipo = identificar_cifra(texto)
    print("\nIC = %.3f | qui-quadrado = %.1f" % (ic, q))
    print("palpite: %s" % tipo)


if __name__ == "__main__":
    main()
