import os
import re
import time

import orodja

URL_TECAJNICA = "https://zdu-giz.si/tecajnica/"
URL_ZGODOVINA = "https://zdu-giz.si/wp-admin/admin-ajax.php"

MAPA_SUROVO = os.path.join("podatki", "surovo")
MAPA_VEP = os.path.join(MAPA_SUROVO, "vep")
DATOTEKA_TECAJNICA = "tecajnica.html"


def ime_datoteke(sklad):
    """Iz imena sklada naredi ime datoteke, npr. 'NLB Skladi - Azija'
    -> 'nlb_skladi_azija.json'."""
    return re.sub(r"\W+", "_", sklad.lower()).strip("_") + ".json"


def prenesi_tecajnico(ponovno=False):
    """Prenese tečajnico vseh skladov, če še ni shranjena."""
    pot = os.path.join(MAPA_SUROVO, DATOTEKA_TECAJNICA)
    if os.path.exists(pot) and not ponovno:
        print("Tečajnica je že shranjena.")
        return
    vsebina = orodja.prenesi_stran(URL_TECAJNICA)
    if vsebina is not None:
        orodja.shrani_niz(vsebina, MAPA_SUROVO, DATOTEKA_TECAJNICA)
        print("Tečajnica prenesena.")


def prenesi_zgodovino(sklad, upravljavec_id):
    """Vrne zgodovino VEP enega sklada kot JSON niz. Stran podatke za graf
    naloži s POST zahtevkom, zato ga pošljemo sami."""
    podatki = {
        "action": "micustom_fetch_member_list_data",
        "table_type": upravljavec_id,
        "textVal": sklad,
    }
    return orodja.poslji_post(URL_ZGODOVINA, podatki)


def prenesi_vse_zgodovine(skladi, ponovno=False):
    """Za vsak sklad prenese zgodovino VEP, če še ni shranjena."""
    for sklad in skladi:
        datoteka = ime_datoteke(sklad["sklad"])
        if os.path.exists(os.path.join(MAPA_VEP, datoteka)) and not ponovno:
            continue
        vsebina = prenesi_zgodovino(sklad["sklad"], sklad["upravljavec_id"])
        if vsebina is not None:
            orodja.shrani_niz(vsebina, MAPA_VEP, datoteka)
            print("Prenesena zgodovina:", sklad["sklad"])
        time.sleep(1)  # strežnika ne obremenjujemo preveč
