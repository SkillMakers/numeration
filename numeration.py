"""Numeration et codage des nombres, calcules a la main comme sur une copie.

Chaque fonction refait le calcul du cours (divisions par 2, paquets de 4 bits, addition colonne par colonne,
complement a deux, virgule flottante) SANS passer par int(x, 2), bin(), hex() ni struct : les tests comparent
ensuite chaque resultat a ces fonctions de Python, qui servent de juge.

Les nombres binaires sont des chaines de '0' et de '1', bit de poids fort a gauche : "10011100".
"""
import math
from fractions import Fraction

CHIFFRES = "0123456789ABCDEF"


# --- Conversions entre bases ------------------------------------------------------------------------------------

def vers_base(n, base):
    """Ecrit l'entier n >= 0 dans la base donnee par divisions successives.

    Renvoie (chiffres, etapes), ou etapes est la liste des (dividende, quotient, reste) dans l'ordre du calcul.
    Le resultat se lit en remontant : le premier reste obtenu est le chiffre de poids faible.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"entier positif ou nul attendu : {n!r}")
    if not 2 <= base <= 16:
        raise ValueError(f"base entre 2 et 16 attendue : {base}")
    if n == 0:
        return "0", [(0, 0, 0)]
    etapes = []
    restes = []
    while n > 0:
        q, r = divmod(n, base)
        etapes.append((n, q, r))
        restes.append(CHIFFRES[r])
        n = q
    return "".join(reversed(restes)), etapes


def depuis_base(chiffres, base):
    """Valeur d'un nombre ecrit dans une base : somme des chiffres fois les puissances de la base.

    Renvoie (valeur, termes), termes = liste des (chiffre, puissance) non nuls, poids fort d'abord.
    """
    if not 2 <= base <= 16:
        raise ValueError(f"base entre 2 et 16 attendue : {base}")
    chiffres = chiffres.replace(" ", "").upper()
    if not chiffres:
        raise ValueError("nombre vide")
    valeur = 0
    termes = []
    for i, c in enumerate(chiffres):
        if c not in CHIFFRES[:base]:
            raise ValueError(f"chiffre {c!r} impossible en base {base}")
        d = CHIFFRES.index(c)
        p = len(chiffres) - 1 - i
        valeur += d * base ** p
        if d:
            termes.append((d, p))
    return valeur, termes


def binaire_vers_hexa(bits):
    """Paquets de 4 bits en partant de la droite, un chiffre hexadecimal par paquet.

    Renvoie (hexa, paquets). Le paquet de gauche est complete par des zeros.
    """
    bits = _verifier_bits(bits)
    bits = bits.zfill((len(bits) + 3) // 4 * 4)
    paquets = [bits[i:i + 4] for i in range(0, len(bits), 4)]
    hexa = "".join(CHIFFRES[depuis_base(p, 2)[0]] for p in paquets)
    return hexa, paquets


def hexa_vers_binaire(hexa):
    """Chaque chiffre hexadecimal devient un paquet de 4 bits."""
    hexa = hexa.replace(" ", "").upper()
    if not hexa or any(c not in CHIFFRES for c in hexa):
        raise ValueError(f"nombre hexadecimal invalide : {hexa!r}")
    return "".join(vers_base(CHIFFRES.index(c), 2)[0].zfill(4) for c in hexa)


# --- Addition binaire ---------------------------------------------------------------------------------------------

def addition(a, b):
    """Addition colonne par colonne de deux nombres binaires de meme longueur n, comme sur papier.

    Renvoie (somme sur n bits, retenue sortante, retenues), ou retenues[i] est la retenue qui ENTRE dans la colonne
    i en comptant depuis la droite (retenues[0] = 0). La retenue sortante est le bit qui ne tient plus sur n bits.
    """
    a, b = _verifier_bits(a), _verifier_bits(b)
    if len(a) != len(b):
        raise ValueError(f"meme nombre de bits attendu : {a} et {b}")
    retenue = 0
    retenues = []
    somme = []
    for x, y in zip(reversed(a), reversed(b)):
        retenues.append(retenue)
        t = int(x) + int(y) + retenue
        somme.append(str(t % 2))
        retenue = t // 2
    return "".join(reversed(somme)), retenue, retenues


# --- Nombres negatifs ---------------------------------------------------------------------------------------------

def plage(n, signe):
    """Plus petite et plus grande valeur sur n bits : non signe, ou en complement a deux."""
    if n < 1:
        raise ValueError("au moins 1 bit")
    if signe:
        return -2 ** (n - 1), 2 ** (n - 1) - 1
    return 0, 2 ** n - 1


def inverser(bits):
    """Le NON bit a bit : chaque 0 devient 1, chaque 1 devient 0."""
    return "".join("1" if c == "0" else "0" for c in _verifier_bits(bits))


def ajouter_un(bits):
    """bits + 1 sur le meme nombre de bits ; la retenue qui deborde a gauche est perdue."""
    bits = _verifier_bits(bits)
    return addition(bits, "1".zfill(len(bits)))[0]


def signe_valeur_absolue(x, n):
    """Bit de signe (1 = negatif) puis la valeur absolue sur n - 1 bits."""
    if n < 2:
        raise ValueError("au moins 2 bits : le signe et la valeur")
    if abs(x) > 2 ** (n - 1) - 1:
        raise ValueError(f"{x} ne tient pas sur {n} bits en signe et valeur absolue")
    return ("1" if x < 0 else "0") + vers_base(abs(x), 2)[0].zfill(n - 1)


def complement_a_un(x, n):
    """Un negatif s'ecrit en inversant tous les bits du positif."""
    if n < 2:
        raise ValueError("au moins 2 bits : le signe et la valeur")
    if abs(x) > 2 ** (n - 1) - 1:
        raise ValueError(f"{x} ne tient pas sur {n} bits en complement a un")
    positif = vers_base(abs(x), 2)[0].zfill(n)
    return inverser(positif) if x < 0 else positif


