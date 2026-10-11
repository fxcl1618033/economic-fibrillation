import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
RNG=np.random.default_rng(101)
GLOBAL_REC=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
       'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
NSUR=5000; PRE=8; WIN=15; SIG=5.0

md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
YEARS=np.arange(1962,2023); YI={y:i for i,y in enumerate(YEARS)}; T=len(YEARS)

# ---- cyclical components (band-pass), matrix 26 x T ----
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
X=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    lg=np.log(d.gdppc.values.astype(float)); cyc=filtfilt(b,a,lg-lg.mean())
    s=dict(zip(d.year.values,cyc)); X.append([s[y] for y in YEARS])
X=np.array(X)                                   # (26, T)

def order_param(Xarr):
    """Xarr: (..., N, T) -> r(t): (..., T)"""
    ph=np.angle(hilbert(Xarr,axis=-1))
    return np.abs(np.exp(1j*ph).mean(axis=-2))

def roll_stats(r):
    """r: (..., T) -> rolling AR1 and VAR of fluctuations, (..., T)"""
    fl=r-gaussian_filter1d(r,SIG,axis=-1)
    shp=fl.shape[:-1]
    ar=np.full(shp+(T,),np.nan); va=np.full(shp+(T,),np.nan)
    for t in range(WIN-1,T):
        seg=fl[...,t-WIN+1:t+1]
        seg=seg-seg.mean(axis=-1,keepdims=True)
        x1,x2=seg[...,:-1],seg[...,1:]
        s1=x1.std(axis=-1); s2=x2.std(axis=-1)
        num=(x1*x2).mean(axis=-1)
        with np.errstate(invalid='ignore',divide='ignore'):
            ar[...,t]=np.where((s1>0)&(s2>0),num/(s1*s2),np.nan)
        va[...,t]=seg.var(axis=-1)
    return ar,va

# fast Kendall tau vs increasing index, vectorized over leading dims
IU=np.triu_indices(PRE,1)
def tau_pre(ind):
    """ind: (..., T) -> mean tau across the 5 crises, (...)"""
    taus=[]
    for o in GLOBAL_REC:
        idx=[YI[y] for y in range(o-PRE,o) if y in YI]
        if len(idx)<PRE: continue
        seg=ind[...,idx]                                  # (..., PRE)
        if np.isnan(seg).any(): 
            if np.isnan(seg).all(axis=-1).any(): continue
        diff=seg[...,IU[1]]-seg[...,IU[0]]
        taus.append(np.nansum(np.sign(diff),axis=-1)/(0.5*PRE*(PRE-1)))
    return np.nanmean(np.stack(taus,axis=-1),axis=-1)

# ---- REAL ----
r_real=order_param(X)
ar_r,va_r=roll_stats(r_real)
tau_ar_real=float(tau_pre(ar_r)); tau_va_real=float(tau_pre(va_r))

# ---- 5000 SURROGATE ECONOMY SETS (Fourier/phase-randomized, spectrum preserved) ----
Xf=np.fft.rfft(X,axis=-1); amp=np.abs(Xf); nf=Xf.shape[-1]
BATCH=250; null_ar=[]; null_va=[]
for s0 in range(0,NSUR,BATCH):
    nb=min(BATCH,NSUR-s0)
    rp=RNG.uniform(0,2*np.pi,size=(nb,len(CODES),nf)); rp[...,0]=0
    if T%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None,...]*np.exp(1j*rp),n=T,axis=-1)   # (nb,26,T)
    rs=order_param(Xs)                                          # (nb,T)
    a_,v_=roll_stats(rs)
    null_ar.append(tau_pre(a_)); null_va.append(tau_pre(v_))
null_ar=np.concatenate(null_ar); null_va=np.concatenate(null_va)

p_ar=(1+np.sum(null_ar>=tau_ar_real))/(1+len(null_ar))
p_va=(1+np.sum(null_va>=tau_va_real))/(1+len(null_va))

print(f"NULL = {NSUR} surrogate economy sets (spectrum-preserving, coupling destroyed)")
print(f"  AR1(r)  pre-crisis mean tau = {tau_ar_real:+.3f}   null mean {null_ar.mean():+.3f}   p = {p_ar:.4f}")
print(f"  VAR(r)  pre-crisis mean tau = {tau_va_real:+.3f}   null mean {null_va.mean():+.3f}   p = {p_va:.4f}")
print(f"  null 95th pct: AR1 {np.percentile(null_ar,95):+.3f} | VAR {np.percentile(null_va,95):+.3f}")

# per-crisis detail for VAR(r)
print("\nper-crisis VAR(r) trend tau:")
for o in GLOBAL_REC:
    idx=[YI[y] for y in range(o-PRE,o) if y in YI]
    if len(idx)<PRE: print(f"   {o}: insufficient pre-window"); continue
    seg=va_r[idx]; d=seg[IU[1]]-seg[IU[0]]
    print(f"   {o}: tau = {np.nansum(np.sign(d))/(0.5*PRE*(PRE-1)):+.2f}")

json.dump({"nsur":NSUR,"pre":PRE,"win":WIN,"sigma":SIG,
 "tau_ar_real":tau_ar_real,"p_ar":float(p_ar),
 "tau_va_real":tau_va_real,"p_va":float(p_va),
 "null_ar_mean":float(null_ar.mean()),"null_va_mean":float(null_va.mean()),
 "null_ar_p95":float(np.percentile(null_ar,95)),"null_va_p95":float(np.percentile(null_va,95))},
 open("csd_surrogate_results.json","w"),indent=2)
np.save("null_ar.npy",null_ar); np.save("null_va.npy",null_va)
print("\nsaved csd_surrogate_results.json")
