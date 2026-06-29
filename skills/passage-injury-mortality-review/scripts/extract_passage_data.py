#!/usr/bin/env python3
"""Mine fish-passage injury/mortality PDFs into a structured CSV.

Usage:
    python extract_passage_data.py <folder_with_pdfs> -o extraction.csv

Requires `pdftotext` (poppler-utils) on PATH. Recurses subfolders. Categorical
fields (mechanism/species/life-stage/structure) are detected from the title +
early text to avoid reference-list noise; numeric fields (pressure ratios, kPa,
strain rate, mortality %, sample size, fish size) are mined from full text.
Output is a precision-leaning FIRST PASS — verify the rows that matter.
"""
import os, sys, re, csv, json, subprocess, argparse

MECH=[("Blade strike",r"blade[- ]?strike|blade strikes|leading edge|impact trauma|strike injur|mechanical strike"),
 ("Barotrauma/pressure",r"barotrauma|decompression|rapid pressure|nadir pressure|pressure change|\bRPC\b|\bLRP\b|swim ?bladder|boyle|depressuriz"),
 ("Shear",r"\bshear\b|fluid shear|shear stress|strain rate"),("Cavitation",r"cavitation"),
 ("Turbulence",r"turbulen"),("Grinding/abrasion/pinch",r"grinding|abrasion|\bpinch"),
 ("Gas supersaturation/GBT",r"supersaturation|gas bubble|total dissolved gas|\bTDG\b"),
 ("Entrainment/impingement/screen",r"entrainment|impingement|trash ?rack|fish screen")]
SPECIES=[("Chinook salmon (O. tshawytscha)",r"chinook|tshawytscha"),("Atlantic salmon (Salmo salar)",r"atlantic salmon|salmo salar"),
 ("Masu salmon (O. masou)",r"masu salmon|masou"),("Rainbow trout/steelhead (O. mykiss)",r"rainbow trout|steelhead|mykiss"),
 ("Sockeye/coho (Oncorhynchus)",r"sockeye|coho|nerka|kisutch"),("Bull trout (S. confluentus)",r"bull trout|confluentus"),
 ("Lake trout (S. namaycush)",r"lake trout|namaycush"),("American shad (A. sapidissima)",r"american shad|sapidissima"),
 ("Blueback herring (A. aestivalis)",r"blueback herring|aestivalis"),("Alewife (A. pseudoharengus)",r"alewife|pseudoharengus"),
 ("American eel (A. rostrata)",r"american eel|rostrata"),("European eel (A. anguilla)",r"european eel|anguilla anguilla|silver eel|yellow eel"),
 ("Lamprey",r"lamprey|petromyzon|entosphenus|lampetra"),("Murray cod (M. peelii)",r"murray cod|peelii"),
 ("Golden perch (M. ambigua)",r"golden perch|ambigua"),("Silver perch (B. bidyanus)",r"silver perch|bidyanus"),
 ("Crucian carp (Carassius)",r"crucian carp|carassius"),("Common carp (C. carpio)",r"common carp|cyprinus carpio"),
 ("Cyprinids (general)",r"cyprinid"),("Pictus catfish (P. pictus)",r"pictus"),("Pimelodus maculatus",r"maculatus"),
 ("Redfin perch (P. fluviatilis)",r"redfin|perca fluviatilis"),("Round goby (N. melanostomus)",r"round goby|melanostomus"),
 ("Bullhead (Cottus gobio)",r"bullhead|cottus gobio"),("Gudgeon (Gobio gobio)",r"gudgeon|gobio gobio"),
 ("White sturgeon (A. transmontanus)",r"white sturgeon|transmontanus|sturgeon"),("Mosquitofish (Gambusia)",r"gambusia"),
 ("Tilapia",r"tilapia|oreochromis"),("Brown trout (S. trutta)",r"brown trout|salmo trutta"),
 ("Salmonids (general)",r"salmonid"),("Smolts (unspec.)",r"\bsmolt")]
