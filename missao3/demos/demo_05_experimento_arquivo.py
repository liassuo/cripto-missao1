import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_texto
from securedocs_simetrica import arquivo
from securedocs_simetrica.blocos import para_hex
from textos import CONTRATO

def area_de_trabalho():
    # pergunta ao Windows onde fica a Área de Trabalho (pode estar dentro do OneDrive)
    try:
        import ctypes
        caminho = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, caminho)   # 0x10 = Desktop
        if os.path.isdir(caminho.value):
            return caminho.value
    except (AttributeError, OSError):
        pass
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return desktop if os.path.isdir(desktop) else MISSAO


# os arquivos do experimento ficam na Área de Trabalho para abrir na hora da apresentação
PASTA = os.path.join(area_de_trabalho(), "SecureDocs_experimento")


def mostrar_inicio(caminho, n=48):
    with open(caminho, "rb") as f:
        dados = f.read(n)
    print("  %-26s %6d bytes | %s" % (os.path.basename(caminho), os.path.getsize(caminho),
                                       para_hex(dados[:24], 4)))
    texto = "".join(chr(b) if 32 <= b < 127 else "." for b in dados)
    print("  %-26s              | %s" % ("", texto))


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
    print("   salva em %s\n" % caminho_chave)

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

    print("\n4) o invasor copiou o .sdoc mas não tem a chave:")
    with open(cifrado, "rb") as f:
        roubado = f.read()
    try:
        lixo = arquivo.decifrar_dados(roubado, arquivo.gerar_chave(256))
        print("   chave errada -> saiu lixo: %s..." % para_hex(lixo[:16]))
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
    experimento(original)

    print("\n(arquivos gerados em %s)" % PASTA)


def interativo():
    caminho = ler_texto("caminho do arquivo (enter = contrato de exemplo): ")
    if not caminho:
        main()
        return
    # ao arrastar o arquivo para o terminal, o Windows pode colocar aspas ou "& '...'"
    if caminho.startswith("& "):
        caminho = caminho[2:]
    caminho = caminho.strip().strip('"').strip("'")
    if not os.path.isfile(caminho):
        print("arquivo não encontrado")
        return
    print()
    experimento(caminho)
    print("\n(arquivos gerados em %s)" % PASTA)


if __name__ == "__main__":
    main()
