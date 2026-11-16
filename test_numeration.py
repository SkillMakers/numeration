"""Tests : chaque calcul fait « a la main » est compare a Python (int, bin, hex, struct), qui sert de juge.

    python -m unittest -v
"""
import random
import struct
import unittest
from fractions import Fraction

from numeration import (addition, addition_signee, binaire_vers_hexa, complement_a_deux, complement_a_un,
                        decimal_exact, depuis_base, flottant_simple, fraction_binaire, groupes, hexa_vers_binaire,
                        lire_non_signe, lire_signe, oppose, plage, signe_valeur_absolue, valeur_flottant_simple,
                        vers_base)


class TestConversions(unittest.TestCase):

    def test_les_divisions_par_2_donnent_bin_de_python(self):
        """De 0 a 4 095, la methode des divisions successives donne exactement bin(n)."""
        # GIVEN
        nombres = range(4096)
        # WHEN
        resultats = [vers_base(n, 2)[0] for n in nombres]
        # THEN
        self.assertEqual(resultats, [format(n, "b") for n in nombres])

    def test_toutes_les_bases_de_2_a_16(self):
        """L'aller-retour vers_base puis depuis_base retombe sur le nombre, et int(x, base) est d'accord."""
        # GIVEN
        nombres = range(0, 5000, 7)
        for base in range(2, 17):
            for n in nombres:
                # WHEN
                chiffres = vers_base(n, base)[0]
                # THEN
                self.assertEqual(depuis_base(chiffres, base)[0], n)
                self.assertEqual(int(chiffres, base), n)

    def test_exercice_1_156_en_binaire(self):
        """156 = 1001 1100, en huit divisions par 2."""
        # GIVEN
        n = 156
        # WHEN
        bits, etapes = vers_base(n, 2)
        # THEN
        self.assertEqual(bits, "10011100")
        self.assertEqual(len(etapes), 8)

    def test_exercice_2_1011_0110_en_decimal(self):
        """1011 0110 = 128 + 32 + 16 + 4 + 2 = 182."""
        # GIVEN
        bits = "1011 0110"
        # WHEN
        valeur, termes = depuis_base(bits, 2)
        # THEN
        self.assertEqual(valeur, 182)
        self.assertEqual([2 ** p for _, p in termes], [128, 32, 16, 4, 2])

    def test_exercice_3_hexadecimal(self):
        """1011 0110 = B6 ; 3F = 0011 1111 = 63 ; 2026 = 7EA."""
        # GIVEN
        bits, hexa, decimal = "10110110", "3F", 2026
        # WHEN
        b6 = binaire_vers_hexa(bits)[0]
        trois_f = hexa_vers_binaire(hexa), depuis_base(hexa, 16)[0]
        en_hexa = vers_base(decimal, 16)[0]
        # THEN
        self.assertEqual(b6, "B6")
        self.assertEqual(trois_f, ("00111111", 63))
        self.assertEqual(en_hexa, "7EA")

    def test_les_paquets_de_4_bits_donnent_hex_de_python(self):
        """La methode des paquets de 4 bits, dans les deux sens, contre hex()."""
        # GIVEN
        nombres = range(70000)
        for n in nombres:
            # WHEN
            hexa = binaire_vers_hexa(format(n, "b"))[0].lstrip("0") or "0"
            retour = int(hexa_vers_binaire(format(n, "X")), 2)
            # THEN
            self.assertEqual(hexa, format(n, "X"))
            self.assertEqual(retour, n)

    def test_un_chiffre_impossible_est_refuse(self):
        """« 2 » n'existe pas en binaire, « G » pas en hexadecimal : erreur, pas de resultat faux."""
        # GIVEN
        mauvais = [("102", 2), ("1G", 16), ("", 10)]
        for chiffres, base in mauvais:
            # WHEN / THEN
            with self.assertRaises(ValueError):
                depuis_base(chiffres, base)