LIFE=[("Egg",r"\beggs?\b"),("Larva",r"larva|larvae|larval"),("Fry/fingerling",r"\bfry\b|fingerling"),
 ("Juvenile",r"juvenile"),("Smolt",r"smolt"),("Yearling/sub-adult",r"yearling|sub-?adult"),("Adult",r"\badult")]
STRUCT=[("Kaplan",r"kaplan"),("Francis",r"francis"),("Bulb",r"bulb turbine"),("Propeller/axial",r"propeller|axial[- ]?flow"),
 ("Pump",r"\bpump\b|pumping station|fish pump"),("Archimedean screw",r"archimed|screw turbine|screw pump"),
 ("Weir",r"\bweir"),("Spillway",r"spillway"),("Very Low Head (VLH)",r"very low head|\bVLH\b"),
 ("Hydrokinetic/MHK",r"hydrokinetic|\bMHK\b"),("Tidal",r"tidal"),("Shaft hydropower",r"shaft hydropower"),
 ("Siphon",r"siphon"),("Pumped storage",r"pumped[- ]?storage|pumped hydro"),("Vortex",r"vortex power|water vortex")]
METH=[("Pressure/barotrauma chamber",r"hyperbaric|hypobaric|pressure chamber|barotrauma chamber|barometric chamber|mobile aquatic barotrauma|depressuriz"),
 ("Shear flume/jet",r"shear flume|submerged jet|turbulent jet|shear environment|jet velocit|induced shear"),
 ("Blade-strike apparatus",r"blade[- ]?strike apparatus|striking apparatus|pneumatic|impact apparatus|simulated.{0,15}strike"),
 ("Sensor Fish",r"sensor fish|autonomous sensor"),
 ("CFD/numerical",r"\bcfd\b|computational fluid|numerical simul|finite volume|openfoam|\brans\b|lattice boltzmann|discrete element|particle tracking|lagrangian|immersed boundary"),
 ("Telemetry/tagging",r"telemetry|acoustic tag|radio tag|\bPIT\b|transmitter|acoustic camera|didson"),
 ("Mark-recapture/balloon-net",r"balloon tag|hi-?z|recaptur|stow[- ]?net|netting"),
 ("Imaging/necropsy/histology",r"x-ray|radiograph|necropsy|histolog"),
 ("In-situ field assessment",r"in situ|in-situ|field test|field-based|live[- ]fish"),
 ("Review/meta-analysis",r"literature review|systematic review|meta-analysis|: a review")]
HYP=[("Boyle's law",r"boyle"),("Henry's law",r"henry'?s law"),("Surrogacy across species",r"surrogac|surrogate species"),
 ("Dose-response",r"dose[- ]?response"),("Neutral buoyancy / acclimation depth",r"neutral buoyanc|acclimation depth|depth[- ]?acclimat"),
 ("Mechanistic threshold model",r"biological response model|barotrauma metric|mortal injury|threshold")]
PART={"van","Van","Ben","de","De","von","Von"}

def parse_name(f):
    n=re.sub(r"\.pdf$","",f,flags=re.I); t=n.split("_"); y=t[0]
    if len(t)>=4 and t[1] in PART: return y,t[1]+t[2]," ".join(t[4:])
    return y,(t[1] if len(t)>1 else "")," ".join(t[3:])
def det(lst,h): return [l for l,p in lst if re.search(p,h,re.I)]
def cnt(p,t): return len(re.findall(p,t,re.I))
def kpa(t): return sorted(set(re.findall(r"(\d{1,4}(?:\.\d+)?)\s?kpa",t,re.I)),key=lambda x:float(x))[:6]
def ratios(t):
    o=[]
    for m in re.finditer(r"(?:ratio of pressure change|log[- ]?ratio of pressure|\bLRP\b|\bRPC\b)[^.\n]{0,35}?(\d+(?:\.\d+)?)",t,re.I):
        o.append(re.sub(r"\s+"," ",m.group(0)).strip()[:45])
    return list(dict.fromkeys(o))[:4]
