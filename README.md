# Analiza slovenskih vzajemnih skladov

Projektna naloga pri predmetu Uvod v programiranje (FMF).

Program s strani [ZDU-GIZ](https://zdu-giz.si/tecajnica/) zajame podatke o vseh 72 slovenskih vzajemnih skladih (vrednost enote premoženja in donose) ter dnevno zgodovino vrednosti enote premoženja od leta 2022. V Jupyter zvezku analiziram, kateri skladi so v zadnjih petih letih prinesli največ in kateri najmanj, ali so obvezniški skladi premagali inflacijo, kako se primerjajo upravljalci in ali višji donos pomeni tudi večje tveganje.

## Ogled analize

Analiza je v datoteki [`analiza.ipynb`](analiza.ipynb). Na GitHubu se prikaže skupaj z vsemi grafi, zato za ogled ni treba ničesar nameščati.

## Zagon

Potrebuješ Python 3.10 ali novejši.

1. Kloniraj repozitorij in se premakni v njegovo mapo:
   ```bash
   git clone https://github.com/le20655/vzajemni-skladi.git
   cd vzajemni-skladi
   ```
2. Ustvari virtualno okolje in namesti knjižnice:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install requests pandas matplotlib jupyter
   ```
   Na Windows namesto `source venv/bin/activate` uporabi `venv\Scripts\activate`.
3. (Neobvezno) Ponovno zajemi podatke:
   ```bash
   python main.py
   ```
   Program prenese tečajnico in zgodovino vseh skladov (približno 1,5 minute) ter zapiše `podatki/skladi.csv` in `podatki/vep.csv`. Ker sta obe datoteki že v repozitoriju, lahko ta korak preskočiš.
4. Odpri analizo:
   ```bash
   jupyter notebook analiza.ipynb
   ```
   in izberi *Run → Run All Cells*.

## Datoteke

| Datoteka | Vsebina |
|---|---|
| `orodja.py` | pomožne funkcije za prenos strani, branje in pisanje datotek ter zapis CSV |
| `zajem.py` | prenos tečajnice (GET) in zgodovine VEP za vsak sklad (POST) |
| `izluscenje.py` | izluščenje podatkov iz HTML (regularni izrazi) in JSON |
| `main.py` | požene zajem in izluščenje ter zapiše obe CSV datoteki |
| `analiza.ipynb` | analiza in grafi |
| `podatki/skladi.csv` | en sklad na vrstico: upravljalec, VEP ter donosi za 1 dan, 6, 12 in 60 mesecev |
| `podatki/vep.csv` | zgodovina VEP: sklad, datum, vrednost |
| `uporaba-ui.md` | opis uporabe umetne inteligence in izpisi pogovorov |

Surove prenesene datoteke (`podatki/surovo/`) niso v repozitoriju, ker jih `main.py` ob zagonu ustvari sam.
