# 7. Jupyter in virtualno okolje

## 7.1 Virtualno okolje (`venv`)

Virtualno okolje je ločena mapa z lastnim Pythonom in knjižnicami za en projekt. Tako različni projekti ne vplivajo drug na drugega.

```bash
python3 -m venv venv           # ustvari okolje v mapi venv
source venv/bin/activate       # vklopi (Linux/Mac); Windows: venv\Scripts\activate
pip install requests pandas    # namesti knjižnice V TO okolje
deactivate                     # izklopi
```

- Ko je okolje vklopljeno, je na začetku vrstice v terminalu `(venv)`.
- Okolje vklopiš v **vsakem novem terminalu** znova.
- Mape `venv` ne daš v git, ker si jo vsak ustvari sam. V README napišeš, katere knjižnice so potrebne.

Pogoste napake:

| Sporočilo | Vzrok |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | okolje ni vklopljeno ali knjižnica ni nameščena |
| `Command 'python' not found` | izven okolja se Python imenuje `python3` |
| `venv/bin/activate: No such file or directory` | nisi v mapi projekta (`cd`) |

## 7.2 Jupyter Notebook

Zvezek (`.ipynb`) je zaporedje **celic**:
- **celice s kodo** se izvedejo, rezultat pa se prikaže pod njimi,
- **besedilne celice (Markdown)** vsebujejo razlago, naslove in ugotovitve.

### Jedro (kernel)

Jedro je Python, ki izvaja celice. V VS Code ga izbereš zgoraj desno (**Select Kernel**). Izbrati moraš Python iz svojega `venv`, sicer knjižnic ne najde.

### Stanje in vrstni red

- Spremenljivke ostanejo v pomnilniku med celicami. Celica 5 lahko uporabi spremenljivko iz celice 2.
- Številka `[7]` ob celici pove, **kdaj** je bila izvedena, ne kje stoji.
- Celice lahko izvajaš v poljubnem vrstnem redu, kar pa je past: zvezek lahko deluje pri tebi, pri drugem pa ne.
- **Pred oddajo vedno: Restart → Run All.** Vse se izvede od začetka po vrsti. Če ni napak, bo zvezek deloval tudi drugim.

### Bližnjice

| | |
|---|---|
| Shift+Enter | izvedi celico in pojdi na naslednjo |
| Ctrl+Enter | izvedi celico in ostani na njej |
| Esc, nato A / B | nova celica nad / pod trenutno |
| Esc, nato M / Y | spremeni v Markdown / kodo |
| Ctrl+S | shrani |

V VS Code shranjevanje **ni** samodejno, dokler ne vklopiš *File → Auto Save*. Neshranjen zavihek ima piko ● namesto ✕.

### Markdown na kratko

```markdown
# Naslov
## Podnaslov

Navaden odstavek. **krepko**, *poševno*, `koda`.

- alineja
- alineja

1. oštevilčeno
2. oštevilčeno

[besedilo povezave](https://example.com)

| stolpec | stolpec |
|---|---|
| a | b |
```

Ena nova vrstica v Markdownu **ne** začne novega odstavka. Za nov odstavek pusti prazno vrstico.

## 7.3 README.md

README je prva stran repozitorija na GitHubu. Bralcu pove:
1. **kaj** projekt je (2–3 stavki),
2. **kako ga zaženeš** (knjižnice, ukazi),
3. **katere datoteke** so v repozitoriju in kaj vsebujejo.

README **ni** analiza. Rezultate in razlage pojmov napišeš v zvezek.
