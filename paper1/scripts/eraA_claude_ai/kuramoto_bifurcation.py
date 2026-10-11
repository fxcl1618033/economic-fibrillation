"""
Kuramoto coupling K as the bifurcation parameter.
Mean-field Kuramoto (Lorentzian natural frequencies):  r = sqrt(1 - Kc/K),  K>Kc
  =>  implied coupling   K/Kc = 1/(1 - r^2)
State variable = r.  Control parameter = K/Kc.  Transition at K/Kc = 1.
CSD prediction: recovery rate lambda -> 0 as K/Kc -> 1 (i.e. when coupling COLLAPSES).
Null = 5000 surrogate economy sets (spectrum preserved, coupling destroyed).
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
RNG=np.random.default_rng(202)
GLOBAL_REC=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
       'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
NSUR=5000; WIN=12; SIG=5.0
md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
YEARS=np.arange(1962,2023); YI={y:i for i,y in enumerate(YEARS)}; T=len(YEARS)

b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
X=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    lg=np.log(d.gdppc.values.astype(float)); cyc=filtfilt(b,a,lg-lg.mean())
    s=dict(zip(d.year.values,cyc)); X.append([s[y] for y in YEARS])
X=np.array(X)

def order_param(Xa):
    return np.abs(np.exp(1j*np.angle(hilbert(Xa,axis=-1))).mean(axis=-2))

def coupling(r):
    """implied K/Kc from mean-field Kuramoto inversion"""
    return 1.0/np.clip(1.0-r**2,1e-6,None)

def recovery_rate(r):
    """lambda(t) = -ln(phi), phi = rolling AR(1) of r-fluctuations. lambda->0 = critical slowing."""
    fl=r-gaussian_filter1d(r,SIG,axis=-1)
    shp=fl.shape[:-1]; lam=np.full(shp+(T,),np.nan)
    for t in range(WIN-1,T):
        seg=fl[...,t-WIN+1:t+1]; seg=seg-seg.mean(axis=-1,keepdims=True)
        x1,x2=seg[...,:-1],seg[...,1:]
        s1=x1.std(axis=-1); s2=x2.std(axis=-1)
        with np.errstate(invalid='ignore',divide='ignore'):
            phi=np.where((s1>0)&(s2>0),(x1*x2).mean(axis=-1)/(s1*s2),np.nan)
            phi=np.clip(phi,1e-4,0.9999)
            lam[...,t]=-np.log(phi)
    return lam

def post_minus_base(lam):
    """mean lambda in post-crisis window (t..t+2) minus mean elsewhere. Negative = slowing at transition."""
    post=[]; 
    for o in GLOBAL_REC:
        for k in [0,1,2]:
            if o+k in YI: post.append(YI[o+k])
    post=np.array(sorted(set(post)))
    mask=np.zeros(T,bool); mask[post]=True
    valid=~np.isnan(lam)
    with np.errstate(invalid='ignore'):
        mp=np.nanmean(np.where(mask,lam,np.nan),axis=-1)
        mb=np.nanmean(np.where(~mask,lam,np.nan),axis=-1)
    return mp-mb

# ---------- REAL ----------
r=order_param(X); KKc=coupling(r); lam=recovery_rate(r)
stat_real=float(post_minus_base(lam))

print("=== implied coupling K/Kc around each global recession ===")
L=np.arange(-3,4)
for o in GLOBAL_REC:
    row=[f"{KKc[YI[o+k]]:.1f}" if (o+k) in YI else " na " for k in L]
    print(f"  {o}:  " + "  ".join(f"t{k:+d}={v}" for k,v in zip(L,row)))
epochK=np.array([[KKc[YI[o+k]] if (o+k) in YI else np.nan for k in L] for o in GLOBAL_REC])
print("  MEAN:      " + "  ".join(f"t{k:+d}={v:.1f}" for k,v in zip(L,np.nanmean(epochK,axis=0))))

epochL=np.array([[lam[YI[o+k]] if (o+k) in YI else np.nan for k in L] for o in GLOBAL_REC])
print("\n=== recovery rate lambda (lower = slower recovery = closer to transition) ===")
print("  MEAN:      " + "  ".join(f"t{k:+d}={v:.2f}" for k,v in zip(L,np.nanmean(epochL,axis=0))))
print(f"\nstatistic: mean lambda(post-crisis t..t+2) - mean lambda(elsewhere) = {stat_real:+.4f}")

# ---------- 5000 SURROGATE ECONOMY SETS ----------
Xf=np.fft.rfft(X,axis=-1); amp=np.abs(Xf); nf=Xf.shape[-1]
BATCH=250; null=[]
for s0 in range(0,NSUR,BATCH):
    nb=min(BATCH,NSUR-s0)
    rp=RNG.uniform(0,2*np.pi,size=(nb,len(CODES),nf)); rp[...,0]=0
    if T%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None,...]*np.exp(1j*rp),n=T,axis=-1)
    null.append(post_minus_base(recovery_rate(order_param(Xs))))
null=np.concatenate(null)
p_low=(1+np.sum(null<=stat_real))/(1+len(null))
print(f"\nNULL = {NSUR} surrogate economy sets")
print(f"  null mean {null.mean():+.4f}   null 5th pct {np.percentile(null,5):+.4f}")
print(f"  p (slower recovery after crisis than chance, one-sided) = {p_low:.4f}")

json.dump({"stat_real":stat_real,"p_slowing_post":float(p_low),
 "null_mean":float(null.mean()),"null_p5":float(np.percentile(null,5)),
 "epoch_lags":L.tolist(),"epoch_KKc_mean":np.nanmean(epochK,axis=0).tolist(),
 "epoch_lambda_mean":np.nanmean(epochL,axis=0).tolist(),
 "KKc_by_year":{int(y):float(KKc[i]) for i,y in enumerate(YEARS)},
 "r_by_year":{int(y):float(r[i]) for i,y in enumerate(YEARS)}},
 open("kuramoto_bifurcation_results.json","w"),indent=2)
np.save("null_lambda.npy",null)
print("saved kuramoto_bifurcation_results.json")