class TestAddition(unittest.TestCase):

    def test_l_addition_colonne_par_colonne_est_juste_sur_toutes_les_paires_d_octets(self):
        """65 536 paires : somme sur 8 bits et retenue sortante, contre l'addition de Python."""
        # GIVEN
        paires = [(a, b) for a in range(256) for b in range(256)]
        for a, b in paires:
            # WHEN
            somme, r, _ = addition(format(a, "08b"), format(b, "08b"))
            # THEN
            self.assertEqual(int(somme, 2), (a + b) % 256)
            self.assertEqual(r, int(a + b > 255))

    def test_exercice_4(self):
        """0110 1011 + 0011 0110 = 1010 0001 (107 + 54 = 161), sans retenue sortante."""
        # GIVEN
        a, b = "01101011", "00110110"
        # WHEN
        somme, r, retenues = addition(a, b)
        # THEN
        self.assertEqual((somme, r), ("10100001", 0))
        self.assertEqual("".join(map(str, reversed(retenues))), "11111100")


class TestNegatifs(unittest.TestCase):

    def test_le_complement_a_deux_est_celui_du_processeur(self):
        """De -128 a 127 : x & 0xFF est le complement a deux que la machine stocke."""
        # GIVEN
        valeurs = range(-128, 128)
        for x in valeurs:
            # WHEN
            bits = complement_a_deux(x, 8)
            # THEN
            self.assertEqual(bits, format(x & 0xFF, "08b"))
            self.assertEqual(lire_signe(bits), x)

    def test_la_lecture_signee_est_celle_de_int_from_bytes(self):
        """Chaque octet lu en complement a deux, contre int.from_bytes(signed=True)."""
        # GIVEN
        octets = range(256)
        for o in octets:
            # WHEN
            bits = format(o, "08b")
            # THEN
            self.assertEqual(lire_signe(bits), int.from_bytes(bytes([o]), "big", signed=True))
            self.assertEqual(lire_non_signe(bits), o)

    def test_exercice_5_les_trois_ecritures_de_moins_5(self):
        """-5 : 1000 0101, 1111 1010, 1111 1011."""
        # GIVEN
        x, n = -5, 8
        # WHEN
        ecritures = signe_valeur_absolue(x, n), complement_a_un(x, n), complement_a_deux(x, n)
        # THEN
        self.assertEqual(ecritures, ("10000101", "11111010", "11111011"))

    def test_exercice_6_le_meme_octet_vaut_255_ou_moins_1(self):
        """1111 1111 : 255 en non signe, -1 en signe ; 1000 0000 : 128 ou -128."""
        # GIVEN
        octets = ["11111111", "10000000"]
        # WHEN
        lectures = [(lire_non_signe(o), lire_signe(o)) for o in octets]
        # THEN
        self.assertEqual(lectures, [(255, -1), (128, -128)])

    def test_les_plages(self):
        """n bits : 0 a 2^n - 1, ou -2^(n-1) a 2^(n-1) - 1."""
        # GIVEN
        tailles = [(8, False), (8, True), (32, True)]
        # WHEN
        plages = [plage(n, signe=s) for n, s in tailles]
        # THEN
        self.assertEqual(plages, [(0, 255), (-128, 127), (-2147483648, 2147483647)])

    def test_le_piege_seul_moins_128_n_a_pas_d_oppose(self):
        """Inverser et ajouter 1 donne -x pour toutes les valeurs de 8 bits sauf une : -128 redonne -128."""
        # GIVEN
        valeurs = range(-128, 128)
        # WHEN
        faux = [x for x in valeurs if lire_signe(oppose(complement_a_deux(x, 8))) != -x]
        # THEN
        self.assertEqual(faux, [-128])
        self.assertEqual(oppose("10000000"), "10000000")

    def test_hors_plage_refuse(self):
        """128 ne tient pas sur 8 bits signes, ni -128 en signe et valeur absolue : erreur, pas de troncature."""
        # GIVEN
        trop_grand, trop_petit = 128, -128
        # WHEN / THEN
        with self.assertRaises(ValueError):
            complement_a_deux(trop_grand, 8)
        with self.assertRaises(ValueError):
            signe_valeur_absolue(trop_petit, 8)

    def test_une_largeur_trop_petite_est_refusee(self):
        """Signe et valeur absolue, complement a un : il faut au moins 2 bits (le signe, puis la valeur)."""
        # GIVEN
        largeurs = [0, 1]
        for n in largeurs:
            # WHEN / THEN
            with self.assertRaises(ValueError):
                signe_valeur_absolue(0, n)
            with self.assertRaises(ValueError):
                complement_a_un(0, n)


