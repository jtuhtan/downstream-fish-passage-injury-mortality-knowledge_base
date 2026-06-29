# Study-type parameter templates & assumptions

Capture these parameters per study type. Each type answers a different question
and bakes in different assumptions — record both.

## Lab — pressure / barotrauma chamber
- Parameters: acclimation (neutral-buoyancy) depth/pressure, exposure pressure
  profile (onset → nadir), ratio of pressure change, exposure duration, species,
  life stage, fish size, n, holding/recovery time, injury scoring (necropsy/
  X-ray/transparent fish).
- Assumptions: fish neutrally buoyant at acclimation depth; Boyle's-law (static)
  vs. dynamic decompression; chamber profile ≈ real turbine nadir; surrogacy
  across species.

## Lab — shear flume / submerged jet
- Parameters: jet/nozzle velocity, computed strain rate (s⁻¹), introduction
  orientation (head/tail first), species/size, n, injury index by severity.
- Assumptions: single quasi-2D shear layer represents in-turbine shear; strain
  rate transfers across geometries.

## Lab — blade-strike apparatus / biomimetic
- Parameters: strike velocity, blade thickness/leading-edge geometry, strike
  location, fish length/orientation, n, mortality/injury by velocity.
- Assumptions: single clean strike; orientation distribution; sensor/biomimetic
  fish represents real tissue response.

## Field — survival / mark–recapture
- Parameters: site/turbine type & operating point, route, release/recapture
  method (HI-Z/balloon tag, netting), n released/recaptured, immediate vs.
  delayed (48–96 h) survival, controls for tag/handling, environmental
  conditions.
- Assumptions: control mortality captures handling/tag burden; recaptured sample
  is representative; immediate survival ≈ true survival.

## Field — telemetry / behaviour / Sensor Fish
- Parameters: tag type (acoustic/radio/PIT), array, route selection, Sensor Fish
  exposure traces (pressure, acceleration, rotation), n deployments.
- Assumptions: Sensor Fish exposure ≈ live-fish exposure; tagged fish behave
  normally; detection efficiency.

## Numerical — CFD / blade-strike / particle tracking
- Parameters: turbine geometry & operating point, solver (RANS/LES/finite
  volume/OpenFOAM), mesh, particle/Lagrangian or DEM scheme, exposure outputs
  (pressure field, nadir, strain rate, strike probability), coupling to dose–
  response (BioPA / bio-hill chart), validation data used.
- Assumptions: idealized/representative geometry & operating point; particles
  represent fish; dose–response transferable; steady vs. transient flow.

## Review / synthesis
- Parameters: scope, n studies, inclusion criteria, mechanisms covered,
  quantitative vs. narrative.
- Assumptions: comparability across heterogeneous methods.

## Guidelines / standards
- Parameters: jurisdiction, thresholds/criteria adopted, structures covered,
  basis (which science), intended use (design/permitting/assessment).
