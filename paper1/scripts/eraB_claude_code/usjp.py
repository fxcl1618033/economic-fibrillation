"""US vs Japan: what happens INSIDE each swing.
(1) Demand growth accounting (PWT): contribution of C, I, G, X, M to real GDP growth; variance share of each.
(2) Cross-country link by channel: US-JPN correlation of each component's business-cycle (2-9y band-pass of log real component).
(3) Budget & liquidity (GMD): fiscal balance, fiscal impulse (-Δbalance), real M2 growth, short rate; cyclicality vs GDP cycle."""
import numpy as np, pandas as pd, pyreadr, json
from scipy.signal import butter, filtfilt
from scipy.stats import pearsonr
P=pyreadr.read_r('ext/pwt10/data/pwt10.01.rda')['pwt10.01']
G=pd.read_stata('ext/gmd/data/final/data_final.dta')
b,a=butter(2,[(1/9)/0.5,0.49/0.5],btype='band')
COMP={'C':'csh_c','I':'csh_i','G':'csh_g','X':'csh_x','M':'csh_m'}
def comps(iso):
    d=P[(P.isocode==iso)&(P.year>=1955)].sort_values('year').set_index('year')
    Y=d.rgdpna
    K={k:(d[v]*Y) for k,v in COMP.items()}           # real component levels (M negative)
    g=100*Y.pct_change()
    con={k:100*K[k].diff()/Y.shift(1) for k in K}   # contribution to growth (pp)
    return Y,K,g,pd.DataFrame(con)
def bp(s):
    s=s.dropna(); x=np.log(np.abs(s.values)); return pd.Series(filtfilt(b,a,x-x.mean()),index=s.index)
out={}
for iso in ['USA','JPN']:
    Y,K,g,con=comps(iso)
    w=(g.index>=1961)&(g.index<=2019)
    gg=g[w]; cc=con[w]
    vs={k:float(np.cov(cc[k],gg)[0,1]/gg.var()) for k in cc}
    sd={k:float(cc[k].std()) for k in cc}
    out[iso]={'var_share':vs,'contrib_sd':sd,'gdp_growth_sd':float(gg.std()),
              'resid_share':float(1-sum(vs.values()))}
    print(f"\n{iso}: GDP growth s.d. {gg.std():.2f} pp")
    print("  share of GDP-growth variance carried by:  "+"  ".join(f"{k} {vs[k]:+.2f}" for k in vs)+f"   (residual {1-sum(vs.values()):+.2f})")
    print("  s.d. of each contribution (pp):            "+"  ".join(f"{k} {sd[k]:.2f}" for k in sd))
# (2) cross-country link per channel
YU,KU,_,_=comps('USA'); YJ,KJ,_,_=comps('JPN')
link={}
for k in ['C','I','G','X','M']:
    cu=bp(KU[k]); cj=bp(KJ[k]); ix=cu.index.intersection(cj.index); ix=ix[(ix>=1961)&(ix<=2019)]
    link[k]=float(pearsonr(cu[ix],cj[ix])[0])
cu=bp(YU); cj=bp(YJ); ix=cu.index.intersection(cj.index); ix=ix[(ix>=1961)&(ix<=2019)]
link['GDP']=float(pearsonr(cu[ix],cj[ix])[0])
print("\nUS-Japan cycle correlation by channel (2-9y band-pass):  "+"  ".join(f"{k} {v:+.2f}" for k,v in link.items()))
# split pre/post 1990
for lab,lo,hi in [("1961-1989",1961,1989),("1990-2019",1990,2019)]:
    row={}
    for k in ['C','I','G','X','M']:
        cu=bp(KU[k]); cj=bp(KJ[k]); ix=cu.index.intersection(cj.index); ix=ix[(ix>=lo)&(ix<=hi)]
        row[k]=pearsonr(cu[ix],cj[ix])[0]
    cu=bp(YU); cj=bp(YJ); ix=cu.index.intersection(cj.index); ix=ix[(ix>=lo)&(ix<=hi)]; row['GDP']=pearsonr(cu[ix],cj[ix])[0]
    print(f"   {lab}: "+"  ".join(f"{k} {v:+.2f}" for k,v in row.items()))
    out[f'link_{lab}']={k:float(v) for k,v in row.items()}
out['link']=link
# (3) budget & liquidity
for iso in ['USA','JPN']:
    d=G[(G.ISO3==iso)&(G.year>=1958)&(G.year<=2022)].sort_values('year').set_index('year')
    yc=pd.Series(filtfilt(b,a,np.log(d.rGDP.values)-np.log(d.rGDP.values).mean()),index=d.index)
    bal=d.govdef_GDP; imp=-bal.diff()                      # fiscal impulse: rise in deficit
    rm2=100*np.log(d.M2).diff()-d.infl                       # real money growth
    w=(d.index>=1961)&(d.index<=2022)
    c_bal=pearsonr(yc[w],bal[w])[0]; c_imp=pearsonr(yc[w],imp[w])[0]
    m=w&rm2.notna(); c_m2=pearsonr(yc[m],rm2[m])[0]
    out[iso].update({'corr_cycle_balance':float(c_bal),'corr_cycle_impulse':float(c_imp),'corr_cycle_realM2':float(c_m2),
       'mean_balance':float(bal[w].mean()),'debt_1970':float(d.govdebt_GDP.get(1970,np.nan)),'debt_2022':float(d.govdebt_GDP.get(2022,np.nan))})
    print(f"\n{iso} budget & liquidity (1961-2022):")
    print(f"  corr(GDP cycle, fiscal balance)  = {c_bal:+.2f}   (positive = automatic stabilizers: deficits widen in slumps)")
    print(f"  corr(GDP cycle, fiscal impulse)  = {c_imp:+.2f}   (negative = discretionary policy leans against the cycle)")
    print(f"  corr(GDP cycle, real M2 growth)  = {c_m2:+.2f}")
    print(f"  mean balance {bal[w].mean():+.1f}% GDP | debt {out[iso]['debt_1970']:.0f}% (1970) -> {out[iso]['debt_2022']:.0f}% (2022)")
json.dump(out,open('internal/usjp_results.json','w'),indent=1)
