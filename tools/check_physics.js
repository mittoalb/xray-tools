// Sanity checks of web/physics.js against reference values.  node tools/check_physics.js
const path = require('path');
const XP = require(path.join(__dirname, '../web/physics.js'));
XP.setData(require(path.join(__dirname, '../web/data.json')));
const urad = x => (x * 1e6).toFixed(2), asec = x => (x / XP.DEG * 3600).toFixed(3);
function bragg(cr, hkl, E, pol) {
  const rc = XP.rockingCurve({ crystal: cr, hkl, E, pol }, 2001);
  const f = XP.fwhm(rc.x, rc.R);
  console.log(`${cr}(${hkl.join('')}) ${E} keV ${pol||'sigma'}: thB=${(rc.sm.thB/XP.DEG).toFixed(4)}°  FWHM=${urad(f.fwhm)} urad (${asec(f.fwhm)}")  peak=${f.peak.toFixed(4)}  centre=${urad(f.xpeak)} urad  shift(analytic)=${urad(rc.sm.shift)}  dE/E=${(f.fwhm/Math.tan(rc.sm.thB)).toExponential(3)}  ext=${(rc.sm.extinction*1e-4).toFixed(3)} um  Iint=${urad(XP.trapz(rc.x, rc.R))} urad`);
}
bragg('Si', [1,1,1], 8.048);
bragg('Si', [1,1,1], 8.048, 'pi');
bragg('Si', [3,1,1], 8.048);
bragg('Si', [1,1,1], 20);
bragg('Ge', [1,1,1], 8.048);
bragg('Diamond', [1,1,1], 8.048);
bragg('Si', [3,3,3], 24.144);
const ch = XP.chis('Si',[1,1,1],8.048);
console.log('Si111 |Fh|', XP.C.abs(ch.Fh).toFixed(3), 'F0', ch.F0.map(v=>v.toFixed(3)), 'chi0', ch.chi0.map(v=>v.toExponential(4)), 'mu/cm', ch.mu_cm.toFixed(2));
// thin Bragg / Laue
const S = XP.crystalSetup({crystal:'Si',hkl:[2,2,0],E:17.48,geom:'laue',thickness:1e4*100});
console.log('Si220 Laue 17.48keV Pendellosung um', (XP.crystalSummary(S).pendellosung*1e-4).toFixed(2), 'darwin urad', urad(XP.crystalSummary(S).darwin));
// multilayer
const st = {A:{formula:'W',rho:19.25},B:{formula:'B4C',rho:2.52},sub:{formula:'Si',rho:2.33},d:25,gamma:0.4,N:100,sigma:3};
const ml = XP.mlAnalysis(st, 15, 1);
console.log('ML W/B4C d=25 G=.4 N=100 s=3 @15keV: th=',(ml.theta/XP.DEG).toFixed(4),'kin',(ml.thetaKin/XP.DEG).toFixed(4),'peak',ml.peak.toFixed(3),'dE/E',ml.dEE.toExponential(3),'angFWHM mrad',(ml.angFWHM*1e3).toFixed(4));
const ml2 = XP.mlAnalysis({...st, A:{formula:'Mo',rho:10.22}, B:{formula:'Si',rho:2.33}, d:70, N:40, sigma:0}, 10, 1);
console.log('ML Mo/Si d=70 N=40 s=0 @10keV: peak',ml2.peak.toFixed(3),'dE/E',ml2.dEE.toExponential(3));
// bent Laue magic condition vs Qi eq.10 small-angle tan chi = tan thB/(2+nu)
const o = {crystal:'Si',hkl:[1,1,1],E:33.17,nu:0.2,R_m:5,p_m:Infinity};
const chi = XP.magicChi(o); const th = Math.asin(XP.lambdaOf(33.17)/(2*XP.dSpacing('Si',1,1,1)));
console.log('magic chi', (chi/XP.DEG).toFixed(4), 'deg;  approx', (Math.atan(Math.tan(th)/2.2)/XP.DEG).toFixed(4), '; exact Qi eq9 residual', ((2.2)*Math.tan(chi)+0.2*Math.tan(th)*Math.tan(chi)**2+Math.tan(chi)**3-Math.tan(th)).toExponential(2));
const bl = XP.bentLaue({...o, chi, T_um:600, beam_mm:1});
console.log('bentLaue @magic: fg',bl.fg_m.toFixed(4),'fs',bl.fs_m.toFixed(4),'dE/E exit',bl.dEE_exit.toExponential(3),'dsp',bl.dEE_dsp.toExponential(3),'dE/E ray',bl.dEE_ray.toExponential(3),'Rpeak',bl.Rpeak.toFixed(3),'omegaD urad',urad(bl.omegaD));
// DCM harmonics
const an = XP.dcmAnalysis({crystal:'Si',hkl:[1,1,1],E:10,pol:'sigma',asym1:0,asym2:0,nmax:5});
an.harmonics.forEach(h=>console.log(' n',h.n,h.hkl.join(''),'F',h.F.toFixed(3),'peak',h.peak.toFixed(3),'fwhm urad',urad(h.fwhm),'relFlat',h.relFlat.toExponential(3), 'forbidden', h.forbidden));
