"""
CORRELATION-DRIVEN FRAGILITY / LOSS OF DIVERSIFICATION  (GDP-weighted, real GDP)
World cyclical output: c_world(t) = sum_i w_i(t) * x_i(t), band-passed x_i, weights w_i = real GDP share.
Exact identity: Var_window(c_world) = sum_i w_i^2 Var(x_i) + sum_{i!=j} w_i w_j Cov(x_i,x_j)
  = OWN term (individual volatility)  +  CROSS term (co-movement / lost diversification).
Key test (non-circular): when global recessions hit, does the CROSS term or the OWN term drive the
world-variance spike?  Cross-term dominance => fragility is correlation-driven, not volatility-driven.
Null = 5000 surrogate economy sets (spectra preserved, cross-economy coupling destroyed).
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
from scipy.stats import pearsonr
RNG=np.random.default_rng(707)
GLOBAL_REC=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
       'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
NSUR=5000; WIN=10; N=len(CODES)
md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
YEARS=np.arange(1970,2023); YI={y:i for i,y in enumerate(YEARS)}; T=len(YEARS)

b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
X=[]; LEVEL=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md["pop"].notna())&(md.year>=1950)].sort_values('year')
    lg=np.log(d.gdppc.values.astype(float)); cyc=filtfilt(b,a,lg-lg.mean())
    s=dict(zip(d.year.values,cyc)); X.append([s[y] for y in YEARS])
    # real GDP level = gdppc * pop  (weights)
    gdp=(d.gdppc.values.astype(float)*d["pop"].values.astype(float)); g=dict(zip(d.year.values,gdp))
    LEVEL.append([g[y] for y in YEARS])
X=np.array(X); LEVEL=np.array(LEVEL)
W=LEVEL/LEVEL.sum(axis=0,keepdims=True)          # GDP weights per year (N,T)

def decompose(Xarr, Warr):
    """rolling own-term, cross-term, total world variance (trailing WIN). shapes (...,N,T)->(...,T)"""
    lead=Xarr.shape[:-2]
    own=np.full(lead+(T,),np.nan); cross=np.full(lead+(T,),np.nan); tot=np.full(lead+(T,),np.nan); rbar=np.full(lead+(T,),np.nan)
    for t in range(WIN-1,T):
        xs=Xarr[...,:,t-WIN+1:t+1]                # (...,N,WIN)
        w=Warr[...,:,t] if Warr.ndim==Xarr.ndim else Warr[:,t]
        xm=xs-xs.mean(axis=-1,keepdims=True)
        cov=np.einsum('...iw,...jw->...ij',xm,xm)/xs.shape[-1]   # (...,N,N)
        ww=np.einsum('...i,...j->...ij',w,w)
        diag=np.einsum('...ii->...i',cov)
        own_t=np.einsum('...i,...i->...',w*w,diag)
        tot_t=np.einsum('...ij,...ij->...',ww,cov)
        own[...,t]=own_t; cross[...,t]=tot_t-own_t; tot[...,t]=tot_t
        # weighted mean pairwise correlation
        sd=np.sqrt(np.clip(diag,1e-18,None))
        corr=cov/np.einsum('...i,...j->...ij',sd,sd)
        offw=ww.copy(); 
        eye=np.eye(N,dtype=bool)
        offw[...,eye]=0
        rbar[...,t]=np.einsum('...ij,...ij->...',offw,np.where(eye,0,corr))/np.clip(offw.sum(axis=(-1,-2)),1e-18,None)
    return own,cross,tot,rbar

own,cross,tot,rbar=decompose(X,W)
cross_share=cross/np.clip(tot,1e-18,None)

# link to r(t)
phase=np.angle(hilbert(X,axis=-1)); r=np.abs((W*np.exp(1j*phase)).sum(axis=0))  # GDP-weighted order param
print("GDP-weighted diversification analysis (real GDP, band-passed, WIN=10)")
print(f"corr( rbar(t), r(t) ) = {pearsonr(rbar[~np.isnan(rbar)], r[~np.isnan(rbar)])[0]:+.3f}")

# crisis vs normal: cross-share and its decomposition
gmask=np.isin(YEARS,GLOBAL_REC)&~np.isnan(cross_share)
nmask=(~np.isin(YEARS,GLOBAL_REC))&~np.isnan(cross_share)
print(f"\ncross-term SHARE of world variance:  global-recession yrs {np.nanmean(cross_share[gmask]):.3f}   normal yrs {np.nanmean(cross_share[nmask]):.3f}")
print(f"own-term (indiv volatility) level:   crisis {np.nanmean(own[gmask]):.2e}   normal {np.nanmean(own[nmask]):.2e}")
print(f"cross-term (co-movement) level:      crisis {np.nanmean(cross[gmask]):.2e}   normal {np.nanmean(cross[nmask]):.2e}")

# THE decomposition test: in crisis-vs-normal jump of total variance, how much is own vs cross?
d_own=np.nanmean(own[gmask])-np.nanmean(own[nmask])
d_cross=np.nanmean(cross[gmask])-np.nanmean(cross[nmask])
print(f"\nExcess world variance in crises: from OWN (volatility) = {d_own:.2e}   from CROSS (correlation) = {d_cross:.2e}")
print(f"  -> fraction of the crisis variance-excess due to CORRELATION = {d_cross/(d_own+d_cross):.1%}")

# surrogate null: is cross-share in crises higher than chance?
Xf=np.fft.rfft(X,axis=-1); amp=np.abs(Xf); nf=Xf.shape[-1]
obs=np.nanmean(cross_share[gmask])
BATCH=200; null=[]
for s0 in range(0,NSUR,BATCH):
    nb=min(BATCH,NSUR-s0)
    rp=RNG.uniform(0,2*np.pi,size=(nb,N,nf)); rp[...,0]=0
    if T%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None,...]*np.exp(1j*rp),n=T,axis=-1)
    Wb=np.broadcast_to(W,(nb,N,T))
    _,cs,to,_=decompose(Xs,Wb)
    csh=cs/np.clip(to,1e-18,None)
    null.append(np.nanmean(np.where(np.isin(YEARS,GLOBAL_REC)[None,:],csh,np.nan),axis=1))
null=np.concatenate(null)
p=(1+np.sum(null>=obs))/(1+len(null))
print(f"\nsurrogate null (5000 sets): crisis cross-share obs={obs:.3f}, null mean={np.nanmean(null):.3f}, p={p:.4f}")

json.dump({"win":WIN,"corr_rbar_r":float(pearsonr(rbar[~np.isnan(rbar)], r[~np.isnan(rbar)])[0]),
 "cross_share_crisis":float(np.nanmean(cross_share[gmask])),"cross_share_normal":float(np.nanmean(cross_share[nmask])),
 "excess_from_own":float(d_own),"excess_from_cross":float(d_cross),
 "corr_fraction_of_excess":float(d_cross/(d_own+d_cross)),"p_surrogate":float(p),
 "rbar_by_year":{int(y):(float(rbar[i]) if not np.isnan(rbar[i]) else None) for i,y in enumerate(YEARS)},
 "cross_by_year":{int(y):(float(cross[i]) if not np.isnan(cross[i]) else None) for i,y in enumerate(YEARS)},
 "own_by_year":{int(y):(float(own[i]) if not np.isnan(own[i]) else None) for i,y in enumerate(YEARS)},
 "tot_by_year":{int(y):(float(tot[i]) if not np.isnan(tot[i]) else None) for i,y in enumerate(YEARS)}},
 open("diversification_results.json","w"),indent=2)
np.save("div_null.npy",null)
print("saved diversification_results.json")
