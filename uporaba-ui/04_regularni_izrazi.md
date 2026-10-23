# 4. Regularni izrazi (modul `re`)

Regularni izraz je **vzorec**, s katerim v besedilu poiščeš dele, ki ustrezajo pravilu, npr. „vsa števila“ ali „vse, kar je med `<b>` in `</b>`“.

```python
import re
```

## 4.1 Osnovni gradniki

| Vzorec | Pomen | Primer ujemanja |
|---|---|---|
| `abc` | dobesedno besedilo | `abc` |
| `.` | katerikoli znak (razen nove vrstice) | `a`, `7`, `%` |
| `\d` | števka | `5` |
| `\w` | črka, števka ali `_` | `a`, `č`, `3` |
| `\s` | prazen prostor (presledek, tabulator, nova vrstica) | ` ` |
| `\W`, `\D`, `\S` | **nasprotje** zgornjih | |
| `[abc]` | eden od naštetih znakov | `b` |
| `[\d.,]` | števka, pika ali vejica | `,` |
| `[^"]` | katerikoli znak **razen** `"` | `x` |
| `\.` `\(` `\?` | dobesedna pika, oklepaj, vprašaj (ubežni znak) | `.` |

**Ponavljanje:**

| | Pomen |
|---|---|
| `*` | 0 ali več |
| `+` | 1 ali več |
| `?` | 0 ali 1 |
| `{3}` | točno 3-krat |

```python
besedilo = "Cena: 12,50 €, popust 3 €, skupaj 9,50 €"
print(re.findall(r"\d+", besedilo))         # ['12', '50', '3', '9', '50']
print(re.findall(r"\d[\d,]*", besedilo))    # ['12,50', '3', '9,50']
```

Drugi vzorec pomeni „števka, nato poljubno števk ali vejic“. Vzorec `[\d,]+` bi ujel tudi samostojne vejice za cenami, zato mora biti prvi znak števka.

**`r"..."` (surov niz):** v navadnem nizu ima `\` poseben pomen (`"\n"` je nova vrstica). V surovem nizu ostane `\` dobesedno, kar je pri regularnih izrazih skoraj vedno tisto, kar želiš. Zato regularne izraze vedno piši z `r`.

## 4.2 Skupine: izlušči samo del

Z oklepaji `( )` označiš del, ki ga želiš dobiti ven:

```python
html = '<a href="/knjiga/12">Martin Krpan</a> <a href="/knjiga/7">Butalci</a>'
print(re.findall(r'<a href="/knjiga/(\d+)">(.*?)</a>', html))
# [('12', 'Martin Krpan'), ('7', 'Butalci')]
```

- Ena skupina: `findall` vrne seznam nizov.
- Več skupin: `findall` vrne seznam naborov (tuple).

### Imenovane skupine

`(?P<ime>...)` da skupini ime, kar izboljša berljivost:

```python
vzorec = r'<a href="/knjiga/(?P<id>\d+)">(?P<naslov>.*?)</a>'
for ujemanje in re.finditer(vzorec, html):
    print(ujemanje["id"], ujemanje["naslov"])
# 12 Martin Krpan
# 7 Butalci
```

- `re.finditer` vrne ujemanja eno za drugim kot objekte `Match`.
- `ujemanje["id"]` je isto kot `ujemanje.group("id")`.
- `ujemanje.groupdict()` vrne slovar vseh imenovanih skupin.

## 4.3 Pohlepno in nepohlepno: `.*` ali `.*?`

To je najpogostejša past.

```python
html = "<b>prvi</b> in <b>drugi</b>"
print(re.findall(r"<b>(.*)</b>", html))    # ['prvi</b> in <b>drugi']
print(re.findall(r"<b>(.*?)</b>", html))   # ['prvi', 'drugi']
```

- **`.*` (pohlepno)** ujame **čim več**, torej do **zadnjega** `</b>`.
- **`.*?` (nepohlepno)** ujame **čim manj**, torej do **prvega** `</b>`.

Pri razčlenjevanju HTML skoraj vedno želiš `.*?`.

## 4.4 Zastavice: `re.DOTALL`

`.` privzeto **ne** ujame znaka za novo vrstico. HTML pa se pogosto razteza čez več vrstic:

```python
html = """<div class="cena">
    12,50
</div>"""
print(re.findall(r'<div class="cena">(.*?)</div>', html))             # []
print(re.findall(r'<div class="cena">(.*?)</div>', html, re.DOTALL))  # ['\n    12,50\n']
print(re.findall(r'<div class="cena">\s*([\d,]+)\s*</div>', html))    # ['12,50']
```

Zadnja vrstica pokaže drugo rešitev: `\s*` „pogoltne“ presledke in nove vrstice okoli števila, `[\d,]+` pa ujame samo število.

## 4.5 `re.compile`: vzorec pripravi enkrat

```python
VZOREC_CENE = re.compile(r"(\d+),(\d{2}) €")

