# 3. Zajem podatkov s spleta

## 3.1 Kako deluje splet: zahtevek in odgovor

Ko v brskalnik vpišeš naslov, brskalnik strežniku pošlje **zahtevek (request)**, strežnik pa vrne **odgovor (response)**. Ta pogovor poteka po protokolu **HTTP**.

Odgovor ima:
- **statusno kodo**: `200` pomeni OK, `404` pomeni, da stran ne obstaja, `403` dostop zavrnjen, `500` napaka na strežniku,
- **glave (headers)**: dodatne informacije, npr. vrsto vsebine,
- **telo (body)**: vsebino, npr. HTML, JSON ali sliko.

### GET in POST

| | GET | POST |
|---|---|---|
| namen | „daj mi to stran/podatke“ | „pošiljam ti podatke“ (obrazec, iskanje …) |
| kje so podatki | v naslovu: `...?q=python&stran=2` | v telesu zahtevka, v naslovu jih ni videti |
| primer | odpiranje strani, iskanje | prijava, oddaja obrazca, nalaganje podatkov za graf |

## 3.2 Knjižnica `requests`

Namestiš jo z `pip install requests`. Za primere uporabljam [httpbin.org](https://httpbin.org), testno stran, ki vrne nazaj, kar si ji poslal.

### GET

```python
import requests

odgovor = requests.get("https://httpbin.org/get", timeout=30)
print(odgovor.status_code)   # 200
print(odgovor.text[:100])    # vsebina kot niz
```

### POST

```python
odgovor = requests.post(
    "https://httpbin.org/post",
    data={"ime": "Ana", "leto": 2026},
    timeout=30,
)
print(odgovor.json()["form"])   # {'ime': 'Ana', 'leto': '2026'}
```

Razlika v kodi je majhna: namesto `requests.get` napišeš `requests.post` in podatke podaš z `data=`. Gredo v telo zahtevka, kot pri oddaji obrazca.

### Glave: `User-Agent`

Nekatere strani zavrnejo zahtevke, ki ne izgledajo, kot da prihajajo iz brskalnika. Z glavo `User-Agent` se predstaviš:

```python
GLAVE = {"User-Agent": "Mozilla/5.0"}
odgovor = requests.get("https://httpbin.org/headers", headers=GLAVE, timeout=30)
print(odgovor.json()["headers"]["User-Agent"])   # Mozilla/5.0
```

### `timeout`

Brez `timeout` program ob neodzivnem strežniku čaka v nedogled. S `timeout=30` po 30 sekundah sproži napako.

## 3.3 Napake pri prenosu

```python
def prenesi(url):
    """Vrne vsebino strani kot niz ali None, če prenos ne uspe."""
    try:
        odgovor = requests.get(url, headers=GLAVE, timeout=30)
        odgovor.raise_for_status()
    except requests.exceptions.RequestException as napaka:
        print("Napaka:", napaka)
        return None
    return odgovor.text


print(prenesi("https://httpbin.org/status/404"))   # izpiše napako in vrne None
```

- **`raise_for_status()`** sproži napako, če je statusna koda 4xx ali 5xx. Brez tega `requests` pri strani 404 vrne odgovor, kot da je vse v redu.
- **`RequestException`** je skupna napaka za vse težave s prenosom (ni povezave, timeout, 404 …).
- Funkcija ob napaki vrne `None`, zato mora klicatelj preveriti `if vsebina is not None:`.

## 3.4 JSON

**JSON** je zapis podatkov, ki ga uporablja večina spletnih vmesnikov. Izgleda kot Pythonovi slovarji in seznami:

```json
{"mesto": "Ljubljana", "meritve": [{"ura": 8, "t": 11.5}, {"ura": 14, "t": 17.0}]}
```

```python
import json

niz = '{"mesto": "Ljubljana", "meritve": [{"ura": 8, "t": 11.5}, {"ura": 14, "t": 17.0}]}'
podatki = json.loads(niz)               # niz -> slovar
print(podatki["meritve"][1]["t"])       # 17.0
```

Pri `requests` je `odgovor.json()` isto kot `json.loads(odgovor.text)`.

## 3.5 Kje strani dobijo podatke: orodja za razvijalce

Veliko strani ob prvem nalaganju ne vsebuje vseh podatkov. Ko klikneš gumb ali odpreš graf, JavaScript v ozadju pošlje dodaten zahtevek (**AJAX**) in podatke prejme kot JSON.

Kako ugotoviš, kateri zahtevek je to:
1. V brskalniku pritisni **F12** in odpri zavihek **Network** (Omrežje).
2. Izberi filter **Fetch/XHR**, ki prikaže le zahtevke JavaScripta.
3. Na strani naredi dejanje (klik, iskanje …).
4. Klikni na nov zahtevek:
   - **Headers:** naslov (URL) in metoda (GET/POST),
   - **Payload:** kaj je bilo poslano,
   - **Response:** kaj je strežnik vrnil.
5. Isti zahtevek nato ponoviš v Pythonu z `requests.get` ali `requests.post`.

To je pogosto lažje in hitreje kot avtomatiziran brskalnik (Selenium), ker dobiš podatke že v urejeni obliki JSON.

## 3.6 Lepo vedenje pri zajemanju

```python
import time

for stran in range(1, 4):
    vsebina = prenesi(f"https://httpbin.org/get?stran={stran}")
    time.sleep(1)    # med zahtevki počakaj
```

- Med zahtevki počakaj (`time.sleep`), da strežnika ne preobremeniš in te ne blokira.
- Prenesene strani shrani in jih ne prenašaj znova (glej datoteko 2, razdelek 2.4).
- Zajemaj le, kar potrebuješ.

## 3.7 HTML entitete

V HTML so nekateri znaki zapisani kot entitete:

```python
import html

print(html.unescape("Tom &amp; Jerry &quot;klasika&quot;"))  # Tom & Jerry "klasika"
```