def strain(t): return list(dict.fromkeys(re.findall(r"(\d{2,4})\s?(?:s\s?[-−]\s?1|/s|s-1)",t)))[:6]
def nval(t): return list(dict.fromkeys(re.findall(r"\bn\s?=\s?(\d{1,5})",t)))[:8]
def pct(t):
    o=[]
    for m in re.finditer(r"(mortalit\w*|surviv\w*|injur\w*)[^.\n]{0,50}?(\d{1,3}(?:\.\d+)?)\s?%",t,re.I): o.append(f"{m.group(2)}% {m.group(1).lower()[:7]}")
    for m in re.finditer(r"(\d{1,3}(?:\.\d+)?)\s?%[^.\n]{0,25}?(mortalit\w*|surviv\w*)",t,re.I): o.append(f"{m.group(1)}% {m.group(2).lower()[:7]}")
    return list(dict.fromkeys(o))[:10]
def sizes(t):
    o=[]
    for m in re.finditer(r"(\d{2,3}(?:\.\d+)?)\s?(?:to|–|-|±)\s?(\d{2,3}(?:\.\d+)?)\s?(mm|cm)\b",t): o.append(f"{m.group(1)}-{m.group(2)} {m.group(3)}")
    for m in re.finditer(r"(?:fork length|total length|body length|mean length)[^.\d]{0,15}(\d{2,3}(?:\.\d+)?)\s?(mm|cm)",t,re.I): o.append(f"{m.group(1)} {m.group(2)}")
    return list(dict.fromkeys(o))[:6]

def mine(text, cat, fname):
    year,author,title=parse_name(fname)
    full=re.sub(r"[ \t]+"," ",text)
    focus=title+" \n "+full[:2200]
    mech=det(MECH,focus) or det(MECH,full[:6000])
    sp=det(SPECIES,title+" "+full[:3500])
    if not sp:
        sc=sorted(((l,cnt(p,full)) for l,p in SPECIES),key=lambda x:-x[1]); sp=[l for l,c in sc if c>=3][:4]
    st=det(STRUCT,focus) or det(STRUCT,full[:8000])
    meth=det(METH,focus)
    if cat=="Numerical" and "CFD/numerical" not in meth: meth=["CFD/numerical"]+meth
    thr=ratios(full)
    if kpa(full): thr.append("pressure kPa: "+", ".join(kpa(full)))
    if strain(full): thr.append("strain rate s-1: "+", ".join(strain(full)))
    return {"Year":year,"First author":author,"Category":cat,"Title":title,
      "Mechanism(s)":"; ".join(mech),"Species":"; ".join(sp[:6]),
      "Life stage":"; ".join(det(LIFE,title+" "+full[:5000])),"Fish size":"; ".join(sizes(full)),
      "Thresholds/metrics":"; ".join(thr),"Mortality/survival":"; ".join(pct(full)),
      "Sample size (n=)":"; ".join(nval(full)),"Turbine/structure":"; ".join(st),
      "Methodology":"; ".join(dict.fromkeys(meth)),"Hypotheses/assumptions":"; ".join(det(HYP,focus)),
      "Outcome summary":"","Confidence":"Mined","Notes":""}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("folder"); ap.add_argument("-o","--out",default="extraction.csv")
    a=ap.parse_args(); rows=[]
    for dp,_,fs in os.walk(a.folder):
        cat=os.path.basename(dp)
        for f in sorted(fs):
            if not f.lower().endswith(".pdf"): continue
            try: txt=subprocess.run(["pdftotext","-q",os.path.join(dp,f),"-"],capture_output=True,timeout=120).stdout.decode("utf-8","ignore")
            except Exception: txt=""
            rows.append(mine(txt,cat,f))
    cols=list(rows[0].keys()) if rows else []
    with open(a.out,"w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {a.out}")

if __name__=="__main__": main()
