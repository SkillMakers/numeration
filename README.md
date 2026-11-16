# Numération binaire, hexadécimal et complément à deux : exercices corrigés

Code de la vidéo **Numération binaire, hexadécimal et complément à deux** de la chaîne
[IT Skills Maker](https://www.youtube.com/@ItSkillsMaker), 3e vidéo de la playlist « Architecture des ordinateurs : cours
et exercices corrigés ». La vidéo précédente, sur les portes logiques et l'additionneur :
[SkillMakers/portes-logiques](https://github.com/SkillMakers/portes-logiques).

Chaque calcul est refait **comme sur une copie** (divisions par 2, paquets de 4 bits, addition colonne par colonne,
inverser et ajouter 1, multiplications par 2, codage IEEE 754), sans `int(x, 2)`, `bin`, `hex` ni `struct`. Les tests
comparent ensuite chaque résultat à ces fonctions de Python, qui servent de juge.

## Lancer

Python 3.11 ou plus, aucune dépendance.

```
python demo.py           # les neuf exercices de la vidéo, et le piège de -128
python -m unittest -v    # les 29 tests
```

Les sorties obtenues pour la vidéo sont dans [`preuves/`](preuves/) : `demo.txt` (Python 3.15.1) et `tests.txt`
(29 tests verts sous 3.15.1 et 3.11).

## Les exercices

| | Énoncé | Résultat |
|---|---|---|
| 1 | Écrire 156 en binaire | 1001 1100 (8 divisions par 2) |
| 2 | Que vaut 1011 0110 ? | 128 + 32 + 16 + 4 + 2 = 182 |
| 3 | 1011 0110 et 3F, puis 2026 en hexadécimal | B6 ; 0011 1111 = 63 ; 7EA |
| 4 | 0110 1011 + 0011 0110 | 1010 0001 (107 + 54 = 161) |
| 5 | -5 sur 8 bits, de trois façons | 1000 0101 · 1111 1010 · 1111 1011 |
| 6 | Que vaut l'octet 1111 1111 ? | 255 en non signé, -1 en complément à deux |
| 7 | 100 + 50 sur 8 bits signés | 1001 0110 = -106 : débordement (16 384 additions sur 65 536 débordent) |
| 8 | 5,75 puis 0,1 en binaire | 101,11 ; 0,0(0011) se répète à l'infini |
| 9 | -6,25 en IEEE 754 simple précision | 1 · 1000 0001 · 1001 0…0 = C0C80000 |

**Le piège** : sur 8 bits, l'opposé de -128 (inverser, puis ajouter 1) redonne -128. C'est la seule valeur des 256 dans
ce cas, et la même chose arrive à -2 147 483 648 sur 32 bits.

## Les fichiers

| Fichier | Rôle |
|---|---|
| `numeration.py` | les conversions, l'addition, les trois écritures des négatifs, le débordement, la virgule fixe et le codage IEEE 754 |
| `demo.py` | les exercices de la vidéo, exécutés |
| `test_numeration.py` | chaque résultat cité dans la vidéo, en test, et la comparaison avec Python |

## Ce que le programme simplifie

- **IEEE 754** : simple précision seulement, arrondi au plus proche (égalité vers le chiffre pair) ; le dépassement
  donne l'infini, -0 garde son signe ; les NaN ne sont pas codés.
- Les nombres binaires sont des chaînes de `0` et de `1`, bit de poids fort à gauche.
