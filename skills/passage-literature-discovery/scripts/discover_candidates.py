#!/usr/bin/env python3
"""Citation-snowballing discovery for the passage knowledge base.

Finds works cited by many included papers but NOT in the collection, ranks them
by in-collection citation frequency, and tags each with the mechanism themes of
the citing papers. Bibliographic output only.

Usage:
    python discover_candidates.py <pdf_folder> <repo_data_dir> -o candidate_additions.csv
    # <pdf_folder>  : local folder of the included PDFs (recursed; never committed)
    # <repo_data_dir>: the repo's data/ dir (needs corpus.csv + *_register.csv)

Requires `pdftotext` (Poppler). Title snippets are APPROXIMATE — verify before adding.
"""
import os, re, csv, sys, argparse, subprocess
from collections import defaultdict, Counter

HEAD=re.compile(r"\n\s*(references|literature cited|bibliography)\s*\n", re.I)
ENTRY=re.compile(r"([A-Z][A-Za-zÀ-ſ’'\-]{2,})\s*,\s*(?:[A-Z]\.?\s?){1,4}[^()\n]{0,200}?\(?((?:19[5-9]\d|20[0-2]\d))\)?")
STOP={"harbor","dam","river","lake","table","figure","appendix","report","university","national",
"department","abstract","introduction","discussion","results","methods","fish","water","pacific",
"northwest","hydro","turbine","energy","renewable","journal","proceedings","conference","volume",
"chapter","fisheries","ocean","marine","science","sciences","engineering","ecology","environmental",
"downstream","passage","available","received","published","corresponding","associates"}
def norm(s): return re.sub(r"[^a-z0-9]","",s.lower())

def refs_of(path):
    try: t=subprocess.run(["pdftotext","-q",path,"-"],capture_output=True,timeout=120).stdout.decode("utf-8","ignore")
    except Exception: return ""
    t=re.sub(r"[ \t]+"," ",t); ms=list(HEAD.finditer(t))
    return (t[ms[-1].end():] if ms else t[int(len(t)*0.7):])[:45000]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("pdf_folder"); ap.add_argument("data_dir")
    ap.add_argument("-o","--out",default="candidate_additions.csv"); ap.add_argument("--min",type=int,default=5)
    a=ap.parse_args()
    corpus=list(csv.DictReader(open(os.path.join(a.data_dir,"corpus.csv"),encoding="utf-8")))
    key_by_file={c["local_filename"]:c["citation_key"] for c in corpus}
    included=set(); inc_sn=defaultdict(set); sigs=[]
    for c in corpus:
        sn=re.sub(r"[^a-z]","",c["first_author"].lower()); included.add((sn,c["year"])); inc_sn[c["year"]].add(sn)
        tn=norm(c["title"]);  sigs.append(tn[:45]) if len(tn)>=20 else None
    mech=defaultdict(set)
    for m,fn in [("barotrauma","barotrauma_register.csv"),("collision","collision_register.csv"),("shear","shear_register.csv")]:
        p=os.path.join(a.data_dir,fn)
        if os.path.exists(p):
            for r in csv.DictReader(open(p,encoding="utf-8")): mech[r["citation_key"]].add(m)
    def is_inc_title(snip):
        s=norm(snip); return any(g and g in s for g in sigs)
    cand=defaultdict(lambda:{"citing":set(),"themes":Counter(),"titles":[]})
    for dp,_,fs in os.walk(a.pdf_folder):
        for f in sorted(fs):
            if not f.lower().endswith(".pdf"): continue
            K=key_by_file.get(f)
            if not K: continue
            seen=set(); refs=refs_of(os.path.join(dp,f)); mm=mech.get(K,set())
            for e in ENTRY.finditer(refs):
                sn=re.sub(r"[^a-z]","",e.group(1).lower()); yr=e.group(2)
                if len(sn)<3 or sn in STOP: continue
                if (sn,yr) in seen: continue
                seen.add((sn,yr))
                if (sn,yr) in included or sn in inc_sn.get(yr,()): continue
                snip=re.sub(r"\s+"," ",refs[e.end():e.end()+150])
                snip=re.split(r"\b(doi|https?|www\.|\[CrossRef\]|Crossref)\b",snip)[0].strip(" .,:;-")
                if is_inc_title(snip): continue
                cand[(sn,yr)]["citing"].add(K)
                for x in mm: cand[(sn,yr)]["themes"][x]+=1
                cand[(sn,yr)]["titles"].append((e.group(1),snip))
    rows=[]
    for (sn,yr),d in cand.items():
        n=len(d["citing"])
        if n<a.min: continue
        surname=Counter(t[0] for t in d["titles"]).most_common(1)[0][0]
        snip=max((t[1] for t in d["titles"]),key=len)[:110]
        themes="; ".join(f"{k}({v})" for k,v in d["themes"].most_common()) or "general/cross-cutting"
        rows.append((n,yr,surname,themes,snip,"; ".join(sorted(d["citing"])[:3])))
    rows.sort(key=lambda r:(-r[0],-int(r[1])))
    pri=lambda n:"High" if n>=10 else ("Medium" if n>=7 else "Low")
    with open(a.out,"w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh); # short_title_iso4 is left pending: compute it with iso4_abbreviate.py AFTER the
        # canonical title is resolved (abbreviating a raw reference parse is meaningless).
        w.writerow(["rank","priority","first_author","year","times_cited","themes","title_as_cited","short_title_iso4","example_citing","notes"])
        for i,(n,yr,surname,themes,snip,ex) in enumerate(rows,1):
            w.writerow([i,pri(n),surname,yr,n,themes,snip,"(pending canonical resolution)",ex,""])
    print(f"Wrote {len(rows)} candidates (>= {a.min} citing papers) to {a.out}")

if __name__=="__main__": main()
