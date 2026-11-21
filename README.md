# xray-tools: Monochromator Workbench

Interactive calculators for X-ray monochromators:

| Tab | What it computes |
|---|---|
| Crystal DCM | Rocking curves (σ/π), Darwin width, ΔE/E (with divergence), refraction shift, extinction, harmonics n·(hkl) and detuning rejection, fixed-exit / channel-cut geometry over an energy range, asymmetric cuts |
| Multilayer DMM | Parratt reflectivity with roughness, bandpass (1 and 2 mirrors), full spectrum with higher orders, refraction-corrected angles, fixed-exit geometry |
| Bent Laue | Bandwidth (single ray / whole beam) vs bending radius, lamellar reflectivity, flat vs bent rocking curve, geometric and single-ray foci, magic-condition solver |
| Bent Bragg | Meridional and sagittal bending radii vs energy, asymmetric cuts |
| Reflection table | Every allowed reflection of a crystal at one energy with widths and resolution |

## Use

* Double-click `dist/monochromator-workbench.html` (self-contained, works offline apart from web fonts).
* Or open `web/index.html` directly (it needs `data.js` and `physics.js` beside it).

## Online (GitHub Pages)

`docs/index.html` is the deployable copy. In the repository, open Settings → Pages, choose
"Deploy from a branch", branch `main`, folder `/docs`. The page appears at
https://mittoalb.github.io/xray-tools/ after a minute.

After editing `web/`, run `python3 tools/build_standalone.py` to refresh `dist/` and `docs/`.

## Files

* `web/physics.js`: the physics engine (Takagi–Taupin two-beam solution, Parratt, bent-Laue model). Works in the browser or in Node.
* `web/data.js` (and `data.json`): f′, f″, μ/ρ and f₀ tables generated from xraylib (`python3 tools/gen_data.py`).
* `tools/check_physics.js`: reference checks (`node tools/check_physics.js`).
* `tools/build_standalone.py`: rebuilds the single-file version after edits.
