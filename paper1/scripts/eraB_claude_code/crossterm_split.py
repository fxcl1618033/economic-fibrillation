"""Split the crisis-excess CROSS term into: correlation change (rho) vs swing-size change (sigma).
cross = sum_{i!=j} w_i w_j rho_ij s_i s_j.  Compare crisis-window means vs normal-window means.
Counterfactuals: cross(rho_crisis, s_normal), cross(rho_normal, s_crisis)."""
import numpy as np, pyreadr
from scipy.signal import butter, filtfilt
GLOBAL=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE','CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
N=len(CODES); WIN=10
md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
YEARS=np.arange(1970,2023); T=len(YEARS)
X=[]; LEV=[]
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    cyc=filtfilt(b,a,np.log(d.gdppc.values.astype(float))-np.log(d.gdppc.values.astype(float)).mean())
    s=dict(zip(d.year.values,cyc)); X.append([s[y] for y in YEARS])
    g=dict(zip(d.year.values,d.gdppc.values.astype(float)*d['pop'].values.astype(float))); LEV.append([g[y] for y in YEARS])
X=np.array(X); LEV=np.array(LEV)
for label,Wt in [("GDP-weighted",LEV/LEV.sum(0,keepdims=True)),("equal-weighted",np.ones((N,T))/N)]:
    rho=[];sd=[];ww=[];yrs=[]
    for t in range(WIN-1,T):
        seg=X[:,t-WIN+1:t+1]; seg=seg-seg.mean(1,keepdims=True)
        s=seg.std(1); C=np.corrcoef(seg); w=Wt[:,t]
        rho.append(C); sd.append(s); ww.append(w); yrs.append(YEARS[t])
    rho=np.array(rho); sd=np.array(sd); ww=np.array(ww); yrs=np.array(yrs)
    cm=np.isin(yrs,GLOBAL); nm=~cm
    off=~np.eye(N,dtype=bool)
    def cross(R,S,Wv): 
        M=np.outer(Wv*S,Wv*S)*R; return M[off].sum()
    # use mean structures of each regime
    Rc=rho[cm].mean(0); Rn=rho[nm].mean(0); Sc=sd[cm].mean(0); Sn=sd[nm].mean(0); Wc=ww[cm].mean(0); Wn=ww[nm].mean(0)
    base=cross(Rn,Sn,Wn); full=cross(Rc,Sc,Wc)
    only_rho=cross(Rc,Sn,Wn)-base; only_sd=cross(Rn,Sc,Wn)-base
    tot=full-base
    mr=lambda R:(R[off]).mean()
    print(f"\n{label}  (crisis windows: {list(yrs[cm])})")
    print(f"  mean pairwise corr: normal {mr(Rn):.3f} -> crisis {mr(Rc):.3f}")
    print(f"  mean cycle s.d.:    normal {Sn.mean():.4f} -> crisis {Sc.mean():.4f}  (x{Sc.mean()/Sn.mean():.2f})")
    print(f"  cross-term rise: total {tot:.2e} | from correlation alone {only_rho:.2e} ({only_rho/tot:.0%}) | from swing size alone {only_sd:.2e} ({only_sd/tot:.0%}) | interaction {(tot-only_rho-only_sd)/tot:.0%}")
