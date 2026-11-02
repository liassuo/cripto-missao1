import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from missao2.securedocs_classica import vigenere
from missao2.securedocs_classica.criptoanalise import quebrar_vigenere, letras_certas
from missao2.securedocs_classica.frequencia import indice_coincidencia
from securedocs_simetrica import arquivo
from textos import CONTRATO


def frequencia_bytes(dados):
    contagem = [0] * 256
    for b in dados:
        contagem[b] += 1
    usados = sum(1 for c in contagem if c)
    return usados, max(contagem)


def roubo(documento, chave_vigenere):
    print("--- servidor ANTIGO: arquivo cifrado com Vigenère (Missão 2) ---")
    cifrado = vigenere.cifrar(documento, chave_vigenere)
    print("o invasor copiou: %s..." % cifrado[:60])
    print("IC = %.3f (português ~0.072, aleatório ~0.038): é polialfabética"
          % indice_coincidencia(cifrado))
    chave, texto = quebrar_vigenere(cifrado)
    print("ataque da Missão 2 (IC + qui-quadrado) -> chave %s" % chave)
    print("  %s..." % texto[:70])
    certas, total = letras_certas(texto, documento)
    print("  %d de %d letras recuperadas" % (certas, total))

    print("\n--- servidor NOVO: o mesmo arquivo cifrado com AES-256 ---")
    chave_aes = arquivo.gerar_chave(256)
    roubado = arquivo.cifrar_dados(documento.encode("utf-8"), chave_aes)
    print("o invasor copiou: %s..." % roubado[22:52].hex().upper())
    usados, maior = frequencia_bytes(roubado[22:])
    print("bytes diferentes que aparecem: %d de 256, o mais frequente aparece %d vezes"
          % (usados, maior))
    print("a frequência é praticamente plana: não sobra estatística do português")

    print("\no mesmo contrato cifrado de novo com a MESMA chave:")
    outro = arquivo.cifrar_dados(documento.encode("utf-8"), chave_aes)
    print("  1a vez: %s..." % roubado[22:46].hex().upper())
    print("  2a vez: %s..." % outro[22:46].hex().upper())
    print("  (IV diferente: nem dá para saber que é o mesmo documento)")

    print("\nsem a chave sobra a força bruta: 2^256 ~ %.1e chaves" % 2 ** 256)
    try:
        arquivo.decifrar_dados(roubado, arquivo.gerar_chave(256))
        print("chute aleatório: saiu lixo")
    except ValueError:
        print("chute aleatório: enchimento inválido, saiu lixo")


def main():
    print("=== 7. OS DOCUMENTOS ROUBADOS: CLÁSSICA x AES ===\n")
    print("o invasor copiou os arquivos do servidor. O que ele consegue ler?\n")
    roubo(CONTRATO, "TECHSECURE")
    print("\nconclusão: com AES, copiar o arquivo não adianta. O segredo agora é")
    print("só a chave - e ela não pode ficar no mesmo servidor que os arquivos.")


def interativo():
    texto = ler_texto("documento: ", CONTRATO)
    chave = ler_texto("chave do Vigenère: ", "TECHSECURE")
    print()
    roubo(texto, chave)


if __name__ == "__main__":
    main()