def complement_a_deux(x, n):
    """Un negatif s'ecrit en inversant tous les bits du positif, puis en ajoutant 1.

    -2**(n-1) n'a pas de positif sur n bits : on l'ecrit par son poids, 1 suivi de zeros.
    """
    bas, haut = plage(n, signe=True)
    if not bas <= x <= haut:
        raise ValueError(f"{x} ne tient pas sur {n} bits en complement a deux ({bas} a {haut})")
    if x == bas:
        return "1" + "0" * (n - 1)
    positif = vers_base(abs(x), 2)[0].zfill(n)
    return ajouter_un(inverser(positif)) if x < 0 else positif


def lire_non_signe(bits):
    """Lecture en non signe : chaque bit vaut son poids, 1, 2, 4… jusqu'a 2**(n-1) pour celui de gauche."""
    return depuis_base(_verifier_bits(bits), 2)[0]


def lire_signe(bits):
    """Lecture en complement a deux : le bit de gauche pese -2**(n-1) au lieu de +2**(n-1)."""
    bits = _verifier_bits(bits)
    n = len(bits)
    return lire_non_signe(bits) - (2 ** n if bits[0] == "1" else 0)


def oppose(bits):
    """L'oppose en complement a deux, comme le fait le processeur : inverser, puis ajouter 1, sur n bits."""
    return ajouter_un(inverser(bits))


def addition_signee(a, b):
    """Addition de deux nombres en complement a deux, avec les deux indicateurs du processeur.

    R : la retenue sortante (depassement en NON signe). V : le debordement (depassement en signe), qui vaut 1
    quand la retenue qui entre dans le bit de signe differe de celle qui en sort : deux positifs qui donnent un
    negatif, ou deux negatifs qui donnent un positif.
    """
    somme, r, retenues = addition(a, b)
    v = int(retenues[-1] != r)
    return somme, r, v


# --- Virgule fixe et virgule flottante ----------------------------------------------------------------------------

def fraction_binaire(x, max_bits=40):
    """Partie fractionnaire de 0 <= x < 1 en binaire, par multiplications successives par 2.

    Renvoie (bits, debut_periode, etapes). Si le developpement est fini, debut_periode vaut None. Sinon les bits a
    partir de debut_periode se repetent a l'infini (on s'arrete au premier retour sur un reste deja vu).
    etapes = liste des (x * 2, bit obtenu).
    """
    x = Fraction(x)
    if not 0 <= x < 1:
        raise ValueError(f"partie fractionnaire attendue (0 <= x < 1) : {x}")
    vus = {}
    bits = []
    etapes = []
    while x:
        if x in vus:
            return "".join(bits), vus[x], etapes
        if len(bits) == max_bits:
            raise ValueError(f"pas de periode trouvee en {max_bits} bits")
        vus[x] = len(bits)
        x *= 2
        bit = int(x >= 1)
        etapes.append((x, bit))
        bits.append(str(bit))
        x -= bit
    return "".join(bits), None, etapes