class TestDebordement(unittest.TestCase):

    def test_v_dit_exactement_quand_le_resultat_signe_est_faux(self):
        """65 536 paires d'octets signes : V = 1 si et seulement si la vraie somme sort de -128..127 ; 16 384 cas."""
        # GIVEN
        paires = [(x, y) for x in range(-128, 128) for y in range(-128, 128)]
        debordements = 0
        for x, y in paires:
            # WHEN
            somme, _, v = addition_signee(complement_a_deux(x, 8), complement_a_deux(y, 8))
            # THEN
            self.assertEqual(v, int(not -128 <= x + y <= 127))
            if not v:
                self.assertEqual(lire_signe(somme), x + y)
            debordements += v
        self.assertEqual(debordements, 16384)

    def test_exercice_7(self):
        """100 + 50 = 1001 0110, lu -106, avec V = 1 et sans retenue sortante."""
        # GIVEN
        a, b = complement_a_deux(100, 8), complement_a_deux(50, 8)
        # WHEN
        somme, r, v = addition_signee(a, b)
        # THEN
        self.assertEqual((somme, r, v, lire_signe(somme)), ("10010110", 0, 1, -106))


class TestVirgule(unittest.TestCase):

    def test_exercice_8(self):
        """0,75 = 0,11 (fini) ; 0,1 = 0,0(0011) (periodique)."""
        # GIVEN
        trois_quarts, un_dixieme = Fraction(3, 4), Fraction(1, 10)
        # WHEN
        fini = fraction_binaire(trois_quarts)[:2]
        bits, debut, _ = fraction_binaire(un_dixieme)
        # THEN
        self.assertEqual(fini, ("11", None))
        self.assertEqual((bits[:debut], bits[debut:]), ("0", "0011"))

    def test_une_periode_qui_remplit_juste_la_limite_est_trouvee(self):
        """1/3 = 0,(01) : la periode tient pile dans 2 bits, elle doit etre reconnue."""
        # GIVEN
        un_tiers = Fraction(1, 3)
        # WHEN
        resultat = fraction_binaire(un_tiers, max_bits=2)[:2]
        # THEN
        self.assertEqual(resultat, ("01", 0))

    def test_seuls_les_denominateurs_puissance_de_2_s_ecrivent_en_binaire_fini(self):
        """k/d avec d de 2 a 64 : developpement fini si et seulement si d est une puissance de 2 (fraction reduite)."""
        # GIVEN
        fractions = {Fraction(k, d) for d in range(2, 65) for k in range(1, d)}
        for f in fractions:
            # WHEN
            fini = fraction_binaire(f, max_bits=200)[1] is None
            # THEN
            self.assertEqual(fini, f.denominator & (f.denominator - 1) == 0)

    def test_exercice_9_moins_6_25(self):
        """-6,25 : signe 1, exposant 1000 0001, mantisse 1001 0…, soit C0C80000, comme struct."""
        # GIVEN
        x = -6.25
        # WHEN
        f = flottant_simple(x)
        # THEN
        self.assertEqual((f["signe"], f["exposant"], f["mantisse"][:4]), ("1", "10000001", "1001"))
        self.assertEqual(f["hexa"], "C0C80000")
        self.assertEqual(f["hexa"], struct.pack(">f", x).hex().upper())

    def test_le_codage_flottant_est_celui_de_struct(self):
        """20 000 doubles au hasard (normaux, denormalises, trop petits, trop grands) : meme code que struct."""
        # GIVEN
        hasard = random.Random(2026)
        valeurs = [hasard.uniform(-1, 1) * 10 ** hasard.randint(-50, 42) for _ in range(20000)]
        valeurs += [0.1, 0.2, 0.3, 1.0, 0.0, -0.0, -1e-50, 1e-45, 3.4028235e38, 1.401298464324817e-45]
        trop_grands = 0
        for x in valeurs:
            # WHEN
            code = flottant_simple(x)["hexa"]
            # THEN
            try:
                attendu = struct.pack(">f", x).hex().upper()
            except OverflowError:  # struct refuse ce qui s'arrondit a l'infini : on attend le code de l'infini
                attendu = "FF800000" if x < 0 else "7F800000"
                trop_grands += 1
            self.assertEqual(code, attendu, x)
        self.assertGreater(trop_grands, 0)  # le cas du depassement a bien ete exerce

    def test_l_infini_et_le_zero_negatif(self):
        """1e39 et -1e40 deviennent +inf et -inf ; -0.0 garde son signe (80000000)."""
        # GIVEN
        valeurs = [1e39, -1e40, float("inf"), float("-inf"), -0.0, "-0"]
        # WHEN
        codes = [flottant_simple(x)["hexa"] for x in valeurs]
        # THEN
        self.assertEqual(codes, ["7F800000", "FF800000", "7F800000", "FF800000", "80000000", "80000000"])
        self.assertIsNone(flottant_simple(1e39)["valeur"])

    def test_nan_est_refuse(self):
        """NaN n'a pas de codage dans ce programme : erreur claire."""
        # GIVEN
        nan = float("nan")
        # WHEN / THEN
        with self.assertRaises(ValueError):
            flottant_simple(nan)

    def test_le_0_1_stocke(self):
        """0,1 en simple : 3DCCCCCD = 0,100000001490116119384765625 ; en double, 0.1 + 0.2 != 0.3."""
        # GIVEN
        un_dixieme = Fraction(1, 10)
        # WHEN
        f = flottant_simple(un_dixieme)
        # THEN
        self.assertEqual(f["hexa"], "3DCCCCCD")
        self.assertEqual(decimal_exact(f["valeur"]), "0,100000001490116119384765625")
        self.assertEqual(f["valeur"], Fraction(struct.unpack(">f", struct.pack(">f", 0.1))[0]))
        self.assertEqual(repr(0.1 + 0.2), "0.30000000000000004")
        self.assertNotEqual(0.1 + 0.2, 0.3)

    def test_la_valeur_relue_est_celle_de_struct(self):
        """Lire un code 32 bits redonne la valeur exacte que struct.unpack donne."""
        # GIVEN
        hasard = random.Random(16)
        codes = [c for c in (hasard.getrandbits(32) for _ in range(5000)) if (c >> 23) & 0xFF != 0xFF]
        for c in codes:
            # WHEN
            valeur = valeur_flottant_simple(format(c, "032b"))
            # THEN
            self.assertEqual(valeur, Fraction(struct.unpack(">f", c.to_bytes(4, "big"))[0]))


class TestAffichage(unittest.TestCase):

    def test_groupes(self):
        """Les bits s'affichent par paquets de 4, en partant de la droite."""
        # GIVEN
        octet, neuf_bits = "10011100", "100000000"
        # WHEN
        affichages = groupes(octet), groupes(neuf_bits)
        # THEN
        self.assertEqual(affichages, ("1001 1100", "1 0000 0000"))


if __name__ == "__main__":
    unittest.main()
