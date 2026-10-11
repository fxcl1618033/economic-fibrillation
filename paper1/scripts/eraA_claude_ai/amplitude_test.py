"""
AMPLITUDE analysis. A_i(t) = |analytic signal| = size of economy i's business-cycle swing.
Note: r(t) uses ONLY phases (e^{i.theta}), so r and A are genuinely independent measurements
from the same pipeline -- not a transform of one another.
Q1: when the world synchronizes, do the swings also get bigger?  corr(r, Abar)
Q2: does amplitude rise before global recessions (same arc test as r)?
Confound checked: the Great Moderation (secular decline in macro volatility) -> test detrended too.
Null = 5000 surrogate economy sets.
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
from scipy.stats import pearsonr
RNG=np.random.default_rng(404)
GLOBAL_REC=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
       'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
NSUR=5000; N=len(CODES)
md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
YEARS=np.arange(1970,2023); YI={y:i for i,y in enumerate(YEARS)}; T=len(YEARS)
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
X=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    lg=np.log(d.gdppc.values.astype(float)); cyc=filtfilt(b,a,lg-lg.mean())
    s=dict(zip(d.year.values,cyc)); X.append([s[y] for y in YEARS])
X=np.array(X)

def r_and_A(Xa):
    z=hilbert(Xa,axis=-1)
    r=np.abs(np.exp(1j*np.angle(z)).mean(axis=-2))
    A=np.abs(z).mean(axis=-2)
    return r,A

r,A=r_and_A(X)
G=np.isin(YEARS,GLOBAL_REC).astype(float)

# ---- secular trend (Great Moderation check) ----
tr=gaussian_filter1d(A,8.0); Ad=A-tr
print(f"amplitude secular: A(1970s avg)={A[:10].mean():.4f}  A(1990-2006 avg)={A[YI[1990]:YI[2007]].mean():.4f}  A(2007-2022 avg)={A[YI[2007]:].mean():.4f}")

# ---- Q1: does synchronization go with bigger swings? ----
def perm_corr(x,y,nperm=None):
    obs=pearsonr(x,y)[0]
    null=np.array([pearsonr(x,np.roll(y,k))[0] for k in range(1,len(y))])
    return obs,(1+np.sum(null>=obs))/(1+len(null))
c_raw,p_raw=perm_corr(r,A)
c_det,p_det=perm_corr(r-gaussian_filter1d(r,8.0),Ad)
print(f"\nQ1 corr(r, amplitude):  raw = {c_raw:+.3f} (p={p_raw:.3f})   detrended = {c_det:+.3f} (p={p_det:.3f})")

# surrogate null for corr(r,A)
Xf=np.fft.rfft(X,axis=-1); amp=np.abs(Xf); nf=Xf.shape[-1]
BATCH=250; nullc=[]
for s0 in range(0,NSUR,BATCH):
    nb=min(BATCH,NSUR-s0)
    rp=RNG.uniform(0,2*np.pi,size=(nb,N,nf)); rp[...,0]=0
    if T%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None,...]*np.exp(1j*rp),n=T,axis=-1)
    rs,As=r_and_A(Xs)
    rs_d=rs-gaussian_filter1d(rs,8.0,axis=-1); As_d=As-gaussian_filter1d(As,8.0,axis=-1)
    rc=rs_d-rs_d.mean(axis=-1,keepdims=True); ac=As_d-As_d.mean(axis=-1,keepdims=True)
    nullc.append((rc*ac).mean(axis=-1)/(rc.std(axis=-1)*ac.std(axis=-1)))
nullc=np.concatenate(nullc)
p_sur=(1+np.sum(nullc>=c_det))/(1+len(nullc))
print(f"   vs {NSUR} surrogate economy sets: null mean {nullc.mean():+.3f}, 95th pct {np.percentile(nullc,95):+.3f}  ->  p = {p_sur:.4f}")

# ---- Q2: amplitude arc around global recessions ----
def lagcorr(x,g,lag):
    if lag>0: u,v=x[:-lag],g[lag:]
    elif lag<0: u,v=x[-lag:],g[:lag]
    else: u,v=x,g
    return pearsonr(u,v)[0]
def parc(x,lag,direction='pos'):
    obs=lagcorr(x,G,lag); null=np.array([lagcorr(x,np.roll(G,k),lag) for k in range(1,T)])
    p=(1+np.sum(null>=obs))/(1+len(null)) if direction=='pos' else (1+np.sum(null<=obs))/(1+len(null))
    return obs,p
print("\nQ2 amplitude arc (does the swing size rise before global recessions?)")
for lab,lag in [("2 yr before",2),("1 yr before",1),("crisis year",0),("1 yr after",-1),("2 yr after",-2)]:
    o,p=parc(A,lag); od,pd=parc(Ad,lag)
    print(f"   {lab:12s}: raw {o:+.3f} (p={p:.3f})   detrended {od:+.3f} (p={pd:.3f})")

lags=np.arange(-4,5)
ep=np.array([[A[YI[o+k]] if (o+k) in YI else np.nan for k in lags] for o in GLOBAL_REC])
print("\nsuperposed epoch, mean amplitude: "+"  ".join(f"t{k:+d}={v:.4f}" for k,v in zip(lags,np.nanmean(ep,axis=0))))

json.dump({"corr_r_A_raw":[c_raw,p_raw],"corr_r_A_detr":[c_det,p_det],"p_surrogate":float(p_sur),
 "null_mean":float(nullc.mean()),"epoch_lags":lags.tolist(),"epoch_A_mean":np.nanmean(ep,axis=0).tolist(),
 "A_by_year":{int(y):float(A[i]) for i,y in enumerate(YEARS)},
 "r_by_year":{int(y):float(r[i]) for i,y in enumerate(YEARS)}},
 open("amplitude_results.json","w"),indent=2)
np.save("null_corrA.npy",nullc)
print("\nsaved amplitude_results.json")
