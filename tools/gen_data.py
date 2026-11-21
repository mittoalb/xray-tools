"""Generate the scattering-factor tables used by web/physics.js.

Writes web/data.json with, for each element:
  f'(E), |f''(E)| (xraylib Fi/Fii), total mass attenuation mu/rho(E) (cm^2/g),
  on a log energy grid 1-200 keV refined at every absorption edge;
and for crystal elements the atomic form factor f0(q), q = sin(theta)/lambda.
Also exports unit-cell atom lists for the supported crystals.
Run:  python3 tools/gen_data.py
"""
import json, os
import numpy as np
import xraylib as xl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'web', 'data.json')

ELEMENTS = ['B', 'C', 'N', 'O', 'Al', 'Si', 'Ti', 'V', 'Cr', 'Fe', 'Co', 'Ni', 'Cu',
            'Ga', 'Ge', 'As', 'Mo', 'Ru', 'Rh', 'Pd', 'In', 'Sb', 'La', 'Hf', 'Ta',
            'W', 'Ir', 'Pt', 'Au', 'Be', 'Sc', 'Y', 'Nb', 'Zr', 'Mg', 'F', 'Li', 'Ag', 'Re', 'Os']
CRYSTALS = {  # name in xraylib -> label, default Debye-Waller B (A^2, room temperature)
    'Si': ('Si', 0.4632), 'Ge': ('Ge', 0.5655), 'Diamond': ('Diamond (C)', 0.20),
    'InSb': ('InSb', 0.80), 'GaAs': ('GaAs', 0.60),
}
SHELLS = [xl.K_SHELL, xl.L1_SHELL, xl.L2_SHELL, xl.L3_SHELL,
          xl.M1_SHELL, xl.M2_SHELL, xl.M3_SHELL, xl.M4_SHELL, xl.M5_SHELL]
EMIN, EMAX = 1.0, 200.0


def sig(x, n=5):
    return float(f'{x:.{n}g}')


def grid_for(Z):
    base = np.geomspace(EMIN, EMAX, 520)
    extra = []
    for s in SHELLS:
        try:
            e = xl.EdgeEnergy(Z, s)
        except Exception:
            continue
        if EMIN < e < EMAX:
            extra += [e * (1 - 3e-5), e * (1 + 3e-5)]
    g = np.unique(np.concatenate([base, extra]))
    # drop base points that sit too close to an edge pair
    keep = [g[0]]
    for e in g[1:]:
        if e / keep[-1] - 1 > 2e-5:
            keep.append(e)
    return np.array(keep)


def main():
    data = {'meta': {'source': 'xraylib ' + getattr(xl, '__version__', ''),
                     'note': "fp = f' (Fi), fpp = |f''| (Fii), mu = total mass attenuation cm2/g"},
            'elements': {}, 'crystals': {}}
    qgrid = np.round(np.arange(0, 3.0001, 0.025), 4)
    crystal_Z = set()
    for cname in CRYSTALS:
        c = xl.Crystal_GetCrystal(cname)
        for a in c['atom']:
            crystal_Z.add(a['Zatom'])
    for sym in ELEMENTS:
        Z = xl.SymbolToAtomicNumber(sym)
        E = grid_for(Z)
        el = {'Z': Z, 'A': sig(xl.AtomicWeight(Z), 6),
              'rho': sig(xl.ElementDensity(Z), 4),
              'E': [sig(e, 7) for e in E],
              'fp': [sig(xl.Fi(Z, e), 4) for e in E],
              'fpp': [sig(abs(xl.Fii(Z, e)), 4) for e in E],
              'mu': [sig(xl.CS_Total(Z, e), 4) for e in E]}
        if Z in crystal_Z:
            el['f0'] = [sig(xl.FF_Rayl(Z, q) if q > 0 else Z, 5) for q in qgrid]
        data['elements'][sym] = el
    data['q'] = [float(q) for q in qgrid]
    for cname, (label, B) in CRYSTALS.items():
        c = xl.Crystal_GetCrystal(cname)
        data['crystals'][cname] = {
            'label': label, 'a': c['a'], 'b': c['b'], 'c': c['c'],
            'alpha': c['alpha'], 'beta': c['beta'], 'gamma': c['gamma'],
            'V': c['volume'], 'B': B,
            'atoms': [[xl.AtomicNumberToSymbol(a['Zatom']), a['fraction'],
                       a['x'], a['y'], a['z']] for a in c['atom']]}
    with open(OUT, 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    print('wrote', OUT, os.path.getsize(OUT) // 1024, 'kB')
    # same data as a script, so the page also works when opened from disk (file://)
    js = OUT[:-5] + '.js'
    with open(js, 'w') as f:
        f.write('window.XP_DATA = ' + json.dumps(data, separators=(',', ':')) + ';\n')
    print('wrote', js)
    missing = crystal_Z - {xl.SymbolToAtomicNumber(s) for s in ELEMENTS}
    assert not missing, missing


if __name__ == '__main__':
    main()
