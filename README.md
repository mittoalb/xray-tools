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

## References

**Dynamical diffraction**

- S. Takagi, “A dynamical theory of diffraction for a distorted crystal”, J. Phys. Soc. Jpn. 26, 1239–1253 (1969). doi:10.1143/JPSJ.26.1239
- D. Taupin, “Théorie dynamique de la diffraction des rayons X par les cristaux déformés”, Bull. Soc. Fr. Minéral. Cristallogr. 87, 469–511 (1964).
- B. W. Batterman & H. Cole, “Dynamical diffraction of X rays by perfect crystals”, Rev. Mod. Phys. 36, 681–717 (1964). doi:10.1103/RevModPhys.36.681
- A. Authier, Dynamical Theory of X-ray Diffraction, IUCr Monographs on Crystallography 11, Oxford University Press (2001). Includes spherical-wave theory and the Borrmann fan.
- W. H. Zachariasen, Theory of X-ray Diffraction in Crystals, Wiley, New York (1945).
- S. Stepanov, X0h on the X-ray Server (extinction-length convention), https://x-server.gmca.aps.anl.gov/

**Monochromators and beam optics**

- T. Matsushita & H. Hashizume, “X-ray monochromators”, in Handbook on Synchrotron Radiation, Vol. 1, ed. E.-E. Koch, North-Holland, 261–314 (1983).
- J. W. M. DuMond, “Theory of the use of more than two successive X-ray crystal reflections to obtain increased resolving power”, Phys. Rev. 52, 872–883 (1937). doi:10.1103/PhysRev.52.872
- C. J. Sparks, B. S. Borie & J. B. Hastings, “X-ray monochromator geometry for focusing synchrotron radiation above 10 keV”, Nucl. Instrum. Methods 172, 237–242 (1980).

**Multilayers**

- L. G. Parratt, “Surface studies of solids by total reflection of X-rays”, Phys. Rev. 95, 359–369 (1954). doi:10.1103/PhysRev.95.359
- L. Névot & P. Croce, “Caractérisation des surfaces par réflexion rasante de rayons X”, Rev. Phys. Appl. 15, 761–779 (1980).
- D. L. Windt, “IMD: software for modeling the optical properties of multilayer films”, Computers in Physics 12, 360–370 (1998).

**Bent Laue crystals**

- P. Qi, X. Shi, N. Samadi & D. Chapman, “Focusing and energy dispersion properties of a cylindrically bent asymmetric Laue crystal”, Proc. SPIE 11108, 111080E (2019). doi:10.1117/12.2525449
- M. Martinson, N. Samadi, B. Bassey, A. Gomez & D. Chapman, “Phase-preserving beam expander for biomedical X-ray imaging”, J. Synchrotron Rad. 22, 801–806 (2015).
- Y. Zhu, N. Samadi, M. Martinson, B. Bassey, Z. Wei, G. Belev & D. Chapman, “Spectral K-edge subtraction imaging”, Phys. Med. Biol. 59, 2485–2503 (2014).
- P. Suortti, U. Lienert & C. Schulze, “Focusing monochromators for high energy synchrotron radiation”, Nucl. Instrum. Methods A 338, 27–32 (1994).
- P. Suortti, U. Lienert & C. Schulze, “Bent crystal optics for high energy synchrotron radiation”, AIP Conf. Proc. 389, 175–192 (1997).
- P. Penning & D. Polder, “Anomalous transmission of X-rays in elastically deformed crystals”, Philips Res. Rep. 16, 419–440 (1961).

**Scattering data**

- T. Schoonjans, A. Brunetti, B. Golosio, M. Sanchez del Rio, V. A. Solé, C. Ferrero & L. Vincze, “The xraylib library for X-ray–matter interactions. Recent developments”, Spectrochim. Acta B 66, 776–784 (2011). doi:10.1016/j.sab.2011.09.011
- A. Brunetti, M. Sanchez del Rio, B. Golosio, A. Simionovici & A. Somogyi, “A library for X-ray–matter interaction cross sections for X-ray fluorescence applications”, Spectrochim. Acta B 59, 1725–1731 (2004).
