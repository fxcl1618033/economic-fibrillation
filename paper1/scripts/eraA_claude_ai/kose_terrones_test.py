import numpy as np, pyreadr, json
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

RNG = np.random.default_rng(11)
GLOBAL_REC = [1975, 1982, 1991, 2009, 2020]
DOWNTURN   = [1998, 2001, 2012]
Y0, Y1 = 1970, 2022
CODES = ['USA','GBR','DEU','FRA','ITA','JPN','CAN','ESP','AUS','KOR','IND','MEX','NLD','SWE',
         'CHE','BEL','ZAF','TUR','NOR','AUT','DNK','FIN','GRC','PRT','IDN','THA']

md = pyreadr.read_r('MaddisonData-main/data/MaddisonData.rda')['MaddisonData']
md['year'] = md['year'].astype(int)
b, a = butter(2, [(1/9)/0.5, 0.49/0.5], btype='band')
phase = {}
for c in CODES:
    d = md[(md.ISO==c) & (md.gdppc.notna()) & (md.year>=1950)].sort_values('year')
    g = d.gdppc.values.astype(float)
    cyc = filtfilt(b, a, np.log(g) - np.log(g).mean())
    phase[c] = dict(zip(d.year.values, np.angle(hilbert(cyc))))

YEARS = np.arange(Y0, Y1+1)
r = np.array([np.abs(np.mean([np.exp(1j*phase[c][y]) for c in CODES])) for y in YEARS])
rby = {int(y): float(r[i]) for i, y in enumerate(YEARS)}
G = np.isin(YEARS, GLOBAL_REC).astype(float)
D = np.isin(YEARS, DOWNTURN).astype(float)
normal = (G==0) & (D==0)

def boot_ci(v, nb=10000):
    v=np.asarray(v); bs=[RNG.choice(v,len(v),replace=True).mean() for _ in range(nb)]
    return float(np.mean(v)), float(np.percentile(bs,2.5)), float(np.percentile(bs,97.5))
m_g, m_d, m_n = boot_ci(r[G==1]), boot_ci(r[D==1]), boot_ci(r[normal])

def lagcorr(r, g, lag):
    if lag>0:   x,y=r[:-lag],g[lag:]
    elif lag<0: x,y=r[-lag:],g[:lag]
    else:       x,y=r,g
    return pearsonr(x,y)[0]
def perm(lag, direction):
    obs=lagcorr(r,G,lag); T=len(G)
    null=np.array([lagcorr(r,np.roll(G,k),lag) for k in range(1,T)])
    p=(1+np.sum(null>=obs))/(1+len(null)) if direction=='pos' else (1+np.sum(null<=obs))/(1+len(null))
    p2=(1+np.sum(np.abs(null)>=abs(obs)))/(1+len(null))
    return obs, p, p2

ARC = [("2 yr before",2,'pos'),("1 yr before",1,'pos'),("crisis year",0,'pos'),
       ("1 yr after",-1,'neg'),("2 yr after",-2,'neg')]
arc={}
for lab,lag,d_ in ARC:
    o,p1,p2=perm(lag,d_); arc[lab]={"lag":lag,"corr":o,"p_dir":p1,"p_two":p2,"dir":d_}

Lax=np.arange(-4,5)
comp=np.array([[rby.get(o+k,np.nan) for k in Lax] for o in GLOBAL_REC])
comp_m,comp_s=np.nanmean(comp,axis=0),np.nanstd(comp,axis=0)
peak_val=comp_m[3]; after2_val=comp_m[6]; shatter=peak_val-after2_val

print("FIBRILLATION ARC")
for l in arc:
    A=arc[l]; star=" *" if A["p_dir"]<0.05 else ""
    print(f"  {l:12s} lag{A['lag']:+d}: corr={A['corr']:+.3f} p={A['p_dir']:.3f}({A['dir']}){star} [2s {A['p_two']:.3f}]")
print(f"epoch: peak {peak_val:.2f}(t-1) -> {after2_val:.2f}(t+2), shatter {shatter:.2f}")

plt.rcParams.update({"figure.dpi":140,"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.alpha":0.25})
GC,DC="#e63946","#f4a261"

fig,ax=plt.subplots(figsize=(11,4.3))
for y in GLOBAL_REC: ax.axvspan(y-0.5,y+0.5,color=GC,alpha=0.25)
for y in DOWNTURN:   ax.axvspan(y-0.5,y+0.5,color=DC,alpha=0.30)
ax.plot(YEARS,r,color="#1d3557",lw=2.3); ax.axhline(m_n[0],color="grey",ls=":",lw=1)
ax.text(YEARS[1],m_n[0]+0.01,"normal-year average",fontsize=8,color="grey")
ax.set_ylim(0,1); ax.set_xlim(YEARS[0],YEARS[-1]); ax.set_xlabel("year"); ax.set_ylabel("r (synchronization)")
ax.set_title("Synchronization r(t) vs Kose-Terrones global recessions (red) and downturns (orange)",loc="left")
fig.savefig("kfig1_overview.png",bbox_inches="tight"); fig.savefig("kfig1_overview.pdf",bbox_inches="tight"); plt.close(fig)

