# 1. Python za obdelavo zajetih podatkov

Deli Pythona, ki se pri zajemanju podatkov s spleta uporabljajo drugače kot pri običajnem programiranju: kako hraniš zajete zapise, kako vrednostim prirediš imena stolpcev in kako besedilo s strani pretvoriš v števila.

## 1.1 Zajeti podatki kot seznam slovarjev

```python
knjiga = {"naslov": "Martin Krpan", "avtor": "Levstik", "leto": 1858}
print(knjiga["avtor"])          # Levstik
knjiga["strani"] = 64           # dodamo nov ključ

knjige = []                     # seznam slovarjev = "tabela"
knjige.append(knjiga)
knjige.append({"naslov": "Butalci", "avtor": "Milčinski", "leto": 1949})
print(len(knjige))              # 2
```

**Seznam slovarjev** je najpogostejša oblika podatkov pred zapisom v CSV: vsak slovar je ena vrstica, ključi pa so stolpci.

**Ključi v slovarju so unikatni.** Če isti ključ zapišeš dvakrat, se vrednost prepiše. To je preprost način za odstranjevanje podvojitev:

```python
meritve = [("pon", 12), ("tor", 14), ("tor", 14), ("sre", 11)]
po_dnevih = {}
for dan, temperatura in meritve:
    po_dnevih[dan] = temperatura
print(po_dnevih)  # {'pon': 12, 'tor': 14, 'sre': 11}  -> "tor" le enkrat
```

`.items()` vrne pare (ključ, vrednost):

```python
for dan, t in sorted(po_dnevih.items()):
    print(dan, t)
```

## 1.2 `zip`: hkrati čez dva seznama

```python
predmeti = ["matematika", "fizika", "kemija"]
ocene = [9, 8, 10]

for predmet, ocena in zip(predmeti, ocene):
    print(predmet, ocena)

spricevalo = dict(zip(predmeti, ocene))
print(spricevalo)  # {'matematika': 9, 'fizika': 8, 'kemija': 10}
```

`zip` sestavi pare istoležnih elementov in se ustavi pri krajšem seznamu. Uporaben je, ko imaš seznam imen stolpcev in seznam vrednosti v istem vrstnem redu, saj ti ni treba pisati `ocene[0]`, `ocene[1]` …

## 1.3 Pretvorba v števila: `try/except`

```python
def v_stevilo(niz):
    """Pretvori niz v float; če ne gre, vrne None."""
    try:
        return float(niz)
    except ValueError:
        return None


print(v_stevilo("3.5"))  # 3.5
print(v_stevilo("-"))    # None
```

- Koda v `try` se izvaja normalno. Če pride do napake **navedene vrste**, se izvede `except`.
- Lovi **konkretno** napako (`ValueError`, `KeyError` …), ne kar vseh. Sicer skriješ tudi napake, ki jih nisi pričakoval.

Pogoste vrste napak:

| Napaka | Kdaj |
|---|---|
| `ValueError` | prava vrsta, napačna vrednost: `float("abc")` |
| `KeyError` | ključa ni v slovarju ali stolpca ni v tabeli |
| `NameError` | spremenljivka ne obstaja (npr. tipkarska napaka, celica ni bila izvedena) |
| `FileNotFoundError` | datoteka ne obstaja |
| `TypeError` | napačna vrsta: `"3" + 4` |

## 1.4 Čiščenje besedila s strani

```python
s = "  1.234,56  "
s = s.strip()                    # "1.234,56"   odstrani presledke na robovih
s = s.replace(".", "")           # "1234,56"
s = s.replace(",", ".")          # "1234.56"
print(float(s))                  # 1234.56

print("Martin Krpan".lower())    # martin krpan
print("a,b,c".split(","))        # ['a', 'b', 'c']
print("__ime__".strip("_"))      # ime
```

**Vrstni red zamenjav je pomemben:** če bi najprej zamenjal `,` s `.`, bi dobil `1.234.56`.
