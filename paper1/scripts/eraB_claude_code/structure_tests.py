"""
CRISIS STRUCTURE TESTS (built on Pangallo 2025 synchronization framing)
Test 1 — Fibrillation identity: world phasor Z = (1/N) sum A_j e^{i theta_j}
   |Z|^2 = Abar^2 * R_A^2,  R_A = |sum A_j e^{i theta_j}| / sum A_j  (amplitude-weighted alignment)
   Decompose log|Z|^2 crisis-vs-normal into: 2 log Abar (bigger swings) + 2 log R_A (more alignment).
Test 2 — Pangallo hierarchy: Fiedler split of correlation network into 2 blocs.
   r_within(t) = mean of each bloc's own order parameter; r_between(t) = |mean of bloc mean-phasors|
   Which rises before / at global recessions? Circular-shift permutation (exact, 52 shifts) + 5000 surrogates.
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr
RNG=np.random.default_rng(909)
GLOBAL=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE','CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
N=len(CODES)
md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
FULL=np.arange(1950,2023); YEARS=np.arange(1970,2023); T=len(YEARS); off=YEARS[0]-FULL[0]
Xf=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    s=dict(zip(d.year.values,np.log(d.gdppc.values.astype(float))))
    lg=np.array([s[y] for y in FULL]); Xf.append(filtfilt(b,a,lg-lg.mean()))
Xf=np.array(Xf)                        # (N, 73) full-length cycles (run-in)
G=np.isin(YEARS,GLOBAL).astype(float)

def phasors(Xfull):
    z=hilbert(Xfull,axis=-1)[...,off:]  # analyse 1970-2022 with run-in
    return np.abs(z), np.angle(z)

# ---------------- TEST 1: fibrillation identity ----------------
A,TH=phasors(Xf)
Z=(A*np.exp(1j*TH)).mean(axis=0)
Abar=A.mean(axis=0)
RA=np.abs((A*np.exp(1j*TH)).sum(axis=0))/A.sum(axis=0)
r=np.abs(np.exp(1j*TH).mean(axis=0))
chk=np.max(np.abs(np.abs(Z)**2-(Abar**2)*(RA**2)))
print(f"identity check max|err| = {chk:.2e}  (should be ~0)")
print(f"corr(R_A, r) = {pearsonr(RA,r)[0]:+.3f}  (amplitude-weighted vs plain alignment)")
cm=G==1; nm=~cm
lZ=np.log(np.abs(Z)**2); lA=2*np.log(Abar); lR=2*np.log(RA)
dZ=lZ[cm].mean()-lZ[nm].mean(); dA=lA[cm].mean()-lA[nm].mean(); dR=lR[cm].mean()-lR[nm].mean()
print(f"\ncrisis-vs-normal log world-swing^2: total {dZ:+.3f} = swings {dA:+.3f} + alignment {dR:+.3f}")
print(f"  share of crisis excess from ALIGNMENT = {dR/dZ:.1%}, from SWING SIZE = {dA/dZ:.1%}")
per={}
for g in GLOBAL:
    i=list(YEARS).index(g); per[g]=(lA[i]-lA[nm].mean(), lR[i]-lR[nm].mean())
    print(f"  {g}: swing {per[g][0]:+.2f}   alignment {per[g][1]:+.2f}")

# surrogate null for the alignment component dR (destroys cross-economy phase relations, keeps spectra)
F=np.fft.rfft(Xf,axis=1); amp=np.abs(F); nf=F.shape[1]; Tf=Xf.shape[1]
nullR=[]; nullA=[]
for s0 in range(0,5000,250):
    rp=RNG.uniform(0,2*np.pi,(250,N,nf)); rp[...,0]=0
    if Tf%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None]*np.exp(1j*rp),n=Tf,axis=-1)
    As,Ts=phasors(Xs)
    Ras=np.abs((As*np.exp(1j*Ts)).sum(axis=1))/As.sum(axis=1); Abs=As.mean(axis=1)
    lr=2*np.log(Ras); la=2*np.log(Abs)
    nullR.append(lr[:,cm].mean(1)-lr[:,nm].mean(1)); nullA.append(la[:,cm].mean(1)-la[:,nm].mean(1))
nullR=np.concatenate(nullR); nullA=np.concatenate(nullA)
pR=(1+np.sum(nullR>=dR))/5001; pA=(1+np.sum(nullA>=dA))/5001
print(f"  surrogate p(alignment excess)={pR:.4f}   p(swing excess)={pA:.4f}")

# ---------------- TEST 2: Pangallo hierarchy (Fiedler blocs) ----------------
C=np.corrcoef(Xf[:,off:])
W=np.clip(C,0,None); np.fill_diagonal(W,0)
deg=W.sum(1); Dm=np.diag(1/np.sqrt(deg)); Ln=np.eye(N)-Dm@W@Dm
ev,evec=np.linalg.eigh(Ln); fied=evec[:,1]
blocA=[CODES[i] for i in range(N) if fied[i]>=0]; blocB=[CODES[i] for i in range(N) if fied[i]<0]
print(f"\nFiedler split (lambda2={ev[1]:.3f}):\n  bloc A ({len(blocA)}): {blocA}\n  bloc B ({len(blocB)}): {blocB}")
ia=fied>=0; ib=~ia
def hier(TH):
    ea=np.exp(1j*TH[...,ia,:]).mean(axis=-2); eb=np.exp(1j*TH[...,ib,:]).mean(axis=-2)
    rw=(np.abs(ea)*ia.sum()+np.abs(eb)*ib.sum())/N
    rb=np.abs((np.exp(1j*np.angle(ea))+np.exp(1j*np.angle(eb)))/2)
    return rw,rb
rw,rb=hier(TH)
def lagcorr(x,lag):
    if lag>0: u,v=x[:-lag],G[lag:]
    elif lag<0: u,v=x[-lag:],G[:lag]
    else: u,v=x,G
    return pearsonr(u,v)[0]
def perm(x,lag,dirn):
    o=lagcorr(x,lag); nl=[]
    for k in range(1,T):
        Gs=np.roll(G,k)
        if lag>0: u,v=x[:-lag],Gs[lag:]
        elif lag<0: u,v=x[-lag:],Gs[:lag]
        else: u,v=x,Gs
        nl.append(pearsonr(u,v)[0])
    nl=np.array(nl)
    return o,((1+np.sum(nl>=o))/T if dirn=='pos' else (1+np.sum(nl<=o))/T)
print("\nlead-lag vs global recessions (circular-shift, floor 0.019):")
res={}
for name,x in [("r (all)",r),("r_within blocs",rw),("r_between blocs",rb)]:
    row=[]
    for lab,lag,dn in [("lead2",2,'pos'),("lead1",1,'pos'),("crisis",0,'pos'),("after2",-2,'neg')]:
        o,p=perm(x,lag,dn); row.append((lab,o,p))
    res[name]=row
    print(f"  {name:16s} "+"  ".join(f"{l} {o:+.2f}(p={p:.3f}){'*' if p<0.05 else ' '}" for l,o,p in row))
print(f"\ncorr(r_within, r_between) = {pearsonr(rw,rb)[0]:+.3f}")
print(f"mean r_within={rw.mean():.3f}  mean r_between={rb.mean():.3f}")

json.dump({"identity_err":float(chk),"dZ":float(dZ),"dA":float(dA),"dR":float(dR),
  "align_share":float(dR/dZ),"p_align":float(pR),"p_swing":float(pA),
  "per_crisis":{str(k):v for k,v in per.items()},"blocA":blocA,"blocB":blocB,"lambda2":float(ev[1]),
  "hier":{k:[(l,float(o),float(p)) for l,o,p in v] for k,v in res.items()},
  "series":{"year":YEARS.tolist(),"r":r.tolist(),"RA":RA.tolist(),"Abar":Abar.tolist(),"absZ":np.abs(Z).tolist(),"rw":rw.tolist(),"rb":rb.tolist()}},
  open("structure_results.json","w"),indent=1)
print("saved")
