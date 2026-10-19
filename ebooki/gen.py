import json,html
L=open('/mnt/project-files/kpp/strona/index.html',encoding='utf-8').read().split('\n')
def g(i,o,c): s=L[i]; return json.loads(s[s.index(o):s.rindex(c)+1])
Q=g(145,'[',']'); LS=g(146,'[',']'); PAT="https://patronite.pl/czakmed"; V=g(148,'{','}'); W=g(149,'[',']')
NOTES={44:"Tak brzmi klucz bazy egzaminacyjnej. Aktualne zalecenia nie zalecają prowokowania wymiotów; na egzaminie zaznaczasz odpowiedź z klucza."}
IMG={255:"Pytanie w oryginale zawiera rysunek (brak w tym wydaniu).",256:"Pytanie w oryginale zawiera rysunek (brak w tym wydaniu)."}
e=html.escape
for l in LS:
    for key in ("goal","task"): l[key]=l[key].replace("<","&lt;")
    l["points"]=[p.replace("<","&lt;") for p in l["points"]]; l["scenario"]=[p.replace("<","&lt;") for p in l["scenario"]]
# --- skrypt
o=["---\ntitle: 'Kurs KPP przed recertyfikacją'\nsubtitle: 'Skrypt: 20 lekcji w 4 tygodnie'\nlang: pl\n---\n",
"# Jak korzystać\n\nKurs ma 4 tygodnie po 5 lekcji. Każda lekcja to: cel, filmy, najważniejsze punkty do zapamiętania, scenariusz do przemyślenia i ćwiczenie praktyczne. Na końcu lekcji są numery pytań z bazy egzaminacyjnej (280 pytań), które znajdziesz w e-booku z fiszkami.\n\nFilmy oznaczone „Patronite” są na profilu [czakmed]("+PAT+") (wymagają zalogowania, szukaj po tytule w zakładce Filmy). Pozostałe filmy otwierają się na Dysku Google.\n"]
for i,l in enumerate(LS):
    if i%5==0: o.append(f"# Tydzień {i//5+1}: {W[i//5]}\n")
    o.append(f"## Lekcja {i+1}. {l['title']}\n\n*Czas: ok. {l['min']} min. Cel: {l['goal']}*\n\n### Filmy\n")
    for k in l['videos']:
        v=V[k]
        if len(v)>2: o.append(f"- [{v[0]}]({v[1] or PAT}) (Patronite)")
        else: o.append(f"- [{v[0]}](https://drive.google.com/file/d/{v[1]}/view)")
    o.append("\n### Zapamiętaj\n"); o+= [f"- {p}" for p in l['points']]
    o.append(f"\n### Scenariusz\n\n{l['scenario'][0]}\n\n> **Odpowiedź:** {l['scenario'][1]}\n\n### Ćwiczenie\n\n{l['task']}\n")
    o.append("### Pytania testowe\n\n"+(("Numery z bazy: "+", ".join(map(str,sorted(l['q'])))+".") if l['q'] else "Powtórka: losowe pytania z całej bazy (e-book z fiszkami).")+"\n")
open('skrypt.md','w').write("\n".join(o))
# --- fiszki
def card(q,ans):
    r=[f'<div class="card"><p class="nr">Pytanie {q["nr"]} z 280</p><p class="q">{e(q["question"])}</p>']
    if q['nr'] in IMG: r.append(f'<p class="note">{IMG[q["nr"]]}</p>')
    r.append('<ol class="opts">')
    for k,t in q['options'].items():
        ok=ans and k==q['correct']
        r.append(f'<li{' class="ok"' if ok else ""}><b>{k}.</b> {e(t)}{" ✔" if ok else ""}</li>')
    r.append('</ol>')
    if ans:
        r.append(f'<p class="key">Prawidłowa odpowiedź: <b>{q["correct"]}</b></p>')
        if q['nr'] in NOTES: r.append(f'<p class="note">{NOTES[q["nr"]]}</p>')
    r.append('</div>'); return "\n".join(r)
o=["---\ntitle: 'KPP: fiszki egzaminacyjne'\nsubtitle: '280 pytań testowych z odpowiedziami'\nlang: pl\n---\n",
"# Jak korzystać\n\nKażde pytanie zajmuje dwie strony: na pierwszej karta z pytaniem, na następnej ta sama karta z zaznaczoną prawidłową odpowiedzią. Odpowiedz w myślach, potem przewróć stronę.\n"]
for q in Q:
    n=q['nr']
    if (n-1)%20==0: o.append(f"# Pytania {n}–{min(n+19,280)}\n")
    o.append(f"## Pytanie {n} {{.unnumbered .hidden}}\n\n```{{=html}}\n{card(q,False)}\n```\n")
    o.append(f"## Pytanie {n}: odpowiedź {{.unnumbered .hidden}}\n\n```{{=html}}\n{card(q,True)}\n```\n")
open('fiszki.md','w').write("\n".join(o))
