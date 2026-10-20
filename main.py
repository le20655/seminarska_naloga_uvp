import os

import izluscenje
import orodja
import zajem

MAPA_PODATKOV = "podatki"
STOLPCI_SKLADI = [
    "sklad", "upravljavec", "upravljavec_id", "datum", "vep", "valuta",
    "donos_1d", "donos_6m", "donos_12m", "donos_60m",
]
STOLPCI_VEP = ["sklad", "datum", "vep"]


def main(ponovno_prenesi=False):
    """Prenese podatke, jih izlušči in shrani v dve CSV datoteki."""
    zajem.prenesi_tecajnico(ponovno_prenesi)
    tecajnica = orodja.preberi_niz(zajem.MAPA_SUROVO, zajem.DATOTEKA_TECAJNICA)
    skladi = izluscenje.izlusci_sklade(tecajnica)
    orodja.zapisi_csv(STOLPCI_SKLADI, skladi, MAPA_PODATKOV, "skladi.csv")
    print("Število skladov:", len(skladi))

    zajem.prenesi_vse_zgodovine(skladi, ponovno_prenesi)
    vrednosti = []
    for sklad in skladi:
        datoteka = zajem.ime_datoteke(sklad["sklad"])
        if os.path.exists(os.path.join(zajem.MAPA_VEP, datoteka)):
            vsebina = orodja.preberi_niz(zajem.MAPA_VEP, datoteka)
            vrednosti.extend(izluscenje.izlusci_vep(vsebina, sklad["sklad"]))
    orodja.zapisi_csv(STOLPCI_VEP, vrednosti, MAPA_PODATKOV, "vep.csv")
    print("Število vrednosti VEP:", len(vrednosti))


if __name__ == "__main__":
    main()
