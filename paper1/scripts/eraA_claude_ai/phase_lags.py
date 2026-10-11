"""
PAIRWISE PHASE LAGS: who leads whom in the world business cycle?
lead_i = mean wrapped(theta_i - Psi), where Psi = global mean phase; converted to YEARS
via the mean instantaneous frequency. Positive = economy runs AHEAD of the world cycle.
Also computed in windows around 2009 and 2020 (epicenter hint for Paper 2).
NOTE: endogenous (derived from the same GDP cycles) -> DESCRIPTIVE, not causal.
Null = 5000 surrogate economy sets.
"""
import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
RNG=np.random.default_rng(505)
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

def phase(Xa): return np.angle(hilbert(Xa,axis=-1))
def wrap(x): return (x+np.pi)%(2*np.pi)-np.pi

TH=phase(X)                                     # (N,T)
PSI=np.angle(np.exp(1j*TH).mean(axis=0))        # global mean phase (T,)
# mean instantaneous frequency (rad/yr) -> convert phase lead to years
omega=np.mean([np.mean(wrap(np.diff(TH[i]))) for i in range(N)])
period=2*np.pi/omega
print(f"mean cycle period = {period:.1f} years  (omega={omega:.3f} rad/yr)")

def leadership(TH_, PSI_):
    d=wrap(TH_-PSI_[None,:] if TH_.ndim==2 else TH_-PSI_[...,None,:])
    return np.angle(np.exp(1j*d).mean(axis=-1))/omega     # in YEARS

lead=leadership(TH,PSI)
order=np.argsort(-lead)
print("\n=== who leads the world business cycle? (years ahead of global phase) ===")
print("  LEADERS:")
for i in order[:6]:  print(f"    {CODES[i]}: {lead[i]:+.2f} yr")
print("  LAGGARDS:")
for i in order[-6:]: print(f"    {CODES[i]}: {lead[i]:+.2f} yr")
print(f"\n  spread (max-min) = {lead.max()-lead.min():.2f} yr   sd = {lead.std():.3f} yr")

# --- surrogate null on the SPREAD (is the leadership structure real?) ---
Xf=np.fft.rfft(X,axis=-1); amp=np.abs(Xf); nf=Xf.shape[-1]
BATCH=250; nulls=[]
for s0 in range(0,NSUR,BATCH):
    nb=min(BATCH,NSUR-s0)
    rp=RNG.uniform(0,2*np.pi,size=(nb,N,nf)); rp[...,0]=0
    if T%2==0: rp[...,-1]=0
    Xs=np.fft.irfft(amp[None,...]*np.exp(1j*rp),n=T,axis=-1)
    ths=phase(Xs); psis=np.angle(np.exp(1j*ths).mean(axis=1))
    ls=leadership(ths,psis)
    nulls.append(ls.std(axis=-1))
nulls=np.concatenate(nulls)
p_spread=(1+np.sum(nulls>=lead.std()))/(1+len(nulls))
print(f"  vs {NSUR} surrogates: null sd mean {nulls.mean():.3f}, 95th {np.percentile(nulls,95):.3f} -> p = {p_spread:.4f}")

# --- leadership in windows around the two modern crises ---
print("\n=== who led INTO each modern crisis? (8-yr window before onset) ===")
per_crisis={}
for onset in [2009,2020]:
    idx=[YI[y] for y in range(onset-8,onset) if y in YI]
    d=wrap(TH[:,idx]-PSI[None,idx]); L=np.angle(np.exp(1j*d).mean(axis=1))/omega
    o=np.argsort(-L); per_crisis[onset]={CODES[i]:float(L[i]) for i in range(N)}
    print(f"  {onset}: leaders " + ", ".join(f"{CODES[i]}({L[i]:+.2f})" for i in o[:4]) +
          "  |  laggards " + ", ".join(f"{CODES[i]}({L[i]:+.2f})" for i in o[-3:]))

json.dump({"period_years":float(period),"lead_years":{CODES[i]:float(lead[i]) for i in range(N)},
 "spread":float(lead.max()-lead.min()),"sd":float(lead.std()),"p_spread":float(p_spread),
 "per_crisis":per_crisis},open("phase_lag_results.json","w"),indent=2)
np.save("null_spread.npy",nulls)
print("\nsaved phase_lag_results.json")