for vrstica in ["kruh 2,30 €", "mleko 1,15 €"]:
    m = VZOREC_CENE.search(vrstica)
    print(int(m[1]) + int(m[2]) / 100)
```

- Vzorec, ki ga uporabljaš večkrat, prevedeš enkrat in ga shraniš kot konstanto.
- `search` najde **prvo** ujemanje (ali vrne `None`), `findall` pa **vsa**.

**Dolg vzorec razdeli na več vrstic.** Zaporedni nizi v oklepajih se samodejno združijo:

```python
VZOREC_KNJIGE = re.compile(
    r'<div class="knjiga">\s*'
    r'<h2>(?P<naslov>.*?)</h2>\s*'
    r'<span class="avtor">(?P<avtor>.*?)</span>',
    re.DOTALL,
)
```

## 4.6 Dva koraka: najprej blok, nato podrobnosti

Če en zapis vsebuje **več** enakih podatkov (npr. več ocen), jih ena skupina ne ujame vseh. Najprej izlušči celoten blok, nato iz njega z drugim vzorcem vse vrednosti:

```python
html = """
<div class="izdelek"><h3>Kruh</h3><span class="ocena">4</span><span class="ocena">5</span></div>
<div class="izdelek"><h3>Mleko</h3><span class="ocena">3</span></div>
"""
VZOREC_BLOKA = re.compile(r'<div class="izdelek">(.*?)</div>', re.DOTALL)
VZOREC_IMENA = re.compile(r"<h3>(.*?)</h3>")
VZOREC_OCENE = re.compile(r'<span class="ocena">(\d)</span>')

izdelki = []
for blok in VZOREC_BLOKA.findall(html):
    ime = VZOREC_IMENA.search(blok)[1]
    ocene = [int(o) for o in VZOREC_OCENE.findall(blok)]
    izdelki.append({"ime": ime, "povprecna_ocena": sum(ocene) / len(ocene)})
print(izdelki)
# [{'ime': 'Kruh', 'povprecna_ocena': 4.5}, {'ime': 'Mleko', 'povprecna_ocena': 3.0}]
```

Enak pristop uporablja `macke.py` s predavanj: `page_to_ads` razdeli stran na oglase, `get_dict_from_ad_block` pa iz vsakega izlušči podatke.

## 4.7 `re.sub`: zamenjava

```python
naslov = "Martin Krpan z Vrha!"
print(re.sub(r"\W+", "_", naslov.lower()).strip("_"))   # martin_krpan_z_vrha
```

`\W+` (eden ali več znakov, ki niso črke ali števke) zamenja z enim `_`. Tako iz poljubnega besedila narediš varno ime datoteke.

## 4.8 Kako sestaviš vzorec za resnično stran

1. Shrani HTML v datoteko in ga odpri v urejevalniku.
2. Poišči en primer podatka, ki ga želiš (Ctrl+F).
3. Poglej, kaj je **tik pred** in **tik za** njim. To postane dobesedni del vzorca.
4. Podatek zamenjaj s skupino, npr. `(.*?)` ali bolj natančno `(\d+)`.
5. Preizkusi na enem primeru (`re.search`), šele nato na celi strani (`findall`). Preveri, ali je število zadetkov pričakovano.

Za sprotno preizkušanje je priročna stran [regex101.com](https://regex101.com) (izberi „Python“).
