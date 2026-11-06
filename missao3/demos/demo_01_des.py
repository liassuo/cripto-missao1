import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_hex, ler_texto
from securedocs_simetrica import des, vetores
from securedocs_simetrica.blocos import para_hex, de_hex, bytes_para_int, int_para_bytes
from textos import MENSAGEM, CHAVE_DES
from tela import mostrar_mensagem_inteira


def binario(x, bits, grupo=0):
    # grupo separa os bits com espaço para ficar legível na tela
    texto = format(x, "0%db" % bits)
    if grupo:
        texto = " ".join(texto[i:i + grupo] for i in range(0, bits, grupo))
    return texto


def como_texto(bloco):
    # mostra os caracteres só quando dá para ler (acento conta 2 bytes em UTF-8)
    try:
        texto = bloco.decode("utf-8")
    except UnicodeDecodeError:
        return ""
    if texto.isprintable():
        return '"%s" = ' % texto
    return ""


def passo_subchaves(chave):
    print("PASSO 1 - as 16 subchaves (o schedule da chave)")
    k56 = des.permutar(bytes_para_int(chave), des.PC1, 64)
    c, d = k56 >> 28, k56 & 0xFFFFFFF
    print("  PC-1 tira os 8 bits de paridade (8, 16, ..., 64) e embaralha os 56 que sobram:")
    print("  PC-1(K) = C0D0 (28 + 28 bits)")
    linha = "  %-3s %-3s %-33s %-33s %s"
    print()
    print(linha % ("i", "LS", "Ci = LSi(Ci-1)", "Di = LSi(Di-1)", "Ki = PC-2(CiDi)"))
    print(linha % ("0", "", binario(c, 28, 7), binario(d, 28, 7), ""))
    for i, desloc in enumerate(des.DESLOCAMENTOS, 1):
        c, d = des.girar_28(c, desloc), des.girar_28(d, desloc)
        k = des.permutar((c << 28) | d, des.PC2, 56)
        print(linha % (i, desloc, binario(c, 28, 7), binario(d, 28, 7), "%012X" % k))
    print("  LS = deslocamento circular à esquerda: 1 posição nas rodadas 1, 2, 9 e 16 e")
    print("  2 nas outras. PC-2 escolhe 48 dos 56 bits. No total são 28 deslocamentos,")
    print("  então C16 e D16 voltam a ser iguais a C0 e D0.")


def passo_funcao_f(r, k):
    print("\n  dentro da f na rodada 1: f(R0, K1)")
    e = des.permutar(r, des.E, 32)
    x = e ^ k
    print("    R0                = %s  (32 bits)" % binario(r, 32, 4))
    print("    E(R0)             = %s  (48 bits)" % binario(e, 48, 6))
    print("    K1                = %s" % binario(k, 48, 6))
    print("    B = E(R0) xor K1  = %s" % binario(x, 48, 6))
    print("                          B1     B2     B3     B4     B5     B6     B7     B8")
    print("    E repete 16 bits para chegar a 48. Em cada Bj, b1b6 dá a linha e b2b3b4b5 a coluna:")
    saida = 0
    for j in range(8):
        seis = (x >> (42 - 6 * j)) & 0x3F
        linha = ((seis >> 4) & 0b10) | (seis & 1)
        coluna = (seis >> 1) & 0xF
        valor = des.SBOX[j][linha][coluna]
        saida = (saida << 4) | valor
        print("      B%d = %s -> S%d(linha %d, coluna %2d) = %2d = %s"
              % (j + 1, binario(seis, 6), j + 1, linha, coluna, valor, binario(valor, 4)))
    f = des.permutar(saida, des.P, 32)
    print("    C = C1...C8       = %s  (32 bits)" % binario(saida, 32, 4))
    print("    f = P(C)          = %s  = %08X" % (binario(f, 32, 4), f))


def rodadas(x0, chaves, nomes):
    esq, dir_ = x0 >> 32, x0 & 0xFFFFFFFF
    linha = "  %-3s %-19s %-13s %-12s %s"
    print()
    print(linha % ("i", "subchave", "f(Ri-1, Ki)", "Li = Ri-1", "Ri = Li-1 xor f"))
    print(linha % ("0", "", "", "%08X" % esq, "%08X" % dir_))
    for i, k in enumerate(chaves, 1):
        f = des.funcao_f(dir_, k)
        esq, dir_ = dir_, esq ^ f
        print(linha % (i, "%-3s = %012X" % (nomes[i - 1], k), "%08X" % f, "%08X" % esq, "%08X" % dir_))
    return esq, dir_


