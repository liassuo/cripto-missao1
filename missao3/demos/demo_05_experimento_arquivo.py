import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_simetrica import arquivo
from securedocs_simetrica.blocos import para_hex
from textos import CONTRATO

PASTA = os.path.join(MISSAO, "experimento")


def mostrar_inicio(caminho, n=48):
    with open(caminho, "rb") as f:
        dados = f.read(n)
    print("  %-26s %6d bytes | %s" % (os.path.basename(caminho), os.path.getsize(caminho),
                                       para_hex(dados[:24], 4)))
    texto = "".join(chr(b) if 32 <= b < 127 else "." for b in dados)
    print("  %-26s              | %s" % ("", texto))


def conferir_com_openssl(cifrado, chave, original):
    # prova extra: a biblioteca cryptography (OpenSSL) abre o arquivo que nós ciframos
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding
    except ImportError:
        print("  (biblioteca cryptography não instalada, conferência pulada)")
        return
    with open(cifrado, "rb") as f:
        conteudo = f.read()
    d = Cipher(algorithms.AES(chave), modes.CBC(conteudo[6:22])).decryptor()
    u = padding.PKCS7(128).unpadder()
    dados = u.update(d.update(conteudo[22:]) + d.finalize()) + u.finalize()
    with open(original, "rb") as f:
        print("  OpenSSL decifrou o nosso arquivo e bateu com o original: %s"
              % ("SIM" if dados == f.read() else "NÃO"))


def experimento(original):
    os.makedirs(PASTA, exist_ok=True)
    nome = os.path.basename(original)
    cifrado = os.path.join(PASTA, nome + ".sdoc")
    nome_base, ext = os.path.splitext(nome)
    decifrado = os.path.join(PASTA, nome_base + "_decifrado" + ext)
    caminho_chave = os.path.join(PASTA, "chave_" + nome_base + ".txt")

    chave = arquivo.gerar_chave(256)
    arquivo.salvar_chave(caminho_chave, chave)
    print("1) chave AES-256 sorteada (secrets): %s" % para_hex(chave, 4))
    print("   salva em %s\n" % os.path.relpath(caminho_chave, MISSAO))

    print("2) arquivo original -> AES -> arquivo cifrado")
    arquivo.cifrar_arquivo(original, cifrado, chave)
    mostrar_inicio(original)
    mostrar_inicio(cifrado)
    print("   cabeçalho: SDOC | versão | tamanho da chave | IV (16 bytes) | blocos AES-CBC\n")

    print("3) arquivo cifrado -> AES -> arquivo original")
    arquivo.decifrar_arquivo(cifrado, decifrado, arquivo.ler_chave(caminho_chave))
    mostrar_inicio(decifrado)
    print("\n   decifrado idêntico ao original, byte a byte? %s"
          % ("SIM" if arquivo.arquivos_iguais(original, decifrado) else "NÃO"))
    conferir_com_openssl(cifrado, chave, original)

    print("\n4) o invasor copiou o .sdoc mas não tem a chave:")
    try:
        arquivo.decifrar_arquivo(cifrado, os.path.join(PASTA, "tentativa.bin"),
                                 arquivo.gerar_chave(256))
        print("   saiu lixo")
    except ValueError as erro:
        print("   chave errada -> %s" % erro)
    return cifrado, chave


def main():
    print("=== 5. EXPERIMENTO: CIFRAR UM ARQUIVO COM AES ===\n")
    print("arquivo original -> AES -> arquivo cifrado -> AES -> arquivo original\n")

    os.makedirs(PASTA, exist_ok=True)
    original = os.path.join(PASTA, "contrato.txt")
    with open(original, "w", encoding="utf-8") as f:
        f.write(CONTRATO + "\n")
    cifrado, chave = experimento(original)

    print("\n5) e se o invasor alterar 1 byte do arquivo cifrado?")
    with open(cifrado, "rb") as f:
        conteudo = bytearray(f.read())
    conteudo[22 + 20] ^= 0x01        # um bit do segundo bloco
    try:
        alterado = arquivo.decifrar_dados(bytes(conteudo), chave).decode("utf-8", "replace")
        print("   %s..." % alterado[:70])
        print("   o AES decifrou sem reclamar: o bloco ficou corrompido e o seguinte teve 1 bit")
        print("   trocado. Sigilo não garante integridade - isso fica para a próxima missão (hash/MAC).")
    except ValueError as erro:
        print("   %s" % erro)


def interativo():
    caminho = ler_texto("caminho do arquivo (enter = contrato de exemplo): ")
    if not caminho:
        main()
        return
    caminho = caminho.strip('"')
    if not os.path.isfile(caminho):
        print("arquivo não encontrado")
        return
    print()
    experimento(caminho)
    print("\n(arquivos gerados em %s)" % PASTA)


if __name__ == "__main__":
    main()
