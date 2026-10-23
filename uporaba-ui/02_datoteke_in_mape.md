# 2. Datoteke, mape in CSV

## 2.1 Branje in pisanje besedilnih datotek

```python
with open("pozdrav.txt", "w", encoding="utf-8") as datoteka:
    datoteka.write("Živijo, svet!\n")

with open("pozdrav.txt", encoding="utf-8") as datoteka:
    vsebina = datoteka.read()
print(vsebina)
```

- **Način:** `"w"` pomeni pisanje (obstoječo vsebino **prepiše**), `"a"` dodajanje na konec, `"r"` branje (privzeto).
- **`with`** datoteko samodejno zapre, ko blok konča, tudi če pride do napake. Zato ne potrebuješ `datoteka.close()`.
- **`encoding="utf-8"`**: brez tega se lahko na Windows č, š in ž pokvarijo. Pri slovenskem besedilu ga vedno navedi.

## 2.2 Poti in mape: modul `os`

```python
import os

pot = os.path.join("podatki", "surovo", "stran.html")
print(pot)   # podatki/surovo/stran.html  (na Windows: podatki\surovo\stran.html)

os.makedirs(os.path.join("podatki", "surovo"), exist_ok=True)
print(os.path.exists(os.path.join("podatki", "surovo")))  # True
print(os.path.exists("ne_obstaja.txt"))                   # False
```

- **`os.path.join`** sestavi pot s pravilnim ločilom za operacijski sistem. Poševnic ne piši ročno.
- **`os.makedirs(mapa, exist_ok=True)`** ustvari mapo in vse nadrejene mape. Z `exist_ok=True` ni napake, če mapa že obstaja.
- **`os.path.exists(pot)`** vrne `True`/`False`. Uporabno, da česa ne prenašaš dvakrat.

## 2.3 Vzorec: pomožne funkcije za datoteke

V projektih se splača pisanje in branje zapreti v funkcije, ki jih nato uporabljaš povsod:

```python
import os


def shrani(besedilo, mapa, ime):
    """Zapiše niz v datoteko mapa/ime; mapo po potrebi ustvari."""
    os.makedirs(mapa, exist_ok=True)
    with open(os.path.join(mapa, ime), "w", encoding="utf-8") as f:
        f.write(besedilo)


def preberi(mapa, ime):
    """Vrne vsebino datoteke mapa/ime kot niz."""
    with open(os.path.join(mapa, ime), encoding="utf-8") as f:
        return f.read()


shrani("prva vrstica\n", "zapiski", "test.txt")
print(preberi("zapiski", "test.txt"))
```

## 2.4 Predpomnjenje: ne prenašaj dvakrat

Pogost vzorec pri zajemu podatkov: če je datoteka že na disku, je ne prenašaj znova.

```python
def pridobi(ime, ponovno=False):
    """Vrne vsebino datoteke; 'prenos' izvede le, če je ni ali če ponovno=True."""
    if os.path.exists(os.path.join("predpomnilnik", ime)) and not ponovno:
        return preberi("predpomnilnik", ime)
    vsebina = f"vsebina za {ime}"   # tu bi bil pravi prenos s spleta
    shrani(vsebina, "predpomnilnik", ime)
    return vsebina


print(pridobi("a.txt"))
print(pridobi("a.txt"))   # drugič se prebere z diska
```

**Zakaj:** strani ne obremenjuješ z odvečnimi zahtevki, program je hitrejši, in če se zmotiš pri obdelavi, lahko obdelavo ponoviš brez novega prenosa.

## 2.5 CSV: zapis seznama slovarjev

CSV (*comma-separated values*) je besedilna tabela. Prva vrstica so imena stolpcev, vsaka naslednja vrstica pa je en zapis.

```
naslov,avtor,leto
Martin Krpan,Levstik,1858
Butalci,Milčinski,1949
```

Z modulom `csv` zapišeš seznam slovarjev:

```python
import csv

knjige = [
    {"naslov": "Martin Krpan", "avtor": "Levstik", "leto": 1858},
    {"naslov": "Butalci", "avtor": "Milčinski", "leto": 1949},
]

with open("knjige.csv", "w", encoding="utf-8", newline="") as f:
    pisalec = csv.DictWriter(f, fieldnames=["naslov", "avtor", "leto"])
    pisalec.writeheader()       # prva vrstica z imeni stolpcev
    pisalec.writerows(knjige)   # vse vrstice naenkrat
```

- **`fieldnames`** določa stolpce in njihov vrstni red. Ključi slovarjev se morajo ujemati.
- **`newline=""`**: brez tega na Windows med vrsticami nastanejo prazne vrstice.
- Vrednost `None` se zapiše kot prazna celica.