def passo_fim(esq, dir_):
    junto = (dir_ << 32) | esq
    saida = int_para_bytes(des.permutar(junto, des.FP, 64), 8)
    print("    swap das metades: R16L16 = %016X" % junto)
    print("    IP^-1(R16L16)          = %s" % para_hex(saida))
    return saida


def mostrar_rodadas(bloco, chave):
    cifra = des.Cifra(chave)
    print("texto claro x: %s%s (8 bytes = 64 bits)" % (como_texto(bloco), para_hex(bloco)))
    print("chave K      : %s (64 bits = 16 dígitos hex)\n" % para_hex(chave))

    passo_subchaves(chave)

    print("\nPASSO 2 - permutação inicial: x0 = IP(x) = L0R0")
    x0 = des.permutar(bytes_para_int(bloco), des.IP, 64)
    print("  IP(x) = %016X    L0 = %08X (32 bits)    R0 = %08X (32 bits)"
          % (x0, x0 >> 32, x0 & 0xFFFFFFFF))

    print("\nPASSO 3 - as 16 rodadas de Feistel: Li = Ri-1  e  Ri = Li-1 xor f(Ri-1, Ki)")
    passo_funcao_f(x0 & 0xFFFFFFFF, cifra.chaves[0])
    nomes = ["K%d" % i for i in range(1, 17)]
    esq, dir_ = rodadas(x0, cifra.chaves, nomes)
    print("  (o R de uma linha vira o L da linha de baixo)")
    print("  por que 16 rodadas? com menos rodadas a criptoanálise diferencial quebra o DES")
    print("  mais rápido que a força bruta; com 16 ela já não compensa")

    print("\nPASSO 4 - fim: y = IP^-1(R16L16)")
    cifrado = passo_fim(esq, dir_)
    print("  texto cifrado y = %s" % para_hex(cifrado))

    print("\nPASSO 5 - decifrar: o mesmo algoritmo, com y na entrada e as subchaves de K16 até K1")
    y0 = des.permutar(bytes_para_int(cifrado), des.IP, 64)
    esq, dir_ = rodadas(y0, cifra.chaves[::-1], nomes[::-1])
    decifrado = passo_fim(esq, dir_)
    print("  texto decifrado = %s%s (voltou ao texto claro)" % (como_texto(decifrado), para_hex(decifrado)))
    print("  a f nunca precisa ser invertida: o xor com o mesmo valor desfaz o anterior")
    return cifra


def main():
    print("=== 1. DES (Data Encryption Standard) ===\n")
    print("estrutura de Feistel: bloco de 64 bits, chave de 64 bits (8 são de paridade,")
    print("sobram 56 que contam de verdade) e 16 rodadas\n")

    cifra = mostrar_rodadas(de_hex("0123456789ABCDEF"), de_hex(CHAVE_DES))

    print("\nvetores de teste:")
    for nome, chave, claro, esperado, obtido, fonte, ok in vetores.conferir("DES"):
        print("  %s  chave %s  P = %s -> %s  %s" % (nome, chave, claro, obtido,
                                                   "OK" if ok else "ERRO"))

    mostrar_mensagem_inteira(cifra, MENSAGEM)

    print("\nproblema: 2^56 = %d chaves. Em 1998 a máquina Deep Crack da EFF" % 2 ** 56)
    print("achou uma chave em 56 horas.")


def interativo():
    dados = ler_texto("texto claro (8 caracteres): ", "SEGREDO!").encode("utf-8")
    if len(dados) > 8:
        print("  o texto tem %d bytes (letra com acento ocupa 2); o bloco usa só os 8 primeiros"
              % len(dados))
    bloco = dados[:8].ljust(8, b" ")
    chave = ler_hex("chave (16 dígitos hex): ", 8, CHAVE_DES)
    print()
    cifra = mostrar_rodadas(bloco, chave)

    texto = ler_texto("\nmensagem inteira: ", MENSAGEM)
    mostrar_mensagem_inteira(cifra, texto)


if __name__ == "__main__":
    main()
