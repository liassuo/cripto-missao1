import os
import sys
MISSAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MISSAO)
sys.path.insert(0, os.path.dirname(MISSAO))

from entrada import ler_int
from missao1.securedocs_math.exponenciacao_modular import exp_mod
from missao1.securedocs_math.primos import eh_primo
from securedocs_simetrica import arquivo, troca_chaves as tc
from securedocs_simetrica.blocos import para_hex
from textos import MENSAGEM


def dh_pequeno(p, g, a, b):
    A = exp_mod(g, a, p)
    B = exp_mod(g, b, p)
    print("públicos: p = %d, g = %d" % (p, g))
    print("Alice sorteia a = %d e envia A = %d^%d mod %d = %d" % (a, g, a, p, A))
    print("Bob   sorteia b = %d e envia B = %d^%d mod %d = %d" % (b, g, b, p, B))
    print("Alice calcula B^a = %d^%d mod %d = %d" % (B, a, p, tc.dh_segredo(B, a, p)))
    print("Bob   calcula A^b = %d^%d mod %d = %d" % (A, b, p, tc.dh_segredo(A, b, p)))
    print("o invasor viu p, g, A e B. Com p pequeno ele acha a no braço:")
    print("  log discreto de %d na base %d = %s" % (A, g, tc.logaritmo_discreto(A, g, p)))


def main():
    print("=== 8. NOVA DESCOBERTA: COMO ENTREGAR A CHAVE? ===\n")

    print("problema 1: com chave simétrica cada par de pessoas precisa da sua chave")
    for n in (2, 10, 100, 1000):
        print("  %4d usuários -> %7d chaves" % (n, tc.chaves_necessarias(n)))
    print("e cada uma teria que ser entregue por um canal seguro (pessoalmente, pendrive...)\n")

    print("--- SOLUÇÃO 1: Diffie-Hellman (1976) - combinar a chave em público ---")
    dh_pequeno(23, 5, 6, 15)

    print("\ncom o primo de 2048 bits da RFC 3526 (valores reais):")
    a, A = tc.dh_par_de_chaves()
    b, B = tc.dh_par_de_chaves()
    k_alice = tc.derivar_chave_aes(tc.dh_segredo(B, a))
    k_bob = tc.derivar_chave_aes(tc.dh_segredo(A, b))
    print("  A = %s... (%d bits)" % (hex(A)[2:34].upper(), A.bit_length()))
    print("  B = %s... (%d bits)" % (hex(B)[2:34].upper(), B.bit_length()))
    print("  chave AES da Alice: %s" % para_hex(k_alice, 4))
    print("  chave AES do Bob  : %s" % para_hex(k_bob, 4))
    print("  agora o log discreto teria ~2^112 passos: inviável")

    cifrado = arquivo.cifrar_dados(MENSAGEM.encode("utf-8"), k_alice)
    print("  Alice cifra, Bob decifra: %s" % arquivo.decifrar_dados(cifrado, k_bob).decode())

    print("\nmas e o homem-no-meio? Eva intercepta A e B e troca pelos dela:")
    e, E = tc.dh_par_de_chaves()
    k_alice_eva = tc.derivar_chave_aes(tc.dh_segredo(E, a))
    k_bob_eva = tc.derivar_chave_aes(tc.dh_segredo(E, b))
    print("  Alice <-> Eva: %s..." % para_hex(k_alice_eva)[:16])
    print("  Eva <-> Bob  : %s..." % para_hex(k_bob_eva)[:16])
    print("  Eva decifra tudo e cifra de novo para o outro lado. O DH sozinho não")
    print("  sabe QUEM está do outro lado -> precisa de autenticação (certificado/assinatura)")

    print("\n--- SOLUÇÃO 2: envelope digital (RSA, Missão 1) ---")
    publica, privada = tc.rsa_gerar_chaves(1024)
    print("Bob gera p e q (Miller-Rabin), n = pq, e = 65537, d = e^-1 mod phi(n)")
    print("  n = %s... (%d bits)" % (hex(publica[0])[2:34].upper(), publica[0].bit_length()))
    chave_doc = arquivo.gerar_chave(256)
    envelope = tc.envelope_fechar(chave_doc, publica)
    print("Alice sorteia a chave do documento: %s" % para_hex(chave_doc, 4))
    print("e manda envelope = chave^e mod n  : %s..." % hex(envelope)[2:34].upper())
    aberta = tc.envelope_abrir(envelope, privada, 32)
    print("Bob abre com envelope^d mod n     : %s" % para_hex(aberta, 4))
    print("o invasor vê n, e e o envelope; para abrir precisaria fatorar n")

    print("\nresposta: a chave do AES NÃO viaja aberta. Ela é combinada (Diffie-Hellman)")
    print("ou vai trancada com a chave pública do destinatário (RSA). A cifra assimétrica")
    print("só protege a chave (32 bytes); o arquivo em si continua no AES, que é rápido.")
    print("É o esquema híbrido do HTTPS/TLS - e o tema da próxima missão.")


def interativo():
    p = ler_int("primo p (pequeno, ex. 23): ", 5, 100000)
    if not eh_primo(p):
        print("  %d não é primo" % p)
        return
    g = ler_int("gerador g: ", 2, p - 2)
    a = ler_int("segredo da Alice a: ", 2, p - 2)
    b = ler_int("segredo do Bob b: ", 2, p - 2)
    print()
    dh_pequeno(p, g, a, b)


if __name__ == "__main__":
    main()