fig,ax=plt.subplots(figsize=(6.5,4))
groups=["Global\nrecessions","Global\ndownturns","Normal\nyears"]; means=[m_g[0],m_d[0],m_n[0]]
err=[[means[0]-m_g[1],means[1]-m_d[1],means[2]-m_n[1]],[m_g[2]-means[0],m_d[2]-means[1],m_n[2]-means[2]]]
ax.bar(groups,means,color=[GC,DC,"#adb5bd"],yerr=err,capsize=6,edgecolor="white")
for i,m in enumerate(means): ax.text(i,m+0.02,f"{m:.2f}",ha="center")
ax.set_ylim(0,1); ax.set_ylabel("mean r"); ax.set_title("Synchronization by period type (95% bootstrap CI)",loc="left",fontsize=10.5)
fig.savefig("kfig2_groups.png",bbox_inches="tight"); fig.savefig("kfig2_groups.pdf",bbox_inches="tight"); plt.close(fig)

fig,ax=plt.subplots(figsize=(8,4.5))
for o,row in zip(GLOBAL_REC,comp): ax.plot(Lax,row,marker="o",lw=1.2,alpha=0.45,label=str(o))
ax.fill_between(Lax,comp_m-comp_s,comp_m+comp_s,color=GC,alpha=0.13)
ax.plot(Lax,comp_m,color="#1d3557",lw=2.8,marker="o",label="mean")
ax.axvline(0,color=GC,ls="--",lw=1.2); ax.axhline(m_n[0],color="grey",ls=":",lw=1)
ax.annotate(f"peak {peak_val:.2f}\n(1 yr before)",(-1,peak_val),xytext=(-3.4,0.86),fontsize=8.5,color="#1d3557",arrowprops=dict(arrowstyle="->",color="#1d3557"))
ax.annotate(f"shatter {after2_val:.2f}\n(2 yr after)",(2,after2_val),xytext=(2.3,0.20),fontsize=8.5,color=GC,arrowprops=dict(arrowstyle="->",color=GC))
ax.set_ylim(0,1); ax.set_xlabel("years relative to global-recession onset"); ax.set_ylabel("r(t)")
ax.set_title("Fibrillation signature: rise, peak, then shatter (superposed epoch, n=5)",loc="left",fontsize=10.5)
ax.legend(fontsize=7,ncol=2,loc="lower left")
fig.savefig("kfig4_epoch.png",bbox_inches="tight"); fig.savefig("kfig4_epoch.pdf",bbox_inches="tight"); plt.close(fig)

fig,ax=plt.subplots(figsize=(9,4.6))
labels=[a[0] for a in ARC]; xs=np.arange(len(labels))
colors=["#2a9d8f" if arc[l]["corr"]>=0 else GC for l in labels]
ax.bar(xs,[arc[l]["corr"] for l in labels],color=colors,edgecolor="white",width=0.6)
for i,l in enumerate(labels):
    A=arc[l]; star="*" if A["p_dir"]<0.05 else ""
    yoff=0.012 if A["corr"]>=0 else -0.03
    ax.text(xs[i],A["corr"]+yoff,f"{A['corr']:+.2f}\np={A['p_dir']:.3f}{star}",ha="center",
            va="bottom" if A["corr"]>=0 else "top",fontsize=8.5,fontweight="bold" if A["p_dir"]<0.05 else "normal")
ax.axhline(0,color="k",lw=0.7); ax.axvline(2.5,color="#ccc",ls=":",lw=1)
ax.set_xticks(xs); ax.set_xticklabels(labels)
ax.text(0.5,-0.36,"BEFORE  (rise)",ha="center",fontsize=9,color="#2a9d8f",fontweight="bold")
ax.text(3.5,-0.36,"AFTER  (collapse)",ha="center",fontsize=9,color=GC,fontweight="bold")
ax.set_ylim(-0.42,0.32); ax.set_ylabel("correlation of synchronization with crisis")
ax.set_title("The full fibrillation arc: rise before the crisis, significant collapse after",loc="left",fontsize=10.5)
ax.text(4.0,0.26,"* p<0.05 (one-sided,\n predicted direction)",fontsize=7.5,color="#555",ha="center")
fig.savefig("kfig5_arc.png",bbox_inches="tight"); fig.savefig("kfig5_arc.pdf",bbox_inches="tight"); plt.close(fig)

json.dump({"definition":"Kose-Terrones global recessions","global_recessions":GLOBAL_REC,"downturns":DOWNTURN,
 "window":[Y0,Y1],"n_economies":26,"mean_recession":m_g,"mean_downturn":m_d,"mean_normal":m_n,
 "arc":arc,"epoch_peak":float(peak_val),"epoch_after2":float(after2_val),"shatter_drop":float(shatter),
 "epoch_mean":comp_m.tolist(),"epoch_lags":Lax.tolist(),"r_by_year":rby},
 open("kose_terrones_results.json","w"),indent=2)
print("saved kfig1,2,4,5 and updated json")
