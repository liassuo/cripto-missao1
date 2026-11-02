import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int
from securedocs_simetrica import comparacao as cp


def tabela():
    print("%-5s %-5s %-25s %-14s %-17s %s" % ("", "ano", "estrutura", "bloco (bits)",
                                             "chave (bits)", "rodadas"))
    for nome, ano, autor, estrutura, bloco, chave, rodadas, situacao in cp.CARACTERISTICAS:
        print("%-5s %-5d %-25s %-14s %-17s %s" % (nome, ano, estrutura, bloco, chave, rodadas))
    print("\nsituação hoje:")
    for nome, ano, autor, estrutura, bloco, chave, rodadas, situacao in cp.CARACTERISTICAS:
        print("  %-5s %s" % (nome, situacao))


def forca_bruta(por_segundo):
    print("tempo médio de força bruta testando %.0e chaves por segundo:" % por_segundo)
    for nome, bits in cp.BITS_EFETIVOS:
        print("  %-16s 2^%-3d -> %s" % (nome, bits,
                                        cp.formatar_tempo(cp.tempo_forca_bruta(bits, por_segundo))))
    print("  (idade do universo: ~1.4e10 anos)")


def main():
    print("=== 6. COMPARAÇÃO: DES x RC5 x AES ===\n")
    tabela()

    print()
    forca_bruta(1e12)

    print("\nvelocidade da NOSSA implementação em Python (cifrando 8 KB):")
    cifras = cp.cifras_padrao()
    for cifra in cifras:
        print("  %-13s %8.1f KB/s" % (cifra.nome, cp.medir_velocidade(cifra) / 1024))
    print("  (em Python puro; com instruções AES-NI do processador o AES passa de 1 GB/s)")

    print("\nefeito avalanche: troca 1 bit do texto claro, quantos bits do cifrado mudam?")
    for cifra in cifras:
        media, total = cp.avalanche_medio(cifra)
        print("  %-13s %5.1f de %3d bits (%.0f%%)" % (cifra.nome, media, total, 100 * media / total))
    print("  o ideal é ~50%: o cifrado não dá pista de quão perto o chute está")

    print("\nESCOLHA PARA O SECUREDOCS: AES-256 (modo CBC)")
    print("  - DES: chave de 56 bits cai por força bruta em horas;")
    print("  - 3DES: seguro na chave, mas lento e com bloco de 64 bits (Sweet32);")
    print("  - RC5: rápido e flexível, mas não é padrão, teve patente até 2015 e quase")
    print("    nenhuma biblioteca ou hardware dá suporte;")
    print("  - AES: padrão do NIST desde 2001, bloco de 128 bits, chave de até 256 bits,")
    print("    sem ataque prático, aceleração em hardware em todo processador atual;")
    print("  - 256 bits porque o algoritmo de Grover (computador quântico) corta a")
    print("    segurança pela metade: 256 -> 128 bits ainda é seguro (ameaça futura).")


def interativo():
    print("quantas chaves por segundo o atacante testa? (expoente de 10)")
    e = ler_int("10^", 1, 30)
    print()
    forca_bruta(10 ** e)


if __name__ == "__main__":
    main()
