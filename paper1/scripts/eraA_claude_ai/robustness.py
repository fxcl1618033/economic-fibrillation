"""
ROBUSTNESS SUITE for the fibrillation arc (Kose-Terrones global recessions).
Checks: (1) band choice  (2) detrending method (HP filter, growth rates)
        (3) drop the US  (4) split-sample  (5) leave-one-crisis-out
Statistic: corr(r(t-k), G(t)); exact circular-shift permutation, one-sided in predicted direction.
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr
GLOBAL_REC=[1975,1982,1991,2009,2020]
CODES=['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
       'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']
md=pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']; md['year']=md['year'].astype(int)
Y0,Y1=1970,2022
LOG={}
for c in CODES:
    d=md[(md.ISO==c)&(md.gdppc.notna())&(md.year>=1950)].sort_values('year')
    LOG[c]=(d.year.values, np.log(d.gdppc.values.astype(float)))

def hp_cycle(y,lamb=100.0):
    n=len(y); I=np.eye(n)
    K=np.zeros((n-2,n))
    for i in range(n-2): K[i,i],K[i,i+1],K[i,i+2]=1.0,-2.0,1.0
    trend=np.linalg.solve(I+lamb*K.T@K, y)
    return y-trend

def phases(codes, method="bp", lo=1/9., hi=0.49):
    ph={}
    for c in codes:
        yrs,lg=LOG[c]
        if method=="bp":
            b,a=butter(2,[lo/0.5,hi/0.5],btype='band'); cyc=filtfilt(b,a,lg-lg.mean())
        elif method=="hp":
            cyc=hp_cycle(lg)
        elif method=="growth":
            cyc=np.diff(lg,prepend=lg[0]); cyc=cyc-cyc.mean()
        ph[c]=dict(zip(yrs,np.angle(hilbert(cyc))))
    return ph

def arc(ph, codes, y0=Y0, y1=Y1, crises=GLOBAL_REC):
    YEARS=np.arange(y0,y1+1)
    r=np.array([np.abs(np.mean([np.exp(1j*ph[c][y]) for c in codes if y in ph[c]])) for y in YEARS])
    G=np.isin(YEARS,crises).astype(float)
    if G.sum()<2: return None
    T=len(YEARS); out={}
    def lc(lag):
        if lag>0: u,v=r[:-lag],G[lag:]
        elif lag<0: u,v=r[-lag:],G[:lag]
        else: u,v=r,G
        return pearsonr(u,v)[0]
    for lab,lag,dirn in [("lead2",2,'pos'),("lead1",1,'pos'),("crisis",0,'pos'),("after2",-2,'neg')]:
        obs=lc(lag)
        null=np.array([pearsonr(*( (r[:-lag],np.roll(G,k)[lag:]) if lag>0 else
                                   ((r[-lag:],np.roll(G,k)[:lag]) if lag<0 else (r,np.roll(G,k)))))[0]
                       for k in range(1,T)])
        p=(1+np.sum(null>=obs))/(1+len(null)) if dirn=='pos' else (1+np.sum(null<=obs))/(1+len(null))
        out[lab]=(float(obs),float(p))
    return out

def show(tag,res):
    if res is None: print(f"  {tag:32s}  (too few crises)"); return
    s=lambda k: f"{res[k][0]:+.2f}(p={res[k][1]:.3f}){'*' if res[k][1]<0.05 else ' '}"
    print(f"  {tag:32s} lead2 {s('lead2')}  lead1 {s('lead1')}  crisis {s('crisis')}  after2 {s('after2')}")

BASE=phases(CODES); base=arc(BASE,CODES)
print("=== BASELINE (band-pass 2-9yr, 26 economies, 1970-2022) ===")
show("baseline",base)

print("\n=== 1. BAND CHOICE ===")
for lab,lo,hi in [("band 2-8 yr",1/8.,0.49),("band 3-10 yr",1/10.,1/3.),("band 2-9 (base)",1/9.,0.49)]:
    show(lab, arc(phases(CODES,"bp",lo,hi),CODES))

print("\n=== 2. DETRENDING METHOD ===")
for lab,m in [("HP filter (lambda=100)","hp"),("growth rates","growth")]:
    show(lab, arc(phases(CODES,m),CODES))

print("\n=== 3. DROP AN ECONOMY ===")
for drop in ["USA","DEU","JPN"]:
    sub=[c for c in CODES if c!=drop]
    show(f"without {drop}", arc(BASE,sub))

print("\n=== 4. SPLIT SAMPLE ===")
show("1970-1995 (1975,82,91)", arc(BASE,CODES,1970,1995,[1975,1982,1991]))
show("1996-2022 (2009,2020)",  arc(BASE,CODES,1996,2022,[2009,2020]))

print("\n=== 5. LEAVE-ONE-CRISIS-OUT  <-- the risky test ===")
for drop in GLOBAL_REC:
    sub=[y for y in GLOBAL_REC if y!=drop]
    show(f"without {drop}", arc(BASE,CODES,Y0,Y1,sub))
print("  --- harshest: drop BOTH recent crises ---")
show("without 2009 AND 2020", arc(BASE,CODES,Y0,Y1,[1975,1982,1991]))

json.dump({"baseline":base},open("robustness_results.json","w"),indent=2)
print("\nsaved robustness_results.json")
