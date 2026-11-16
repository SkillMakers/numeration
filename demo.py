"""Les exercices de la video, executes.

    python demo.py
"""
from fractions import Fraction

from numeration import (addition, addition_signee, binaire_vers_hexa, complement_a_deux, complement_a_un,
                        decimal_exact, depuis_base, flottant_simple, fraction_binaire, groupes, hexa_vers_binaire,
                        inverser, lire_non_signe, lire_signe, oppose, plage, signe_valeur_absolue, vers_base)


def virgule(x):
    """1.5 -> « 1,5 » : l'ecriture francaise."""
    return f"{float(x):g}".replace(".", ",")


def titre(t):
    print()
    print("=" * 72)
    print(t)
    print("=" * 72)


def exercice_1():
    titre("Exercice 1 - convertir 156 en binaire (divisions successives par 2)")
    bits, etapes = vers_base(156, 2)
    for n, q, r in etapes:
        print(f"  {n:>3} / 2 = {q:>3}  reste {r}")
    print(f"  on lit les restes de bas en haut : 156 = {groupes(bits)}")
    print(f"  verification : {' + '.join(str(2 ** p) for _, p in depuis_base(bits, 2)[1])} = {depuis_base(bits, 2)[0]}")
    print(f"  Python : bin(156) = {bin(156)}")


def exercice_2():
    titre("Exercice 2 - convertir 1011 0110 en decimal (puissances de 2)")
    valeur, termes = depuis_base("10110110", 2)
    print("  poids :  128  64  32  16   8   4   2   1")
    print("  bits  :    1   0   1   1   0   1   1   0")
    print(f"  {' + '.join(str(2 ** p) for _, p in termes)} = {valeur}")
    print(f"  Python : int('10110110', 2) = {int('10110110', 2)}")


def exercice_3():
    titre("Exercice 3 - l'hexadecimal : paquets de 4 bits, et 2026 en base 16")
    hexa, paquets = binaire_vers_hexa("10110110")
    print(f"  1011 0110 -> {' | '.join(f'{p} = {c}' for p, c in zip(paquets, hexa))} -> {hexa}")
    print(f"  3F -> {groupes(hexa_vers_binaire('3F'))} = {depuis_base('3F', 16)[0]}")
    chiffres, etapes = vers_base(2026, 16)
    for n, q, r in etapes:
        print(f"  {n:>4} / 16 = {q:>3}  reste {r:>2} -> {vers_base(r, 16)[0]}")
    print(f"  2026 = {chiffres} en hexadecimal ; en binaire : {groupes(hexa_vers_binaire(chiffres))}")
    print(f"  Python : hex(2026) = {hex(2026)}")


def exercice_4():
    titre("Exercice 4 - additionner 0110 1011 + 0011 0110 (107 + 54)")
    a, b = "01101011", "00110110"
    somme, r, retenues = addition(a, b)
    ligne_ret = "".join(str(c) for c in reversed(retenues))
    print(f"  retenues   {groupes(ligne_ret)}")
    print(f"             {groupes(a)}")
    print(f"           + {groupes(b)}")
    print(f"           = {groupes(somme)}   retenue sortante : {r}")
    print(f"  en non signe : {lire_non_signe(a)} + {lire_non_signe(b)} = {lire_non_signe(somme)}")
    print(f"  Python : 107 + 54 = {107 + 54} = {bin(107 + 54)}")


def exercice_5():
    titre("Exercice 5 - ecrire -5 sur 8 bits, de trois facons")
    print(f"  +5                      : {groupes(vers_base(5, 2)[0].zfill(8))}")
    print(f"  signe et valeur absolue : {groupes(signe_valeur_absolue(-5, 8))}")
    print(f"  complement a un         : {groupes(complement_a_un(-5, 8))}")
    c2 = complement_a_deux(-5, 8)
    print(f"  complement a deux       : {groupes(inverser('00000101'))} + 1 = {groupes(c2)}")
    print("  les deux zeros :")
    print(f"    signe et valeur absolue : +0 = {groupes(signe_valeur_absolue(0, 8))}, "
          f"-0 = {groupes('1' + '0' * 7)}")
    print(f"    complement a un         : +0 = {groupes(complement_a_un(0, 8))}, -0 = {groupes(inverser('0' * 8))}")
    print(f"    complement a deux       : un seul zero, {groupes(complement_a_deux(0, 8))}")
    somme, r, _ = addition("00000101", c2)
    print(f"  5 + (-5) : {groupes('00000101')} + {groupes(c2)} = {r} {groupes(somme)} -> sur 8 bits : {groupes(somme)} = 0")
    print(f"  Python : (-5) & 0xFF = {bin((-5) & 0xFF)}")