def flottant_simple(x):
    """Code x en IEEE 754 simple precision (32 bits), arrondi au plus proche (egalite : chiffre pair).

    x : int, float, str decimal (« 0.1 ») ou Fraction ; la valeur exacte est arrondie une seule fois.
    Renvoie un dict : signe, exposant (8 bits), mantisse (23 bits), hexa, et la valeur stockee (Fraction, ou None
    pour l'infini). Gere les nombres normaux, denormalises, -0 et le depassement vers l'infini ; pas les NaN.
    """
    if isinstance(x, float) and math.isnan(x):
        raise ValueError("NaN : pas de codage dans ce programme")
    if isinstance(x, float) and math.isinf(x):
        f, s, a = None, int(x < 0), None
    else:
        f = Fraction(x)
        # Le signe se lit sur x et pas sur f : Fraction(-0.0) vaut 0 et perd le signe du zero negatif.
        negatif = math.copysign(1.0, x) < 0 if isinstance(x, float) else str(x).strip().startswith("-")
        s = int(f < 0 or (f == 0 and negatif))
        a = abs(f)
    if a is None:
        code = 0xFF << 23
    elif a == 0:
        code = 0
    else:
        e = a.numerator.bit_length() - a.denominator.bit_length()
        if Fraction(2) ** e > a:
            e -= 1
        # Maintenant 2**e <= a < 2**(e + 1).
        if e < -126:
            m = round(a * 2 ** 149)  # denormalise : pas de 1 implicite, pas fixe de 2**-149
            code = m  # si l'arrondi atteint 2**23, le code devient tout seul le plus petit normal
        else:
            m = round(a / Fraction(2) ** (e - 23))  # 24 bits, le 1 implicite compris
            if m == 2 ** 24:  # l'arrondi a fait passer a la puissance de 2 suivante
                m //= 2
                e += 1
            code = 0xFF << 23 if e > 127 else (e + 127) << 23 | (m - 2 ** 23)
    code |= s << 31
    bits = vers_base(code, 2)[0].zfill(32)
    return {
        "signe": bits[0],
        "exposant": bits[1:9],
        "mantisse": bits[9:],
        "hexa": vers_base(code, 16)[0].zfill(8),
        "valeur": None if bits[1:9] == "11111111" else valeur_flottant_simple(bits),
    }


def valeur_flottant_simple(bits):
    """Valeur exacte d'un code IEEE 754 simple precision : (-1)^s x 1,mantisse x 2^(exposant - 127)."""
    bits = _verifier_bits(bits)
    if len(bits) != 32:
        raise ValueError("32 bits attendus")
    s = -1 if bits[0] == "1" else 1
    exp = lire_non_signe(bits[1:9])
    mant = lire_non_signe(bits[9:])
    if exp == 255:
        raise ValueError("infini ou NaN : pas de valeur finie")
    if exp == 0:
        return s * Fraction(mant, 2 ** 23) * Fraction(2) ** -126
    return s * (1 + Fraction(mant, 2 ** 23)) * Fraction(2) ** (exp - 127)


def decimal_exact(f, chiffres=60):
    """Ecriture decimale exacte d'une Fraction dont le denominateur est une puissance de 2 (toujours finie)."""
    f = Fraction(f)
    signe = "-" if f < 0 else ""
    f = abs(f)
    entier, reste = divmod(f.numerator, f.denominator)
    decimales = []
    while reste and len(decimales) < chiffres:
        reste *= 10
        d, reste = divmod(reste, f.denominator)
        decimales.append(str(d))
    return signe + str(entier) + ("," + "".join(decimales) if decimales else "")


# --- Outils -------------------------------------------------------------------------------------------------------

def _verifier_bits(bits):
    bits = bits.replace(" ", "")
    if not bits or any(c not in "01" for c in bits):
        raise ValueError(f"nombre binaire invalide : {bits!r}")
    return bits


def groupes(bits, taille=4):
    """« 10011100 » -> « 1001 1100 », pour l'affichage."""
    bits = bits.replace(" ", "")
    debut = len(bits) % taille
    morceaux = [bits[:debut]] if debut else []
    morceaux += [bits[i:i + taille] for i in range(debut, len(bits), taille)]
    return " ".join(morceaux)
