# 5. Analiza podatkov s pandas

**pandas** je knjižnica za delo s tabelami. Osnovni objekt je **DataFrame**, tabela z imenovanimi stolpci in oštevilčenimi vrsticami (indeksom). En stolpec je **Series**.

```python
import pandas as pd
```

Za primere uporabljam izmišljene podatke o učencih in meritvah temperature. Najprej ju zapišemo v CSV:

```python
ucenci = pd.DataFrame({
    "ime": ["Ana", "Bor", "Cene", "Dora", "Eva", "Filip"],
    "razred": ["A", "A", "B", "B", "B", "C"],
    "matematika": [5, 3, 4, 5, None, 2],
    "slovenscina": [4, 4, 5, 3, 5, 3],
    "izostanki": [2, 10, 0, 4, 1, 15],
})
ucenci.to_csv("ucenci.csv", index=False)

meritve = pd.DataFrame({
    "mesto": ["Ljubljana"] * 4 + ["Koper"] * 4,
    "datum": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"] * 2,
    "temperatura": [1.0, 3.0, 2.0, 6.0, 8.0, 9.0, 8.0, 10.0],
})
meritve.to_csv("meritve.csv", index=False)
```

## 5.1 Branje in prvi pregled

```python
ucenci = pd.read_csv("ucenci.csv")
meritve = pd.read_csv("meritve.csv", parse_dates=["datum"])

ucenci.head()      # prvih 5 vrstic
```

- pandas sam prepozna števila in besedilo.
- **`parse_dates=["datum"]`** pretvori besedilo `"2026-01-01"` v pravi datum. Šele potem lahko filtriraš po datumu in rišeš časovne osi.
- Prazna celica postane **`NaN`** (*Not a Number*), torej manjkajoča vrednost.

V Jupytru se zadnja vrstica celice izpiše sama in lepo oblikovano, zato `print` ni potreben.

## 5.2 Izbira stolpcev in vrstic

```python
ucenci["ime"]                       # en stolpec (Series)
ucenci[["ime", "matematika"]]       # več stolpcev (DataFrame) -> dvojni oklepaji!
ucenci.iloc[0]                      # prva vrstica po položaju
ucenci.iloc[-1]                     # zadnja vrstica
```

### Filtriranje s pogojem

```python
ucenci[ucenci["izostanki"] > 5]                                   # Bor, Filip
ucenci[(ucenci["razred"] == "B") & (ucenci["slovenscina"] >= 4)] # Cene, Eva
ucenci[ucenci["ime"].isin(["Ana", "Eva"])]                       # samo izbrani
meritve[meritve["datum"] >= "2026-01-03"]                        # od datuma naprej
```

- `ucenci["izostanki"] > 5` vrne stolpec `True`/`False`, in tabela obdrži vrstice, kjer je `True`.
- Pri več pogojih uporabi `&` (in) ali `|` (ali), vsak pogoj pa v **svojih oklepajih**.
- **Rezultat filtra je nova tabela.** Da ohraniš filtrirano tabelo, jo shrani: `meritve = meritve[...]`.

## 5.3 Opisna statistika

```python
ucenci[["matematika", "slovenscina"]].describe().round(2)
```

`describe()` vrne:

| vrstica | pomen |
|---|---|
| `count` | število podatkov (brez manjkajočih) |
| `mean` | povprečje |
| `std` | standardni odklon, ki pove, kako razpršeni so podatki okoli povprečja |
| `min`, `max` | najmanjša in največja vrednost |
| `25%`, `50%`, `75%` | kvartili; `50%` je **mediana**: polovica vrednosti je manjših, polovica večjih |

**Povprečje ali mediana?** En zelo velik podatek povprečje močno premakne, mediano pa komaj. Pri podatkih z izstopajočimi vrednostmi povesta skupaj več.

## 5.4 Razvrščanje in največje/najmanjše

```python
ucenci.sort_values("izostanki")                    # naraščajoče
ucenci.sort_values("izostanki", ascending=False)   # padajoče
ucenci.nlargest(2, "izostanki")                    # 2 z največ izostanki
ucenci.nsmallest(2, "slovenscina")                 # 2 z najnižjo oceno
ucenci.set_index("ime")                            # stolpec "ime" postane indeks (oznake vrstic)
```

