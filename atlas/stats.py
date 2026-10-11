"""Per-country statistics, 1970-2022 (growth contributions 1971-2022)."""
import numpy as np, pandas as pd, json
P=pd.read_csv('panel.csv'); META=json.load(open('meta.json')); ORDER=META['order']+META.get('extra',[]); FIX=META['fixes']
GL=[1975,1982,1991,2009,2020]; OMEGA=2*np.pi/5.85
def nz(x): return None if (x is None or (isinstance(x,float) and np.isnan(x))) else x
def argext(s,fn):
    s=s.dropna()
    if not len(s): return (None,None)
    y=fn(s); return (float(s.loc[y]),int(P.loc[y,'year']) if False else None)
S={}
for iso,name,region in ORDER:
    d=P[P.iso==iso].set_index('year'); w=d.loc[1970:2022]; wc=d.loc[1971:2022]
    st={'iso':iso,'name':name,'region':region}
    g=w.growth.dropna()
    st['growth_mean']=g.mean(); st['growth_sd']=g.std(); st['worst']=(g.min(),int(g.idxmin())); st['best']=(g.max(),int(g.idxmax()))
    st['n_neg']=int((g<0).sum()); st['neg_years']=[int(y) for y in g[g<0].index]
    st['gr_global']={str(y):nz(float(d.growth.get(y,np.nan))) for y in GL}
    st['n_contract_global']=int(sum(1 for y in GL if d.growth.get(y,np.nan)<0))
    # swing anatomy
    cc=wc[['growth','c_C','c_I','c_NX']].dropna(); vg=cc.growth.var()
    st['anat']={k:float(np.cov(cc['c_'+k],cc.growth)[0,1]/vg) for k in ['C','I','NX']}
    st['anat']['resid']=1-sum(st['anat'].values()); st['anat_years']=(int(cc.index.min()),int(cc.index.max()))
    cc19=cc.loc[:2019]; vg19=cc19.growth.var()
    st['anat_pre2020']={k:float(np.cov(cc19['c_'+k],cc19.growth)[0,1]/vg19) for k in ['C','I','NX']}
    st['anat_n']=int(len(cc))
    # composition
    st['shares_from']=int(w.cons_GDP.first_valid_index())
    st['shares_1970']={k:nz(float(w[k+'_GDP'].dropna().iloc[0])) if w[k+'_GDP'].notna().any() else None for k in ['cons','inv','exports','imports']}
    st['shares_2022']={k:nz(float(d[k+'_GDP'].get(2022,np.nan))) for k in ['cons','inv','exports','imports']}
    # coupling to rest of world
    def cr(lo,hi):
        x=d.loc[lo:hi,['cycle','row_cycle']].dropna()
        return float(np.corrcoef(x.cycle,x.row_cycle)[0,1]) if len(x)>=8 else None
    st['coup_7089']=cr(1970,1989); st['coup_9022']=cr(1990,2022); st['coup_all']=cr(1970,2022)
    st['coup_dec']={lab:cr(lo,hi) for lab,lo,hi in [('1970s',1970,1979),('1980s',1980,1989),('1990s',1990,1999),('2000s',2000,2009),('2010-22',2010,2022)]}
    def al(lo,hi):
        x=d.loc[lo:hi,['phase','row_phase']].dropna(); return float(np.mean(np.cos(x.phase-x.row_phase)))
    st['align_7089']=al(1970,1989); st['align_9022']=al(1990,2022)
    x=d.loc[1970:2022,['phase','row_phase']].dropna()
    st['phase_offset_yrs']=float(np.angle(np.mean(np.exp(1j*(x.phase-x.row_phase))))/OMEGA)
    # rolling 10-y coupling
    roll={}
    for y in range(1979,2023):
        x=d.loc[y-9:y,['cycle','row_cycle']].dropna(); roll[y]=float(np.corrcoef(x.cycle,x.row_cycle)[0,1]) if len(x)>=8 else None
    st['coup_roll']=roll
    # budget
    def dm(col,lo,hi):
        s=d.loc[lo:hi,col].dropna(); return float(s.mean()) if len(s) else None
    st['spend_70s']=dm('govexp_GDP',1970,1979); st['spend_10s']=dm('govexp_GDP',2010,2022)
    st['rev_70s']=dm('govrev_GDP',1970,1979); st['rev_10s']=dm('govrev_GDP',2010,2022)
    bal=w.govdef_GDP.dropna(); st['bal_mean']=float(bal.mean()); st['bal_worst']=(float(bal.min()),int(bal.idxmin()))
    st['fiscal_from']=int(bal.index.min()); st['bal_best']=(float(bal.max()),int(bal.idxmax()))
    st['spend_first']=(float(w.govexp_GDP.dropna().iloc[0]),int(w.govexp_GDP.dropna().index[0])); st['spend_2022']=nz(float(d.govexp_GDP.get(2022,np.nan)))
    st['spend_peak']=(float(w.govexp_GDP.max()),int(w.govexp_GDP.idxmax()))
    st['bal_surplus_years']=int((bal>0).sum())
    xb=w[['cycle','govdef_GDP']].dropna(); st['bal_cyc']=float(np.corrcoef(xb.cycle,xb.govdef_GDP)[0,1])
    db=w.govdebt_GDP.dropna(); st['debt_start']=(float(db.iloc[0]),int(db.index[0])); st['debt_2022']=float(db.loc[2022]) if 2022 in db.index else None
    st['debt_low']=(float(db.min()),int(db.idxmin()))
    st['debt_peak']=(float(db.max()),int(db.idxmax()))
    # rates, inflation, money
    inf=w.infl.dropna(); st['infl_mean']=float(inf.mean()); st['infl_peak']=(float(inf.max()),int(inf.idxmax()))
    st['infl_median']=float(inf.median())
    sr=w.strate.dropna(); st['strate_start']=int(sr.index.min()) if len(sr) else None
    RR_FROM={'BRA':1995}       # before the 1994 Real Plan, nominal-minus-inflation is meaningless under hyperinflation
    rr=w.real_strate.loc[RR_FROM.get(iso,1970):].dropna(); st['rr_mean']=float(rr.mean()) if len(rr) else None; st['rr_from']=RR_FROM.get(iso)
    st['rr_neg_years']=int((rr<0).sum()) if len(rr) else None
    z=sr[sr<=0.5]; st['zlb_years']=int(len(z)); st['zlb_first']=int(z.index.min()) if len(z) else None
    st['neg_rate_years']=int((sr<0).sum())
    st['strate_peak']=(float(sr.max()),int(sr.idxmax())) if len(sr) else None
    lr=w.ltrate.dropna(); st['ltrate_start']=int(lr.index.min()) if len(lr) else None
    mg=w.real_money_growth.dropna(); st['rmoney_mean']=float(mg.mean()) if len(mg) else None
    st['rmoney_sd']=float(mg.std()) if len(mg) else None
    st['money_end']=int(mg.index.max()) if len(mg) else None
    src=w.money_src.dropna()
    sw=src[src!='M2']; st['money_note']=('M2' if not len(sw) else f"M2 to {int(sw.index.min())-1}, then {sw.iloc[0]}")
    if st['money_end'] is not None and st['money_end']<2022: st['money_note']+=f" (series ends {st['money_end']})"
    xm=w[['cycle','real_money_growth']].dropna(); st['money_cyc']=float(np.corrcoef(xm.cycle,xm.real_money_growth)[0,1]) if len(xm)>10 else None
    # external
    op=(w.exports_GDP+w.imports_GDP).dropna(); st['open_1970']=float(op.iloc[0]); st['open_2022']=float(op.loc[2022]); st['open_from']=int(op.index[0])
    ca=w.CA_GDP.dropna(); st['ca_mean']=float(ca.mean()); st['ca_min']=(float(ca.min()),int(ca.idxmin())); st['ca_max']=(float(ca.max()),int(ca.idxmax()))
    st['ca_start']=int(ca.index.min())
    re=w.REER.dropna(); st['reer_change']=float(100*(re.loc[2022]/re.iloc[0]-1)) if len(re) else None
    # labour
    u=w.unemp.dropna(); st['unemp_mean']=float(u.mean()) if len(u) else None; st['unemp_peak']=(float(u.max()),int(u.idxmax())) if len(u) else None
    st['unemp_start']=int(u.index.min()) if len(u) else None
    # crises
    st['crisis_covered']=bool(w.BankingCrisis.notna().any())
    st['cycle_from']=int(d.cycle.first_valid_index()); st['growth_from']=int(g.index.min())
    for k,c in [('bank','BankingCrisis'),('curr','CurrencyCrisis'),('sov','SovDebtCrisis')]:
        st['crisis_'+k]=[int(y) for y in w.index[w[c]==1]]
    # extra series stats for text
    inv=w.inv_GDP.dropna(); st['inv_peak']=(float(inv.max()),int(inv.idxmax())); st['inv_2022']=float(inv.loc[2022])
    st['fixes']=FIX[iso]
    S[iso]=st
json.dump(S,open('stats.json','w'),indent=1,default=float)
# quick view
for iso in ['USA','JPN','GRC','IND']:
    s=S[iso]; print(iso, f"g {s['growth_mean']:.2f}±{s['growth_sd']:.2f} worst {s['worst']} | anat", {k:round(v,2) for k,v in s['anat'].items()},
      f"| coup {s['coup_7089']:+.2f}->{s['coup_9022']:+.2f} | bal_cyc {s['bal_cyc']:+.2f} debt {s['debt_start']}->{s['debt_2022']} | zlb {s['zlb_years']} from {s['zlb_first']} | money {s['money_note']} | crises {s['crisis_bank']}")
