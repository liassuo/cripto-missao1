import os
import runpy
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))

MISSOES = [
    ("Missão 1 - Precisamos de matemática (teoria dos números)", "missao1"),
    ("Missão 2 - A mensagem interceptada (criptografia clássica)", "missao2"),
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    while True:
        print()
        print("=" * 58)
        print(" SecureDocs - TechSecure")
        print("=" * 58)
        for i, (nome, _) in enumerate(MISSOES, 1):
            print("  %d - %s" % (i, nome))
        print("  0 - Sair")
        escolha = input("\nescolha: ").strip()

        if escolha == "0":
            break
        elif escolha.isdigit() and 1 <= int(escolha) <= len(MISSOES):
            pasta = os.path.join(PASTA, MISSOES[int(escolha) - 1][1])
            runpy.run_path(os.path.join(pasta, "main.py"), run_name="__main__")
        else:
            print("opção inválida")


if __name__ == "__main__":
    main()
