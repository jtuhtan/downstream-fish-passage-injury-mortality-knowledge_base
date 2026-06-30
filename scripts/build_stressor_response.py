#!/usr/bin/env python3
"""Validate the stressor-response dataset and build the explorer + summaries.

Reads data/stressor_response.csv, data/equations.csv and data/variables_units.csv,
validates them, STANDARDIZES all pressure values to kPa (with a traceability log),
prints a QA report, and renders a self-contained (no external dependencies)
docs/stressor_response.html with: filters (incl. Study), a WITHIN-METRIC
threshold/point dot-plot, the relationships table, the equations registry, the
variables & units table, and the unit-standardization log.

Pressure standardization (where & when, for traceability)
---------------------------------------------------------
* Canonical pressure unit is **kPa**.
* Conversion happens HERE, at build time, in `standardize_pressures()`. Every
  pressure value whose unit is not kPa is converted using `PRESSURE_TO_KPA` and
  recorded in the conversion log (printed below and shown in the explorer). The
  original value+unit is preserved in the row's `notes`.
* Curators should also enter pressures in kPa in the source CSV and note the
  original in `notes`; this step enforces and logs the standard regardless.

Run:
    python scripts/build_stressor_response.py
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SR = REPO / "data" / "stressor_response.csv"
EQ = REPO / "data" / "equations.csv"
VARS = REPO / "data" / "variables_units.csv"
OUT = REPO / "docs" / "stressor_response.html"

REQUIRED = ["relationship_id", "citation_key", "mechanism", "predictor",
            "response", "relationship_type", "source_location", "confidence"]

# --- pressure standardization (canonical unit = kPa) -----------------------
PRESSURE_TO_KPA = {           # multiply a value in <unit> by factor -> kPa
    "kpa": 1.0, "pa": 0.001, "psi": 6.894757, "bar": 100.0,
    "atm": 101.325, "mmhg": 0.1333224, "hpa": 0.1, "mpa": 1000.0,
}
PRESSURE_PREDICTORS = {"nadir_p", "accl_p", "dpdt"}  # dpdt is kPa/s; left as-is


def read_csv(p: Path) -> list[dict]:
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def validate(rows: list[dict]) -> list[str]:
    issues, seen = [], set()
    for i, r in enumerate(rows, start=2):
        rid = r.get("relationship_id", "").strip()
        for c in REQUIRED:
            if not r.get(c, "").strip():
                issues.append(f"row {i} ({rid or '?'}): missing required '{c}'")
        if rid and rid in seen:
            issues.append(f"row {i}: duplicate relationship_id '{rid}'")
        seen.add(rid)
        if r.get("predictor_value", "").strip() and not r.get("predictor_unit", "").strip():
            issues.append(f"row {i} ({rid}): predictor_value without predictor_unit")
        if r.get("confidence", "").strip() not in ("Mined", "Verified", ""):
            issues.append(f"row {i} ({rid}): confidence not Mined/Verified")
    return issues


def _conv_scalar(s: str, factor: float) -> str:
    s = s.strip()
    if not s:
        return s
    try:
        v = float(s) * factor
        return f"{v:.4g}"
    except ValueError:
        # a range like "8.2-19.2": convert both ends
        if "-" in s:
            a, _, b = s.partition("-")
            try:
                return f"{float(a)*factor:.4g}-{float(b)*factor:.4g}"
            except ValueError:
                return s
    return s


def standardize_pressures(rows: list[dict]) -> tuple[list[str], int]:
    """Convert every non-kPa pressure value to kPa in place; return (log, n_kpa)."""
    log: list[str] = []
    n_pressure = 0
    for r in rows:
        # predictor side
        unit = r.get("predictor_unit", "").strip().lower()
        if unit in PRESSURE_TO_KPA:
            n_pressure += 1
            if unit != "kpa":
                f = PRESSURE_TO_KPA[unit]
                orig_v = r.get("predictor_value", "").strip()
                orig_r = r.get("predictor_range", "").strip()
                r["predictor_value"] = _conv_scalar(r.get("predictor_value", ""), f)
                r["predictor_range"] = _conv_scalar(r.get("predictor_range", ""), f)
                r["predictor_unit"] = "kPa"
                orig = orig_v or orig_r
                r["notes"] = (r.get("notes", "") + f" [conv: {orig} {unit} x{f:g} -> kPa]").strip()
                log.append(f"{r['relationship_id']}: predictor {orig} {unit} x{f:g} -> "
                           f"{r['predictor_value'] or r['predictor_range']} kPa")
        # response side (only when the response is itself a pressure)
        runit = r.get("response_unit", "").strip().lower()
        is_press_resp = "pressure" in r.get("response", "").lower() or "nadir" in r.get("response", "").lower()
        if runit in PRESSURE_TO_KPA and is_press_resp:
            n_pressure += 1
            if runit != "kpa":
                f = PRESSURE_TO_KPA[runit]
                orig_v = r.get("response_value", "").strip()
                r["response_value"] = _conv_scalar(r.get("response_value", ""), f)
                r["response_unit"] = "kPa"
                r["notes"] = (r.get("notes", "") + f" [conv: response {orig_v} {runit} x{f:g} -> kPa]").strip()
                log.append(f"{r['relationship_id']}: response {orig_v} {runit} x{f:g} -> {r['response_value']} kPa")
    return log, n_pressure


def main() -> int:
    if not SR.exists():
        print(f"ERROR: {SR} not found", file=sys.stderr)
        return 1
    rows = read_csv(SR)
    eqs = read_csv(EQ) if EQ.exists() else []
    variables = read_csv(VARS) if VARS.exists() else []

    issues = validate(rows)
    conv_log, n_pressure = standardize_pressures(rows)

    print(f"stressor_response.csv: {len(rows)} relationships | equations.csv: {len(eqs)} | "
          f"variables_units.csv: {len(variables)}")
    print(f"pressure values (kPa-standardized): {n_pressure} | conversions applied: {len(conv_log)}")
    for c in conv_log:
        print("  conv:", c)
    if not conv_log:
        print("  (all source pressure values were already in kPa)")
    if issues:
        print(f"\nQA - {len(issues)} issue(s):")
        for s in issues:
            print("  -", s)
    else:
        print("\nQA: all rows pass required-field / unit / confidence checks.")

    n_num = sum(1 for r in rows if _is_num(r.get("predictor_value")))
    meta = {
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "n_rel": len(rows), "n_eq": len(eqs), "n_num": n_num,
        "issues": len(issues), "n_pressure": n_pressure,
        "conversions": conv_log,
        "pressure_factors": {k: v for k, v in PRESSURE_TO_KPA.items() if k != "kpa"},
    }
    html = (TEMPLATE
            .replace("__SR_DATA__", json.dumps(rows, ensure_ascii=False))
            .replace("__EQ_DATA__", json.dumps(eqs, ensure_ascii=False))
            .replace("__VARS_DATA__", json.dumps(variables, ensure_ascii=False))
            .replace("__META__", json.dumps(meta, ensure_ascii=False)))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"\nWrote explorer -> {OUT}")
    return 0


def _is_num(x):
    try:
        float(str(x).strip())
        return True
    except (TypeError, ValueError):
        return False


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Stress-Response Explorer for Downstream Fish Passage - Injury and Mortality</title>
<style>
:root{--bg:#fff;--fg:#1b2330;--mut:#5b6675;--line:#e3e8ef;--accent:#2563eb;--chip:#eef2f7}
*{box-sizing:border-box}
body{margin:0;font:14px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--fg);background:var(--bg)}
header{padding:18px 22px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:19px}
.sub{color:var(--mut);font-size:12.5px;margin-top:4px}
.wrap{padding:16px 22px;max-width:1180px;margin:0 auto}
.filters{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 16px}
.filters label{display:flex;flex-direction:column;font-size:11px;color:var(--mut);gap:3px}
select{padding:6px 8px;border:1px solid var(--line);border-radius:6px;font-size:13px;min-width:150px;background:#fff}
h2{font-size:15px;margin:22px 0 8px;border-bottom:1px solid var(--line);padding-bottom:5px}
.note{background:#fff8e6;border:1px solid #f0d98a;border-radius:8px;padding:9px 12px;font-size:12.5px;color:#6b5600;margin:10px 0}
.std{background:#eef6ff;border:1px solid #b9d4f5;border-radius:8px;padding:9px 12px;font-size:12.5px;color:#13447a;margin:10px 0}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{border:1px solid var(--line);padding:5px 7px;text-align:left;vertical-align:top}
th{background:var(--chip);position:sticky;top:0;font-size:11.5px;text-transform:uppercase;letter-spacing:.3px}
td.small{color:var(--mut);font-size:11.5px}
.tag{display:inline-block;padding:1px 6px;border-radius:10px;background:var(--chip);font-size:11px}
.v{font-weight:600}.mono{font-family:ui-monospace,Consolas,monospace}
.mined{color:#9a6a00}.verified{color:#0a7a2f}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0;font-size:11.5px}
.legend span{display:inline-flex;align-items:center;gap:4px}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.counts{color:var(--mut);font-size:12px;margin:4px 0 0}
.eqform{font-family:ui-monospace,Consolas,monospace;background:#f6f8fa;padding:1px 5px;border-radius:5px}
footer{color:var(--mut);font-size:11.5px;padding:14px 22px;border-top:1px solid var(--line);margin-top:24px}
</style></head><body>
<header>
  <h1>Stress-Response Explorer for Downstream Fish Passage &mdash; Injury and Mortality</h1>
  <div class="sub" id="sub"></div>
</header>
<div class="wrap">
  <div class="note"><b>Comparability rule:</b> thresholds and points are only comparable <b>within one metric</b>.
  Each metric (e.g. <code>rpc_AN = P<sub>A</sub>/P<sub>N</sub></code> vs <code>rpc_EA = P<sub>N</sub>/P<sub>A</sub></code>) gets its
  <b>own lane and axis</b> below &mdash; never read across lanes. Demonstrator data (mostly <span class="mined">Mined</span>); verify against source before use.</div>

  <div class="filters" id="filters"></div>

  <h2>Within-metric comparator (numeric thresholds &amp; points)</h2>
  <div class="legend" id="legend"></div>
  <div id="plot"></div>
  <div class="counts" id="plotcount"></div>

  <h2>Relationships <span class="counts" id="relcount"></span></h2>
  <div style="max-height:430px;overflow:auto;border:1px solid var(--line);border-radius:8px">
    <table id="reltable"></table>
  </div>

  <h2>Equations registry</h2>
  <div style="max-height:340px;overflow:auto;border:1px solid var(--line);border-radius:8px">
    <table id="eqtable"></table>
  </div>

  <h2>Variables &amp; physical units</h2>
  <div class="std" id="unitstd"></div>
  <div style="max-height:360px;overflow:auto;border:1px solid var(--line);border-radius:8px">
    <table id="vartable"></table>
  </div>

  <h2>Coverage</h2>
  <div id="coverage" class="counts"></div>
</div>
<footer id="foot"></footer>

<script>
var ROWS = __SR_DATA__;
var EQS  = __EQ_DATA__;
var VARS = __VARS_DATA__;
var META = __META__;
var PALETTE = ["#2563eb","#dc2626","#059669","#d97706","#7c3aed","#0891b2","#be185d","#65a30d","#475569","#ea580c"];

function tokens(s){ return (s||"").split(";").map(function(x){return x.trim();}).filter(Boolean); }
function uniqSorted(arr){ var s={}; arr.forEach(function(x){ if(x) s[x]=1; }); return Object.keys(s).sort(); }
function speciesList(){ var a=[]; ROWS.forEach(function(r){ a=a.concat(tokens(r.species)); }); return uniqSorted(a); }
function colorFor(sp){ var l=speciesList(); var i=l.indexOf(sp); return PALETTE[(i<0?0:i)%PALETTE.length]; }
function esc(s){ return (s==null?"":String(s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

var FILT={mechanism:"",predictor:"",response:"",species:"",citation_key:"",confidence:""};

function buildFilters(){
  var defs=[
    ["mechanism","Mechanism",uniqSorted(ROWS.map(function(r){return r.mechanism;}))],
    ["citation_key","Study",uniqSorted(ROWS.map(function(r){return r.citation_key;}))],
    ["predictor","Predictor (metric)",uniqSorted(ROWS.map(function(r){return r.predictor;}))],
    ["response","Response",uniqSorted([].concat.apply([],ROWS.map(function(r){return tokens(r.response);})))],
    ["species","Species",speciesList()],
    ["confidence","Confidence",uniqSorted(ROWS.map(function(r){return r.confidence;}))]
  ];
  var html="";
  defs.forEach(function(d){
    html+='<label>'+d[1]+'<select data-k="'+d[0]+'"><option value="">all</option>';
    d[2].forEach(function(o){ html+='<option>'+esc(o)+'</option>'; });
    html+='</select></label>';
  });
  var f=document.getElementById("filters"); f.innerHTML=html;
  f.querySelectorAll("select").forEach(function(sel){
    sel.addEventListener("change",function(){ FILT[sel.getAttribute("data-k")]=sel.value; render(); });
  });
}

function match(r){
  if(FILT.mechanism && r.mechanism!==FILT.mechanism) return false;
  if(FILT.citation_key && r.citation_key!==FILT.citation_key) return false;
  if(FILT.predictor && r.predictor!==FILT.predictor) return false;
  if(FILT.confidence && r.confidence!==FILT.confidence) return false;
  if(FILT.response && tokens(r.response).indexOf(FILT.response)<0) return false;
  if(FILT.species && tokens(r.species).indexOf(FILT.species)<0) return false;
  return true;
}

function renderPlot(rows){
  var pts=rows.filter(function(r){ return r.predictor_value!=="" && !isNaN(parseFloat(r.predictor_value)); });
  var lanesMap={};
  pts.forEach(function(r){ var k=r.predictor+"  ["+(r.predictor_unit||"?")+"]"; (lanesMap[k]=lanesMap[k]||[]).push(r); });
  var lanes=Object.keys(lanesMap).sort();
  var W=1080, padL=210, padR=70, laneH=46, top=10;
  var H=top+lanes.length*laneH+20;
  var svg='<svg width="100%" viewBox="0 0 '+W+' '+H+'" font-size="11" font-family="inherit">';
  lanes.forEach(function(lk,li){
    var arr=lanesMap[lk];
    var vals=arr.map(function(r){return parseFloat(r.predictor_value);});
    var mn=Math.min.apply(null,vals), mx=Math.max.apply(null,vals);
    if(mn===mx){ mn=mn-1; mx=mx+1; }
    var y=top+li*laneH+laneH/2, x0=padL, x1=W-padR;
    svg+='<text x="6" y="'+(y+3)+'" fill="#5b6675">'+esc(lk)+'</text>';
    svg+='<line x1="'+x0+'" y1="'+y+'" x2="'+x1+'" y2="'+y+'" stroke="#cdd5e0"/>';
    svg+='<text x="'+x0+'" y="'+(y+16)+'" fill="#9aa4b2">'+mn+'</text>';
    svg+='<text x="'+x1+'" y="'+(y+16)+'" text-anchor="end" fill="#9aa4b2">'+mx+'</text>';
    arr.forEach(function(r){
      var v=parseFloat(r.predictor_value), x=x0+(x1-x0)*((v-mn)/(mx-mn));
      var sp=tokens(r.species)[0]||"multiple";
      var t=r.relationship_id+"  |  "+r.predictor+"="+r.predictor_value+" "+(r.predictor_unit||"")
            +"  ->  "+r.response+(r.response_value?(" = "+r.response_value+(r.response_unit||"")):"")
            +"  |  "+sp+"  |  "+r.citation_key+" ("+r.source_location+")";
      svg+='<circle cx="'+x.toFixed(1)+'" cy="'+y+'" r="6" fill="'+colorFor(sp)+'" fill-opacity="0.82" stroke="#fff"><title>'+esc(t)+'</title></circle>';
    });
  });
  svg+='</svg>';
  if(!lanes.length) svg='<div class="counts">No numeric predictor points in the current filter (many rows are curves/categorical &mdash; see table).</div>';
  document.getElementById("plot").innerHTML=svg;
  document.getElementById("plotcount").textContent=pts.length+" numeric point(s) across "+lanes.length+" metric lane(s). Hover a dot for details.";
  var sps=uniqSorted([].concat.apply([],pts.map(function(r){return tokens(r.species);})));
  document.getElementById("legend").innerHTML=sps.map(function(s){
    return '<span><i class="dot" style="background:'+colorFor(s)+'"></i>'+esc(s)+'</span>';
  }).join("");
}

function renderTable(rows){
  var cols=[["citation_key","Study"],["predictor","Predictor"],["pv","Value"],["response","Response"],
            ["relationship_type","Type"],["effect_direction","Effect"],["species","Species"],
            ["structure_type","Structure"],["confidence","Conf."],["source_location","Source"],["notes","Notes"]];
  var h="<tr>"+cols.map(function(c){return "<th>"+c[1]+"</th>";}).join("")+"</tr>";
  rows.forEach(function(r){
    var pv=(r.predictor_value||r.predictor_range||"")+" "+(r.predictor_unit||"");
    var resp=r.response+(r.response_value?(" = "+r.response_value+(r.response_unit||"")):"");
    var cc=r.confidence==="Verified"?"verified":"mined";
    h+="<tr><td>"+esc(r.citation_key)+"</td><td>"+esc(r.predictor)+"</td><td class='v'>"+esc(pv.trim())+"</td>"
      +"<td>"+esc(resp)+"</td><td><span class='tag'>"+esc(r.relationship_type)+"</span></td>"
      +"<td>"+esc(r.effect_direction)+"</td><td class='small'>"+esc(r.species)+"</td>"
      +"<td class='small'>"+esc(r.structure_type)+"</td><td class='"+cc+"'>"+esc(r.confidence)+"</td>"
      +"<td class='small'>"+esc(r.source_location)+"</td><td class='small'>"+esc(r.notes)+"</td></tr>";
  });
  document.getElementById("reltable").innerHTML=h;
  document.getElementById("relcount").textContent=rows.length+" shown / "+ROWS.length+" total";
}

function renderEqs(){
  var cols=[["name","Model"],["predicts","Predicts"],["form","Form"],["equation","Equation"],
            ["domain_of_validity","Domain of validity"],["citation_key","Source"],["confidence","Conf."],["notes","Notes"]];
  var h="<tr>"+cols.map(function(c){return "<th>"+c[1]+"</th>";}).join("")+"</tr>";
  EQS.forEach(function(e){
    var cc=e.confidence==="Verified"?"verified":"mined";
    h+="<tr><td class='v'>"+esc(e.name)+"</td><td class='small'>"+esc(e.predicts)+"</td>"
      +"<td class='small'>"+esc(e.form)+"</td><td><span class='eqform'>"+esc(e.equation)+"</span></td>"
      +"<td class='small'>"+esc(e.domain_of_validity)+"</td><td class='small'>"+esc(e.citation_key)+(e.origin_citation_key?(" &larr; "+esc(e.origin_citation_key)):"")+"</td>"
      +"<td class='"+cc+"'>"+esc(e.confidence)+"</td><td class='small'>"+esc(e.notes)+"</td></tr>";
  });
  document.getElementById("eqtable").innerHTML=h;
}

function renderVars(){
  var cols=[["symbol","Symbol"],["quantity","Quantity"],["unit","Unit"],["definition","Definition"],["notes","Notes"]];
  var h="<tr>"+cols.map(function(c){return "<th>"+c[1]+"</th>";}).join("")+"</tr>";
  VARS.forEach(function(v){
    h+="<tr><td class='v mono'>"+esc(v.symbol)+"</td><td>"+esc(v.quantity)+"</td>"
      +"<td class='mono'>"+esc(v.unit)+"</td><td class='small'>"+esc(v.definition)+"</td>"
      +"<td class='small'>"+esc(v.notes)+"</td></tr>";
  });
  document.getElementById("vartable").innerHTML=h;
  // unit-standardization note + traceability log
  var f=META.pressure_factors||{};
  var fac=Object.keys(f).map(function(k){return k+" x"+f[k];}).join(", ");
  var conv=(META.conversions&&META.conversions.length)
    ? "<b>Conversions applied this build ("+META.conversions.length+"):</b><br>"+META.conversions.map(esc).join("<br>")
    : "All "+(META.n_pressure||0)+" source pressure values were already in <b>kPa</b> &mdash; 0 conversions needed.";
  document.getElementById("unitstd").innerHTML=
    "<b>Pressure standard:</b> all pressures are stored and shown in <b>kPa</b>. Conversion happens at build time in "
    +"<span class='mono'>scripts/build_stressor_response.py</span> (<span class='mono'>standardize_pressures()</span>), "
    +"with the original value kept in each row's <i>notes</i> for traceability. Factors: "+esc(fac)
    +". Depth (m) -> absolute kPa = 101.325 + 9.80665 &times; depth (freshwater).<br>"+conv;
}

function renderCoverage(rows){
  function tally(keyfn){ var m={}; rows.forEach(function(r){ keyfn(r).forEach(function(k){ if(k) m[k]=(m[k]||0)+1; }); });
    return Object.keys(m).sort(function(a,b){return m[b]-m[a];}).map(function(k){return k+" ("+m[k]+")";}).join(" &middot; "); }
  document.getElementById("coverage").innerHTML=
    "<b>By predictor:</b> "+tally(function(r){return [r.predictor];})+"<br>"
    +"<b>By response:</b> "+tally(function(r){return tokens(r.response);})+"<br>"
    +"<b>By study:</b> "+tally(function(r){return [r.citation_key];});
}

function render(){
  var rows=ROWS.filter(match);
  renderPlot(rows); renderTable(rows); renderCoverage(rows);
}

document.getElementById("sub").innerHTML=META.n_rel+" relationships &middot; "+META.n_eq+" equations &middot; "
  +META.n_num+" numeric points &middot; "+(META.n_pressure||0)+" pressures in kPa &middot; built "+META.built
  +(META.issues?(" &middot; "+META.issues+" QA issue(s)"):" &middot; QA clean");
document.getElementById("foot").innerHTML="Generated by scripts/build_stressor_response.py from data/stressor_response.csv + data/equations.csv + data/variables_units.csv. "
  +"No PDFs; metadata only. Demonstrator dataset &mdash; verify before citing.";
buildFilters(); renderEqs(); renderVars(); render();
</script>
</body></html>"""


if __name__ == "__main__":
    raise SystemExit(main())
