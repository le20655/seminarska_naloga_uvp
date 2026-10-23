# 6. Grafi s pandas in matplotlib

pandas ima vgrajeno risanje (`.plot`), ki v ozadju uporablja knjižnico **matplotlib**. Iz matplotlib potrebuješ le še `plt` za oznake in prikaz.

```python
import pandas as pd
import matplotlib.pyplot as plt

prodaja = pd.DataFrame({
    "izdelek": ["kruh", "mleko", "jajca", "sir", "jabolka", "kava"],
    "kategorija": ["pekarna", "mlečni", "mlečni", "mlečni", "sadje", "pijača"],
    "prodano": [120, 95, 60, 30, 80, 45],
    "cena": [2.3, 1.2, 3.5, 6.0, 1.8, 7.5],
})
```

## 6.1 Kateri graf za kaj

| Vprašanje | Graf | Ukaz |
|---|---|---|
| Koliko je česa (malo kategorij)? | stolpični | `.plot.bar()` |
| Lestvica, dolga imena | vodoravni stolpični | `.plot.barh()` |
| Kako se nekaj spreminja s časom? | črtni | `.plot()` |
| Ali sta dve količini povezani? | razsevni | `.plot.scatter()` |

## 6.2 Osnovni vzorec

```python
prodaja["kategorija"].value_counts().plot.bar(title="Število izdelkov po kategorijah")
plt.ylabel("število izdelkov")
plt.show()
```

1. pripraviš podatke (tu `value_counts()`),
2. narišeš z `.plot.<vrsta>(title=...)`,
3. dodaš oznake osi (`plt.xlabel`, `plt.ylabel`),
4. `plt.show()` graf prikaže in ga „zaključi“, tako da naslednji graf ne riše čez istega.

**Vsak graf naj ima naslov in oznake osi z enotami** („donos v %“, „temperatura (°C)“). Brez enot bralec ne ve, kaj gleda.

## 6.3 Vodoravni stolpični graf: lestvice

```python
najbolj_prodajani = prodaja.nlargest(5, "prodano").set_index("izdelek")
najbolj_prodajani["prodano"].sort_values().plot.barh(
    title="5 najbolj prodajanih izdelkov", color="tab:green"
)
plt.xlabel("prodanih kosov")
plt.show()
```

- `set_index("izdelek")`: graf za oznake vzame indeks, zato želimo imena izdelkov kot indeks.
- **`sort_values()` pred `barh`**: `barh` riše od spodaj navzgor, zato naraščajoče razvrščanje postavi največjega **na vrh**.
- `color=`: barve `"tab:blue"`, `"tab:red"`, `"tab:green"` … Rdečo uporabi za „slabo“ in zeleno za „dobro“ samo, če to res pomaga razumevanju.

## 6.4 Stolpični graf za več stolpcev hkrati

```python
po_kategorijah = prodaja.groupby("kategorija")[["prodano", "cena"]].mean()
po_kategorijah.plot.bar(title="Povprečje po kategorijah")
plt.show()
```

Vsak stolpec tabele postane svoja barva, legenda pa se doda sama. Paziti moraš, da so stolpci v **istih enotah**. Kosi in evri na isti osi sta slaba kombinacija; tu bi bilo bolje narisati dva grafa.

## 6.5 Črtni graf: časovne vrste

```python
dnevi = pd.date_range("2026-01-01", periods=6)
temp = pd.DataFrame({"Ljubljana": [1, 3, 2, 6, 5, 7],
                     "Koper": [8, 9, 8, 10, 11, 10]}, index=dnevi)

temp.plot(title="Dnevna temperatura", figsize=(10, 5))
plt.ylabel("temperatura (°C)")
plt.show()
```

- Pri široki tabeli (en stolpec na črto) z datumom kot indeksom pandas sam nariše vsako črto in legendo.
- `figsize=(širina, višina)` v palcih. Časovne vrste so bolj berljive v širšem grafu.

**Primerjava na isti lestvici:** če imajo vrste zelo različne velikosti (ena 5, druga 500), jih preračunaj v indeks (glej datoteko 5, razdelek 5.8):
```python
(temp / temp.iloc[0] * 100).plot(title="Temperatura (prvi dan = 100)")
plt.show()
```

## 6.6 Razsevni graf: povezanost

```python
prodaja.plot.scatter(x="cena", y="prodano", title="Cena in prodaja")
plt.xlabel("cena (€)")
plt.ylabel("prodanih kosov")
plt.show()
print("Korelacija:", round(prodaja["cena"].corr(prodaja["prodano"]), 2))
```

Vsaka točka je en izdelek. Če točke tvorijo pas, ki pada od leve proti desni, je povezava negativna. Pri razsevnem grafu je smiselno izpisati še korelacijo.

## 6.7 Lastna funkcija za ponavljajoče grafe

Če isti tip grafa rišeš večkrat, ga zapri v funkcijo. Koda je krajša, pravila za eleganco kode pa to nagrajujejo.

```python
def narisi_lestvico(tabela, stolpec, n, naslov, barva="tab:blue"):
    """Nariše vodoravni stolpični graf n največjih vrednosti stolpca."""
    tabela.nlargest(n, stolpec)[stolpec].sort_values().plot.barh(
        title=naslov, color=barva
    )
    plt.show()


narisi_lestvico(prodaja.set_index("izdelek"), "prodano", 3, "Top 3 po prodaji")
narisi_lestvico(prodaja.set_index("izdelek"), "cena", 3, "Top 3 po ceni",
                barva="tab:orange")
```

## 6.8 Dober graf, kontrolni seznam

- [ ] naslov pove, **kaj** graf kaže
- [ ] osi imajo oznake **z enotami**
- [ ] pri lestvicah je največji na vrhu
- [ ] na isti osi niso različne enote
- [ ] pod grafom je besedilo z **ugotovitvijo**, ne le opis („Največ se proda kruha, skoraj dvakrat več kot jajc.“)
- [ ] pri primerjavi dveh grafov je opozorilo, če se merili razlikujeta
