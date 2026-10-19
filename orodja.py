import csv
import os

import requests

GLAVE = {"User-Agent": "Mozilla/5.0"}


def prenesi_stran(url):
    """Vrne vsebino spletne strani kot niz ali None, če pride do napake."""
    try:
        odgovor = requests.get(url, headers=GLAVE, timeout=30)
        odgovor.raise_for_status()
    except requests.exceptions.RequestException as napaka:
        print("Napaka pri prenosu:", url, napaka)
        return None
    return odgovor.text


def poslji_post(url, podatki):
    """Pošlje POST zahtevek s podatki in vrne odgovor kot niz ali None."""
    try:
        odgovor = requests.post(url, data=podatki, headers=GLAVE, timeout=30)
        odgovor.raise_for_status()
    except requests.exceptions.RequestException as napaka:
        print("Napaka pri prenosu:", url, napaka)
        return None
    return odgovor.text


def shrani_niz(besedilo, mapa, datoteka):
    """Zapiše niz v datoteko mapa/datoteka (mapo po potrebi ustvari)."""
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8") as izhod:
        izhod.write(besedilo)


def preberi_niz(mapa, datoteka):
    """Vrne celotno vsebino datoteke mapa/datoteka kot niz."""
    pot = os.path.join(mapa, datoteka)
    with open(pot, encoding="utf-8") as vhod:
        return vhod.read()


def zapisi_csv(stolpci, vrstice, mapa, datoteka):
    """Seznam slovarjev zapiše v CSV datoteko z danimi stolpci."""
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, "w", encoding="utf-8", newline="") as izhod:
        pisalec = csv.DictWriter(izhod, fieldnames=stolpci)
        pisalec.writeheader()
        pisalec.writerows(vrstice)
