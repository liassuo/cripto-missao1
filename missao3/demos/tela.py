# Parte da tela que mostra a mensagem inteira, bloco por bloco (usada no DES e no RC5)

from securedocs_simetrica import modos
from securedocs_simetrica.blocos import para_hex, dividir_blocos, pkcs7_preencher


def texto_do_bloco(bloco):
    try:
        return "'%s'" % bloco.decode("utf-8")
    except UnicodeDecodeError:
        return para_hex(bloco)      # acento cortado no meio do bloco


def mostrar_mensagem_inteira(cifra, texto):
    n = cifra.tamanho_bloco
    dados = texto.encode("utf-8")
    iv, cifrado = modos.cifrar_cbc(cifra, dados)
    claros = dividir_blocos(pkcs7_preencher(dados, n), n)
    cifrados = dividir_blocos(cifrado, n)

    print("\nMENSAGEM INTEIRA (todos os blocos, modo CBC)")
    print("  texto claro : %s  (%d bytes -> %d %s de %d)"
          % (texto, len(dados), len(claros), "bloco" if len(claros) == 1 else "blocos", n))
    print("  IV          : %s  (aleatório, muda a cada vez)" % para_hex(iv))
    for i, (claro, cif) in enumerate(zip(claros, cifrados), 1):
        if i == len(claros):
            enchimento = claro[-1]
            claro = claro[:-enchimento]
            descricao = texto_do_bloco(claro) if claro else ""
            descricao += " + %d de enchimento" % enchimento
        else:
            descricao = texto_do_bloco(claro)
        print("  bloco %-5d : %-34s -> %s" % (i, descricao, para_hex(cif)))
    print("  decifrado   : %s" % modos.decifrar_cbc(cifra, cifrado, iv).decode("utf-8"))
