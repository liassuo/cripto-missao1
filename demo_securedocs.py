import sys
import time

from entrada import ler_int
from securedocs_math import (coprimos, exp_mod, gerar_primo, inverso_multiplicativo,
                             phi_de_primos, pollard_rho, tcr)


def gerar_chaves(bits=512):
    p = gerar_primo(bits // 2)
    q = gerar_primo(bits // 2)
    while q == p:
        q = gerar_primo(bits // 2)

    n = p * q
    phi_n = phi_de_primos(p, q)

    e = 65537  # valor padrão usado na prática
    while not coprimos(e, phi_n):
        e += 2
    d = inverso_multiplicativo(e, phi_n)
    return (e, n), (d, n), (p, q)


def texto_para_int(texto):
    return int.from_bytes(texto.encode(), "big")


def int_para_texto(numero):
    tamanho = (numero.bit_length() + 7) // 8
    return numero.to_bytes(tamanho, "big").decode()


def demo_confidencialidade():
    print("\n=== 1. CONFIDENCIALIDADE (mensagem em texto claro) ===\n")
    (e, n), (d, _), _ = gerar_chaves(512)
    print("n =", str(n)[:50] + "...", "(%d bits, público)" % n.bit_length())
    print("e =", e, "(público)")
    print("d =", str(d)[:50] + "...", "(privado)")

    msg = "Contrato 4471 - valor confidencial"
    m = texto_para_int(msg)
    c = exp_mod(m, e, n)   # cifra com a chave pública
    m2 = exp_mod(c, d, n)  # decifra com a privada

    print("\noriginal :", msg)
    print("cifrado  :", str(c)[:60] + "...")
    print("decifrado:", int_para_texto(m2))
    print("confere?", int_para_texto(m2) == msg)
    print("\n(funciona por causa do teorema de Euler: m^(e*d) = m^(1 + k*phi(n)) = m mod n)")


def demo_assinatura():
    print("\n=== 2. AUTENTICIDADE / INTEGRIDADE / NÃO REPÚDIO (assinatura) ===\n")
    (e, n), (d, _), _ = gerar_chaves(512)

    documento = "Contrato 4471: prazo de 12 meses, valor fixo."
    # por enquanto o "resumo" é o próprio texto virado número; na missão de hash vira SHA-256
    resumo = texto_para_int(documento) % n

    assinatura = exp_mod(resumo, d, n)      # só quem tem d consegue
    verificado = exp_mod(assinatura, e, n)  # qualquer um confere com e

    print("documento :", documento)
    print("assinatura:", str(assinatura)[:60] + "...")
    print("assinatura bate com o documento?", verificado == resumo)

    adulterado = "Contrato 4471: prazo de 24 meses, valor fixo."
    resumo_adulterado = texto_para_int(adulterado) % n
    print("\ndocumento adulterado:", adulterado)
    print("assinatura ainda bate?", verificado == resumo_adulterado)
    print("-> é o caso do cliente que recebeu o contrato diferente")


def demo_ataque():
    print("\n=== 3. ATAQUE: chave pequena cai ===\n")
    for bits in (32, 48, 64, 80):
        (e, n), (d, _), _ = gerar_chaves(bits)
        inicio = time.time()
        fator = pollard_rho(n)
        tempo = time.time() - inicio
        outro = n // fator
        d_atacante = inverso_multiplicativo(e, (fator - 1) * (outro - 1))
        print("n de %3d bits -> fatorado em %8.4f s | chave privada recuperada: %s"
              % (n.bit_length(), tempo, d_atacante == d))
    print("\ncada +16 bits multiplica o tempo por ~16; com 2048 bits não termina")


def demo_tcr():
    print("\n=== 4. TCR: decifrar mais rápido ===\n")
    (e, n), (d, _), (p, q) = gerar_chaves(1024)
    m = texto_para_int("teste de desempenho")
    c = exp_mod(m, e, n)

    inicio = time.time()
    for _ in range(20):
        direto = exp_mod(c, d, n)
    t_direto = time.time() - inicio

    dp = d % (p - 1)
    dq = d % (q - 1)
    inicio = time.time()
    for _ in range(20):
        mp = exp_mod(c, dp, p)
        mq = exp_mod(c, dq, q)
        via_tcr, _ = tcr([mp, mq], [p, q])
    t_tcr = time.time() - inicio

    print("direto (mod n): %.4f s" % t_direto)
    print("com TCR       : %.4f s (%.1fx mais rápido)" % (t_tcr, t_direto / t_tcr))
    print("mesmo resultado?", direto == via_tcr == m)


def main():
    demo_confidencialidade()
    demo_assinatura()
    demo_ataque()
    demo_tcr()


def interativo():
    bits = ler_int("tamanho da chave em bits (64 a 2048) = ", 64, 2048)
    print("\ngerando as chaves...")
    inicio = time.time()
    (e, n), (d, _), _ = gerar_chaves(bits)
    print("  pronto em %.3f s" % (time.time() - inicio))
    print("  n = %s (%d bits)" % (n, n.bit_length()))
    print("  e = %d" % e)
    print("  d = %s" % d)

    documento = input("\ndigite o documento: ")
    m = texto_para_int(documento)
    if m >= n:
        print("  o texto é grande demais para essa chave, escolha mais bits")
        return

    c = exp_mod(m, e, n)
    print("\ncifrado  : %s" % c)
    print("decifrado: %s" % int_para_texto(exp_mod(c, d, n)))

    assinatura = exp_mod(m % n, d, n)
    print("\nassinatura: %s" % assinatura)
    print("confere com o documento? %s" % (exp_mod(assinatura, e, n) == m % n))

    alterado = input("\nagora digite uma versão alterada do documento: ")
    resumo_alterado = texto_para_int(alterado) % n
    print("a assinatura antiga vale para o texto alterado? %s"
          % (exp_mod(assinatura, e, n) == resumo_alterado))

    if bits <= 96:
        print("\ncomo a chave é pequena, dá pra atacar:")
        inicio = time.time()
        fator = pollard_rho(n)
        outro = n // fator
        d_atacante = inverso_multiplicativo(e, (fator - 1) * (outro - 1))
        print("  fatorado em %.4f s -> p = %d, q = %d" % (time.time() - inicio, fator, outro))
        print("  chave privada recuperada? %s" % (d_atacante == d))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos no terminal do Windows
    main()
    print()
