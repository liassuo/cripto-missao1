import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_hex, ler_texto
from securedocs_simetrica import des, modos, vetores
from securedocs_simetrica.blocos import para_hex, de_hex
from textos import MENSAGEM, CHAVE_DES


def mostrar_rodadas(bloco, chave):
    cifra = des.Cifra(chave)
    print("bloco claro: %s   chave: %s" % (para_hex(bloco), para_hex(chave)))
    print("\nsubchaves (48 bits cada, saem da chave por PC-1, rotações e PC-2):")
    for i, k in enumerate(cifra.chaves[:3], 1):
        print("  K%-2d = %012X" % (i, k))
    print("  ... (16 subchaves no total)")

    passos = []
    cifrado = cifra.cifrar_bloco(bloco, passos)
    print("\nrodada   L(i)       R(i) = L(i-1) xor f(R(i-1), K(i))")
    for i, esq, dir_, k in passos:
        print("  %2d     %08X   %08X" % (i, esq, dir_))
    print("\ncifrado  : %s  (depois de juntar R16 L16 e aplicar IP^-1)" % para_hex(cifrado))
    print("decifrado: %s  (mesmas rodadas, subchaves de K16 até K1)"
          % para_hex(cifra.decifrar_bloco(cifrado)))
    return cifra


def main():
    print("=== 1. DES (Data Encryption Standard) ===\n")
    print("cifra de Feistel: bloco de 64 bits, chave de 56 bits, 16 rodadas")
    print("L(i) = R(i-1)   e   R(i) = L(i-1) xor f(R(i-1), K(i))\n")

    cifra = mostrar_rodadas(de_hex("0123456789ABCDEF"), de_hex(CHAVE_DES))

    print("\nvetores de teste:")
    for nome, chave, claro, esperado, obtido, fonte, ok in vetores.conferir("DES"):
        print("  %s  chave %s  P = %s -> %s  %s" % (nome, chave, claro, obtido,
                                                   "OK" if ok else "ERRO"))

    print("\na mensagem inteira (modo CBC, vários blocos de 8 bytes):")
    iv, cifrado = modos.cifrar_cbc(cifra, MENSAGEM.encode("utf-8"))
    print("  IV       : %s" % para_hex(iv))
    print("  cifrado  : %s" % para_hex(cifrado, 8))
    print("  decifrado: %s" % modos.decifrar_cbc(cifra, cifrado, iv).decode("utf-8"))

    print("\nchave fraca 0101010101010101: as 16 subchaves saem iguais,")
    fraca = des.Cifra(de_hex(des.CHAVES_FRACAS[0]))
    duas_vezes = fraca.cifrar_bloco(fraca.cifrar_bloco(b"SEGREDO!"))
    print("  então cifrar duas vezes devolve o texto: %s" % duas_vezes.decode())

    print("\n3DES (E-D-E com 3 chaves) - remendo para o tamanho de chave do DES:")
    tripla = des.CifraTripla(de_hex(CHAVE_DES + "0E329232EA6D0D73" + "0123456789ABCDEF"))
    c = tripla.cifrar_bloco(b"SEGREDO!")
    print("  SEGREDO! -> %s -> %s" % (para_hex(c), tripla.decifrar_bloco(c).decode()))
    print("  3 vezes mais lento que o DES e o bloco continua com 64 bits")

    print("\nproblema: 2^56 = %d chaves. Em 1998 a máquina Deep Crack da EFF" % 2 ** 56)
    print("achou uma chave em 56 horas.")


def interativo():
    bloco = ler_texto("bloco (8 caracteres): ", "SEGREDO!").encode("utf-8")[:8].ljust(8, b" ")
    chave = ler_hex("chave (16 dígitos hex): ", 8, CHAVE_DES)
    print()
    cifra = mostrar_rodadas(bloco, chave)

    texto = ler_texto("\nmensagem inteira: ", MENSAGEM)
    iv, cifrado = modos.cifrar_cbc(cifra, texto.encode("utf-8"))
    print("cifrado (CBC): %s" % para_hex(cifrado, 8))
    print("decifrado    : %s" % modos.decifrar_cbc(cifra, cifrado, iv).decode("utf-8"))


if __name__ == "__main__":
    main()