`set_index` je uporaben pred risanjem, ker graf za oznake uporabi indeks.

## 5.5 Štetje in združevanje

```python
ucenci["razred"].value_counts()         # koliko učencev ima vsak razred
ucenci.groupby("razred")["slovenscina"].mean()
ucenci.groupby("razred")[["matematika", "slovenscina"]].mean().round(2)
```

`groupby` deluje v treh korakih: **razdeli** tabelo po skupinah, na vsaki **izračuna** (npr. `mean`) in rezultate **združi** v novo tabelo, kjer je vsaka skupina ena vrstica.

Dolge verige ukazov lahko zapišeš v oklepajih, vsak korak v svoji vrstici:

```python
povprecja = (
    ucenci.groupby("razred")[["matematika", "slovenscina"]]
    .mean()
    .sort_values("slovenscina")
)
```

## 5.6 Manjkajoče vrednosti

```python
ucenci.dropna()                    # odstrani vrstice z manjkajočimi vrednostmi
```

Funkcije, kot so `mean`, `describe` in `corr`, manjkajoče vrednosti (`NaN`) same izpustijo. Zato ima v `describe` stolpec z manjkajočo vrednostjo manjši `count`.

## 5.7 Korelacija

```python
ucenci["izostanki"].corr(ucenci["slovenscina"])
```

**Korelacija** (od −1 do 1) meri, kako sta dve količini linearno povezani:
- blizu **1**: ko ena raste, raste tudi druga,
- blizu **−1**: ko ena raste, druga pada,
- blizu **0**: ni linearne povezave.

Groba lestvica: |r| < 0,3 šibka, 0,3–0,7 zmerna, > 0,7 močna povezava. **Korelacija ne pomeni vzročnosti.**

## 5.8 Časovne vrste

### Iz dolge v široko obliko: `pivot`

Meritve so v **dolgi** obliki (ena vrstica = eno mesto na en dan). Za primerjavo mest je bolj praktična **široka** oblika (en stolpec na mesto):

```python
siroka = meritve.pivot(index="datum", columns="mesto", values="temperatura")
print(siroka)
# mesto       Koper  Ljubljana
# datum
# 2026-01-01    8.0        1.0
# ...
```

### Sprememba iz dneva v dan

```python
meritve = meritve.sort_values(["mesto", "datum"])
meritve["sprememba"] = meritve.groupby("mesto")["temperatura"].pct_change() * 100
```

- `pct_change()` je relativna sprememba glede na prejšnjo vrstico (0,5 pomeni +50 %, zato pomnožimo s 100).
- `groupby("mesto")` poskrbi, da se prva vrednost Kopra ne primerja z zadnjo vrednostjo Ljubljane.
- Pred tem je treba **razvrstiti po datumu**.

Standardni odklon sprememb pove, kako zelo količina „skače“:
```python
meritve.groupby("mesto")["sprememba"].std()
```

### Indeks: primerjava na isti lestvici

Če imata dve vrsti zelo različne velikosti, ju preračunaš tako, da obe začneta pri 100:

```python
indeks = siroka / siroka.iloc[0] * 100
```

`siroka.iloc[0]` je prva vrstica. Vsak stolpec se deli s svojo prvo vrednostjo, zato indeks 150 pomeni +50 % glede na začetek, ne glede na to, kakšne so bile izhodiščne vrednosti.

Če kateri stolpec na začetku nima podatkov (`NaN`), najprej odstrani nepopolne vrstice z `siroka.dropna()`, da vsi začnejo na isti dan.

## 5.9 Dodajanje stolpca iz druge tabele: `join`

```python
dodatno = pd.Series({"Ana": "zbor", "Cene": "nogomet"}, name="krozek")
ucenci = ucenci.join(dodatno, on="ime")   # doda stolpec "krozek" po ujemanju imena
```

`on="ime"` pove, po katerem stolpcu se vrstice ujemajo z indeksom druge tabele. Kjer ujemanja ni, je `NaN`.

Če `join` istega stolpca dodaš dvakrat (npr. ponovno poženeš celico v Jupytru), dobiš napako, ker stolpec že obstaja. Rešitev je **Restart & Run All**.
