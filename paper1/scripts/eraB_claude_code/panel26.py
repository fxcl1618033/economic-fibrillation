"""All 26 economies: inside-the-swing anatomy + which CHANNEL carries the fibrillation signature.
Data: GMD (1950/60-2022). Channels (real = nominal/deflator): consumption, investment, exports, imports,
budget spending (govexp), budget balance (% GDP, level), short rate (level), real M2.
For each channel: band-pass 2-9y cycle per economy -> Hilbert phase -> Kuramoto r_k(t) across 26,
mean pairwise correlation pre/post 1990, lead-lag vs Kose-Terrones recessions (circular shift, floor 0.019),
and surrogate test of r_k level (is the channel synchronized beyond chance?)."""
import numpy as np, pandas as pd, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr
RNG=np.random.default_rng(2610)
C=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE','CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
GL=[1975,1982,1991,2009,2020]
G=pd.read_stata('ext/gmd/data/final/data_final.dta'); G=G[G.ISO3.isin(C)]
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
YEARS=np.arange(1970,2023); T=len(YEARS); Gv=np.isin(YEARS,GL).astype(float)
def series(iso,ch):
    d=G[G.ISO3==iso].sort_values('year').set_index('year')
    if ch=='GDP': s=np.log(d.rGDP)
    elif ch in ['cons','inv','exports','imports','govexp']: s=np.log(d[ch]/d.deflator)
    elif ch=='balance': s=d.govdef_GDP
    elif ch=='strate': s=d.strate
    elif ch=='M2': s=np.log(d.M2/d.deflator)
    s=s.replace([np.inf,-np.inf],np.nan).dropna(); s=s[(s.index>=1950)&(s.index<=2022)]
    return s
def cycle(s):
    # need contiguous coverage of 1965..2022 at least; interpolate tiny gaps
    idx=np.arange(int(s.index.min()),2023); s=s.reindex(idx).interpolate(limit=2)
    if int(s.index.min())>1965 or s.loc[1965:2022].isna().any() or len(s)<40: return None
    s=s.dropna(); x=s.values
    if np.isnan(x).any(): return None
    cyc=filtfilt(b,a,x-x.mean()); return pd.Series(cyc,index=s.index)
CH=['GDP','cons','inv','exports','imports','govexp','balance','strate','M2']
NAME={'GDP':'real GDP','cons':'consumption','inv':'investment','exports':'exports','imports':'imports',
      'govexp':'budget spending','balance':'budget balance','strate':'short-term rate','M2':'real money (M2)'}
def lagcorr(x,lag,Gs):
    if lag>0: u,v=x[:-lag],Gs[lag:]
    elif lag<0: u,v=x[-lag:],Gs[:lag]
    else: u,v=x,Gs
    return pearsonr(u,v)[0]
def perm(x,lag,dirn):
    o=lagcorr(x,lag,Gv); nl=np.array([lagcorr(x,lag,np.roll(Gv,k)) for k in range(1,T)])
    return o,((1+np.sum(nl>=o))/T if dirn=='pos' else (1+np.sum(nl<=o))/T)
res={}; RT={}
for ch in CH:
    cyc={}
    for iso in C:
        s=series(iso,ch); c=cycle(s) if len(s) else None
        if c is not None: cyc[iso]=c
    isos=list(cyc); M=np.array([cyc[i].reindex(YEARS).values for i in isos])
    full=[cyc[i] for i in isos]
    # phases with run-in: hilbert on full series, then take 1970-2022
    PH=np.array([np.angle(hilbert(cyc[i].values))[np.isin(cyc[i].index,YEARS)] for i in isos])
    r=np.abs(np.exp(1j*PH).mean(0)); RT[ch]=r
    # pairwise corr pre/post 1990
    def mpc(lo,hi):
        m=(YEARS>=lo)&(YEARS<=hi); cc=np.corrcoef(M[:,m]); iu=np.triu_indices(len(isos),1); return float(np.nanmean(cc[iu]))
    pre,post=mpc(1970,1989),mpc(1990,2022)
    # surrogate: is mean r above spectrum-preserving chance?
    XL=[cyc[i].values for i in isos]; L=min(len(x) for x in XL); Xs=np.array([x[-L:] for x in XL])
    F=np.fft.rfft(Xs,axis=1); amp=np.abs(F); nf=F.shape[1]; nr=[]
    for _ in range(40):
        rp=RNG.uniform(0,2*np.pi,(50,len(isos),nf)); rp[...,0]=0
        if L%2==0: rp[...,-1]=0
        S=np.fft.irfft(amp[None]*np.exp(1j*rp),n=L,axis=-1)
        ph=np.angle(hilbert(S,axis=-1))[...,-T:]; nr.append(np.abs(np.exp(1j*ph).mean(1)).mean(1))
    nr=np.concatenate(nr); p_sync=(1+np.sum(nr>=r.mean()))/(1+len(nr))
    row={'n':len(isos),'mean_r':float(r.mean()),'null_r':float(nr.mean()),'p_sync':float(p_sync),'paircorr_pre90':pre,'paircorr_post90':post}
    for lab,lag,dn in [('lead2',2,'pos'),('lead1',1,'pos'),('crisis',0,'pos'),('after2',-2,'neg')]:
        o,p=perm(r,lag,dn); row[lab]=(float(o),float(p))
    res[ch]=row
print(f"{'channel':16s} {'n':>3s} {'mean r':>7s} {'chance':>7s} {'p':>7s} | {'pair ρ 70-89':>12s} {'90-22':>6s} | lead2        lead1        crisis       after2")
for ch in CH:
    r=res[ch]; f=lambda t:f"{t[0]:+.2f}({t[1]:.3f}){'*' if t[1]<0.05 else ' '}"
    print(f"{NAME[ch]:16s} {r['n']:3d} {r['mean_r']:7.3f} {r['null_r']:7.3f} {r['p_sync']:7.4f} | {r['paircorr_pre90']:12.2f} {r['paircorr_post90']:6.2f} | {f(r['lead2'])} {f(r['lead1'])} {f(r['crisis'])} {f(r['after2'])}")
json.dump({'res':res,'r_t':{k:v.tolist() for k,v in RT.items()},'years':YEARS.tolist()},open('internal/panel26_results.json','w'),indent=1)
