"""
MST / network-topology test (Mantegna Ch.13 method) on 26 economies' business cycles.
  d_ij = sqrt(2(1-rho_ij));  MST = minimum spanning tree over those distances.
Hypothesis: the correlation network CONTRACTS (MST length falls) before global recessions,
and network fragility rises (lambda_max of correlation matrix up => Kc ~ 1/lambda_max down).
Null = 5000 surrogate economy sets (spectrum preserved, cross-economy structure destroyed).
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt
from scipy.sparse.csgraph import minimum_spanning_tree
RNG=np.random.default_rng(303)
GLOBAL_REC=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
       'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
NSUR=5000; WIN=10; PRE=8; N=len(CODES)

md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
YEARS=np.arange(1962,2023); YI={y:i for i,y in enumerate(YEARS)}; T=len(YEARS)
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
X=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    lg=np.log(d.gdppc.values.astype(float)); cyc=filtfilt(b,a,lg-lg.mean())
    s=dict(zip(d.year.values,cyc)); X.append([s[y] for y in YEARS])
X=np.array(X)                                       # (N,T)

def corr_windows(Xa):
    """Xa (...,N,T) -> rolling corr matrices (...,T,N,N) (NaN before first full window)"""
    lead=Xa.shape[:-2]
    out=np.full(lead+(T,N,N),np.nan)
    for t in range(WIN-1,T):
        seg=Xa[...,:,t-WIN+1:t+1]
        seg=seg-seg.mean(axis=-1,keepdims=True)
        sd=seg.std(axis=-1,keepdims=True); sd=np.where(sd>0,sd,1e-12)
        z=seg/sd
        C=np.einsum('...it,...jt->...ij',z,z)/seg.shape[-1]
        out[...,t,:,:]=np.clip(C,-1,1)
    return out

def batch_mst_length(D):
    """D (B,N,N) dense distance -> total MST length (B,) via vectorized Prim."""
    B=D.shape[0]; idx=np.arange(B)
    intree=np.zeros((B,N),bool); intree[:,0]=True
    mind=D[:,0,:].copy(); mind[:,0]=np.inf
    total=np.zeros(B)
    for _ in range(N-1):
        masked=np.where(intree,np.inf,mind)
        j=np.argmin(masked,axis=1)
        total+=masked[idx,j]
        intree[idx,j]=True
        mind=np.minimum(mind,D[idx,j,:])
    return total

def stats_from_corr(C):
    """C (...,T,N,N) -> mean MST edge length L(t) and lambda_max(t), each (...,T)"""
    lead=C.shape[:-3]
    Lf=np.full(lead+(T,),np.nan); LM=np.full(lead+(T,),np.nan)
    flat=C.reshape(-1,T,N,N); B=flat.shape[0]
    Lo=np.full((B,T),np.nan); Mo=np.full((B,T),np.nan)
    for t in range(WIN-1,T):
        Ct=flat[:,t,:,:]
        D=np.sqrt(np.clip(2*(1-Ct),0,None))
        np.einsum('bii->bi',D)[...]=np.inf          # no self loops
        Lo[:,t]=batch_mst_length(D)/(N-1)           # mean edge length
        Mo[:,t]=np.linalg.eigvalsh(Ct)[:,-1]        # largest eigenvalue
    return Lo.reshape(lead+(T,)), Mo.reshape(lead+(T,))

IU=np.triu_indices(PRE,1)
def tau_pre(ind):
    taus=[]
    for o in GLOBAL_REC:
        idx=[YI[y] for y in range(o-PRE,o) if y in YI]
        if len(idx)<PRE: continue
        seg=ind[...,idx]
        if np.isnan(seg).all(axis=-1).any(): continue
        d=seg[...,IU[1]]-seg[...,IU[0]]
        taus.append(np.nansum(np.sign(d),axis=-1)/(0.5*PRE*(PRE-1)))
    return np.nanmean(np.stack(taus,axis=-1),axis=-1)

# ---------- REAL ----------
Creal=corr_windows(X)
L_real,M_real=stats_from_corr(Creal[None,...])
L_real=L_real[0]; M_real=M_real[0]
tauL=float(tau_pre(L_real)); tauM=float(tau_pre(M_real))
print("=== REAL ===")
print("MST mean edge length around crises:")
lags=np.arange(-4,4)
for o in GLOBAL_REC:
    row=" ".join(f"t{k:+d}={L_real[YI[o+k]]:.3f}" if (o+k) in YI and not np.isnan(L_real[YI[o+k]]) else f"t{k:+d}=  na " for k in lags)
    print(f"  {o}: {row}")
ep=np.array([[L_real[YI[o+k]] if (o+k) in YI else np.nan for k in lags] for o in GLOBAL_REC])
print("  MEAN: "+" ".join(f"t{k:+d}={v:.3f}" for k,v in zip(lags,np.nanmean(ep,axis=0))))
print(f"\npre-crisis trend tau:  MST length = {tauL:+.3f} (negative = contraction)   lambda_max = {tauM:+.3f} (positive = fragility up)")

# ---------- NULL: 5000 surrogate economy sets ----------
Xf=np.fft.rfft(X,axis=-1); amp=np.abs(Xf); nf=Xf.shape[-1]
BATCH=100; nullL=[]; nullM=[]
for s0 in range(0,NSUR,BATCH):
    nb=min(BATCH,NSUR-s0)
    rp=RNG.uniform(0,2*np.pi,size=(nb,N,nf)); rp[...,0]=0
    if T%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None,...]*np.exp(1j*rp),n=T,axis=-1)
    Cs=corr_windows(Xs)
    Ls,Ms=stats_from_corr(Cs)
    nullL.append(tau_pre(Ls)); nullM.append(tau_pre(Ms))
nullL=np.concatenate(nullL); nullM=np.concatenate(nullM)
pL=(1+np.sum(nullL<=tauL))/(1+len(nullL))     # contraction => lower tail
pM=(1+np.sum(nullM>=tauM))/(1+len(nullM))     # fragility  => upper tail
print(f"\n=== NULL ({NSUR} surrogate economy sets) ===")
print(f"  MST length : null mean {nullL.mean():+.3f}  5th pct {np.percentile(nullL,5):+.3f}   p(contraction) = {pL:.4f}")
print(f"  lambda_max : null mean {nullM.mean():+.3f}  95th pct {np.percentile(nullM,95):+.3f}  p(fragility)   = {pM:.4f}")

# ---------- centrality (real only) ----------
deg=np.zeros((T,N))
for t in range(WIN-1,T):
    D=np.sqrt(np.clip(2*(1-Creal[t]),0,None)); np.fill_diagonal(D,0)
    tree=minimum_spanning_tree(D).toarray(); tree=tree+tree.T
    deg[t]=(tree>0).sum(axis=1)
mean_deg=np.nanmean(deg[WIN-1:],axis=0)
top=np.argsort(-mean_deg)[:6]
print("\nmost central economies in the business-cycle MST (mean degree):")
for i in top: print(f"   {CODES[i]}: {mean_deg[i]:.2f}")

json.dump({"win":WIN,"pre":PRE,"nsur":NSUR,
 "tau_L":tauL,"p_contraction":float(pL),"tau_lambdamax":tauM,"p_fragility":float(pM),
 "nullL_mean":float(nullL.mean()),"nullM_mean":float(nullM.mean()),
 "epoch_lags":lags.tolist(),"epoch_L_mean":np.nanmean(ep,axis=0).tolist(),
 "L_by_year":{int(YEARS[i]):(float(L_real[i]) if not np.isnan(L_real[i]) else None) for i in range(T)},
 "lambdamax_by_year":{int(YEARS[i]):(float(M_real[i]) if not np.isnan(M_real[i]) else None) for i in range(T)},
 "central":{CODES[i]:float(mean_deg[i]) for i in top}},
 open("mst_results.json","w"),indent=2)
np.save("nullL.npy",nullL); np.save("nullM.npy",nullM)
print("\nsaved mst_results.json")
