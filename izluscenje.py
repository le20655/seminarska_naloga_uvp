import html
import json
import re

VZOREC_VRSTICE = re.compile(
    r'data-fund-name="(?P<sklad>[^"]+)"\s*'
    r"onclick=\"showChart\(this,'(?P<upravljavec_id>\w+)',"
    r"'(?P<upravljavec>[^']+)'.*?"
    r'class="col-date">\s*(?P<datum>[\d.]+)\s*</td>.*?'
    r'class="col-num">\s*(?P<vep>[\d.,]+)\s*</td>.*?'
    r'class="col-currency">\s*(?P<valuta>\w+)\s*</td>'
    r"(?P<donosi>.*?)</tr>",
    re.DOTALL,
)
VZOREC_DONOSA = re.compile(r'class="change-value">(.*?)</span>')
STOLPCI_DONOSOV = ["donos_1d", "donos_6m", "donos_12m", "donos_60m"]


def v_stevilo(niz):
    """Pretvori niz v slovenskem zapisu (npr. '1.234,56') v število.
    Če podatka ni (npr. '-'), vrne None."""
    niz = niz.strip().replace(".", "").replace(",", ".")
    try:
        return float(niz)
    except ValueError:
        return None


def v_iso_datum(niz):
    """Pretvori datum '16.10.2026' v '2026-10-16'."""
    dan, mesec, leto = niz.split(".")
    return f"{leto}-{mesec}-{dan}"


def izlusci_sklade(vsebina):
    """Iz HTML tečajnice izlušči seznam slovarjev, enega za vsak sklad."""
    skladi = []
    for ujemanje in VZOREC_VRSTICE.finditer(vsebina):
        donosi = VZOREC_DONOSA.findall(ujemanje["donosi"])
        sklad = {
            "sklad": html.unescape(ujemanje["sklad"]),
            "upravljavec": ujemanje["upravljavec"],
            "upravljavec_id": ujemanje["upravljavec_id"],
            "datum": v_iso_datum(ujemanje["datum"]),
            "vep": v_stevilo(ujemanje["vep"]),
            "valuta": ujemanje["valuta"],
        }
        for stolpec, donos in zip(STOLPCI_DONOSOV, donosi):
            sklad[stolpec] = v_stevilo(donos)
        skladi.append(sklad)
    return skladi


def izlusci_vep(vsebina, sklad):
    """Iz JSON odgovora izlušči seznam slovarjev (sklad, datum, vep).
    Stran nekatere dneve vrne dvakrat, zato v slovarju po datumih
    obdržimo le eno vrednost za vsak dan."""
    vep_po_datumih = {}
    for vrstica in json.loads(vsebina)["data"]:
        datum = vrstica["datum_formatted"].replace(",", "-")
        vep_po_datumih[datum] = float(vrstica["vep"])
    return [
        {"sklad": sklad, "datum": datum, "vep": vep}
        for datum, vep in sorted(vep_po_datumih.items())
    ]
