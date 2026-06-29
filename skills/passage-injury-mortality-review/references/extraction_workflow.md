# How to read a passage paper quickly (for curation)

The mining script gives breadth; this is how to add depth on the papers that
matter. Aim for ~5 minutes per key paper.

1. **Abstract + last paragraph of intro** → the *primary* mechanism and the
   study's question. Fix the Mechanism column to what they actually test.
2. **Methods** → species, life stage, fish size (FL/TL, mass), sample size,
   acclimation depth, exposure parameters (pressure profile / strain rate /
   strike velocity / operating point), and study type. These populate the
   parameter columns; correct any mined values.
3. **Results — first table/figure** → the headline numbers: threshold values
   with units, dose–response, mortality/injury %. Put the single most important
   number in Thresholds/metrics and the headline in Outcome summary.
4. **Discussion — first two paragraphs** → the main claim and the assumptions
   they lean on (Boyle's vs dynamic, surrogacy, neutral buoyancy, transferability
   of CFD). This is the Hypotheses/assumptions column.
5. Set **Confidence = Verified**.

## Watch for
- Whether mortality is **immediate** or **delayed** (48–96 h) — they differ a
  lot; note it.
- **Control/handling/tag mortality** — net it out before quoting a mortality %.
- **Acclimation depth** — barotrauma numbers are meaningless without it.
- **Combined vs mechanism-specific** estimates (CFD survival often combined).
- **Units** — RPC (ratio) vs nadir (kPa) vs LRP (log); strain rate (s⁻¹) vs
  shear stress (Pa); %TDG. Never compare across units.
- **Duplicate outputs** of one study (conference vs journal vs preprint) — cite
  the definitive version.

## Quick mechanism cues
- chamber / decompression / swim bladder / nadir / RPC → Barotrauma
- jet / flume / strain rate / shear → Shear
- strike rig / leading edge / blade velocity → Blade strike
- CFD / RANS / particle / strike-probability → Numerical (record mechanism(s)
  modeled)
- HI-Z / balloon tag / telemetry / at a named dam → Field survival