def exercice_6():
    titre("Exercice 6 - lire un octet : non signe ou signe ?")
    for bits in ("11111111", "10000000", "01111111", "11111011"):
        print(f"  {groupes(bits)} : non signe {lire_non_signe(bits):>3}, en complement a deux {lire_signe(bits):>4}")
    print("  plages :")
    for n in (4, 8, 16, 32):
        nb, nh = plage(n, signe=False)
        sb, sh = plage(n, signe=True)
        print(f"    {n:>2} bits : non signe {nb} a {nh:,} ; signe {sb:,} a {sh:,}".replace(",", " "))
    print("  Python : int.from_bytes(b'\\xff', signed=True) =", int.from_bytes(b"\xff", "big", signed=True))


def le_piege():
    titre("Le piege - l'oppose de -128 sur 8 bits")
    m = complement_a_deux(-128, 8)
    inv = inverser(m)
    o = oppose(m)
    print(f"  -128           = {groupes(m)}")
    print(f"  on inverse     = {groupes(inv)}   ({lire_signe(inv)})")
    print(f"  on ajoute 1    = {groupes(o)}   ({lire_signe(o)})")
    print(f"  l'oppose de -128 est {lire_signe(o)} : +128 ne tient pas sur 8 bits (maximum {plage(8, True)[1]})")
    sans_oppose = [x for x in range(-128, 128) if lire_signe(oppose(complement_a_deux(x, 8))) != -x]
    print(f"  valeurs de -128 a 127 dont l'oppose est faux : {sans_oppose}")
    print(f"  meme chose sur 32 bits : oppose de {plage(32, True)[0]} = "
          f"{lire_signe(oppose(complement_a_deux(plage(32, True)[0], 32)))}")


def exercice_7():
    titre("Exercice 7 - le debordement : 100 + 50 sur 8 bits signes")
    cas = [(100, 50), (-100, -50), (100, -50), (127, 1), (-1, 1)]
    for x, y in cas:
        a, b = complement_a_deux(x, 8), complement_a_deux(y, 8)
        somme, r, v = addition_signee(a, b)
        print(f"  {x:>4} + {y:>4} : {groupes(a)} + {groupes(b)} = {groupes(somme)}  R={r} V={v}"
              f"  -> {lire_signe(somme):>4}{'   FAUX' if v else ''}")
    total = sum(addition_signee(complement_a_deux(x, 8), complement_a_deux(y, 8))[2]
                for x in range(-128, 128) for y in range(-128, 128))
    print(f"  sur les 65 536 additions de deux octets signes, {total} debordent")


def exercice_8():
    titre("Exercice 8 - la virgule : 5,75 en binaire, puis 0,1")
    bits, periode, etapes = fraction_binaire(Fraction(3, 4))
    print("  partie entiere 5 = 101 ; partie fractionnaire 0,75 :")
    for x, b in etapes:
        print(f"    x 2 = {virgule(x)} -> {b}")
    print(f"  5,75 = 101,{bits}   (4 + 1 + 0,5 + 0,25)")
    bits, periode, etapes = fraction_binaire(Fraction(1, 10))
    print("  0,1 :")
    for x, b in etapes:
        print(f"    x 2 = {virgule(x)} -> {b}")
    print(f"  0,1 = 0,{bits[:periode]}({bits[periode:]}) : le motif {bits[periode:]} se repete a l'infini")


def exercice_9():
    titre("Exercice 9 - coder -6,25 en IEEE 754 simple precision")
    print("  6,25 = 110,01 = 1,1001 x 2^2")
    print(f"  exposant stocke = 2 + 127 = 129 = {vers_base(129, 2)[0]}")
    f = flottant_simple(Fraction(-25, 4))
    print(f"  signe {f['signe']} | exposant {f['exposant']} | mantisse {f['mantisse']}")
    print(f"  en hexadecimal : {f['hexa']}")
    import struct
    print(f"  Python : struct.pack('>f', -6.25).hex() = {struct.pack('>f', -6.25).hex()}")


def flottants_et_0_1():
    titre("Le 0,1 en flottant")
    f = flottant_simple(Fraction(1, 10))
    print(f"  0,1 en simple precision : {f['hexa']}, valeur stockee {decimal_exact(f['valeur'])}")
    print(f"  0,1 en double (Python)  : {decimal_exact(Fraction(0.1))}")
    print(f"  0.1 + 0.2 = {0.1 + 0.2}")
    print(f"  0.1 + 0.2 == 0.3 -> {0.1 + 0.2 == 0.3}")
    print(f"  abs((0.1 + 0.2) - 0.3) < 1e-9 -> {abs((0.1 + 0.2) - 0.3) < 1e-9}")


if __name__ == "__main__":
    for ex in (exercice_1, exercice_2, exercice_3, exercice_4, exercice_5, exercice_6, le_piege, exercice_7,
               exercice_8, exercice_9, flottants_et_0_1):
        ex()
