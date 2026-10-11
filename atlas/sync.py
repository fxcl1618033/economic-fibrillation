"""Channel synchronization r(t) across the 26 on the repaired panel (same method as internal/panel26.py):
band-pass 2-9y on each economy's series (1950-2022 run-in, needs coverage from 1965), Hilbert phase,
Kuramoto r(t) = |mean exp(i*theta)|, 1970-2022.  Lead-lag vs the five global recessions with circular-shift
permutation (floor 1/53).  Channels: real GDP (patched), real investment (deflator chosen per economy in
data.py), short-term interest rate (level)."""
import numpy as np, pandas as pd, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr
P=pd.read_csv('panel.csv'); META=json.load(open('meta.json')); FIX=META['fixes']; ISOS=[o[0] for o in META['order']]
G=pd.read_stata('/home/claude/ext/gmd/data/final/data_final.dta',columns=['ISO3','year','inv','CPI']); G['year']=G.year.astype(int)
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band'); YEARS=np.arange(1970,2023); T=len(YEARS)
GL=[1975,1982,1991,2009,2020]; Gv=np.isin(YEARS,GL).astype(float)
def series(iso,ch):
    d=P[P.iso==iso].set_index('year')
    if ch=='GDP': s=np.log(d.rGDP)
    elif ch=='inv':
        g=G[G.ISO3==iso].set_index('year').reindex(d.index)
        s=np.log(g.inv/(g.CPI if FIX[iso]['contrib_method']=='cpi' else d.deflator))
    elif ch=='strate': s=d.strate
    return s.replace([np.inf,-np.inf],np.nan)
def cycle(s):
    s=s.loc[1950:2022]; s=s.loc[s.first_valid_index():].interpolate(limit=2)
    if s.index.min()>1965 or s.loc[1965:2022].isna().any(): return None
    s=s.dropna(); return pd.Series(filtfilt(b,a,s.values-s.values.mean()),index=s.index)
def lagcorr(x,lag,g):
    u,v=(x[:-lag],g[lag:]) if lag>0 else ((x[-lag:],g[:lag]) if lag<0 else (x,g)); return pearsonr(u,v)[0]
out={'years':YEARS.tolist(),'r_t':{},'tests':{},'n':{}}
for ch in ['GDP','inv','strate']:
    cyc={i:cycle(series(i,ch)) for i in ISOS}; cyc={k:v for k,v in cyc.items() if v is not None}
    PH=np.array([np.angle(hilbert(c.values))[np.isin(c.index,YEARS)] for c in cyc.values()])
    r=np.abs(np.exp(1j*PH).mean(0)); out['r_t'][ch]=r.tolist(); out['n'][ch]=len(cyc)
    t={}
    for lab,lag,dn in [('lead2',2,1),('lead1',1,1),('same',0,1),('after2',-2,-1)]:
        o=lagcorr(r,lag,Gv); nl=np.array([lagcorr(r,lag,np.roll(Gv,k)) for k in range(1,T)])
        t[lab]=[round(float(o),3),round(float((1+np.sum(dn*nl>=dn*o))/T),3)]
    out['tests'][ch]=t
json.dump(out,open('sync.json','w'),indent=1)
for ch in out['tests']: print(ch,'n=',out['n'][ch],out['tests'][ch])
