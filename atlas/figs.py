"""Country dashboards (9 panels), global-factor figures, overview heatmaps."""
import numpy as np, pandas as pd, json, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
P=pd.read_csv('panel.csv'); GB=pd.read_csv('global.csv').set_index('year'); S=json.load(open('stats.json'))
_M=json.load(open('meta.json')); ORDER=_M['order']; EXTRA=_M.get('extra',[]); XISOS=[o[0] for o in EXTRA]; GL=[1975,1982,1991,2009,2020]
BLUE,ORANGE,AQUA,YELLOW,VIOLET,RED='#2a78d6','#eb6834','#1baf7a','#eda100','#4a3aa7','#e34948'
INK,INK2,MUTED,GRID,BASE,BAND='#0b0b0b','#52514e','#898781','#e1e0d9','#c3c2b7','#efeee9'
plt.rcParams.update({'font.family':'Inter','font.size':6.6,'axes.titlesize':7,'axes.titleweight':'bold',
 'axes.titlecolor':INK,'axes.titlelocation':'left','axes.edgecolor':BASE,'axes.linewidth':0.6,'axes.labelcolor':INK2,
 'axes.spines.top':False,'axes.spines.right':False,'xtick.color':MUTED,'ytick.color':MUTED,'xtick.labelcolor':INK2,
 'ytick.labelcolor':INK2,'xtick.major.size':2,'ytick.major.size':2,'axes.grid':True,'axes.grid.axis':'y',
 'grid.color':GRID,'grid.linewidth':0.5,'legend.fontsize':5.9,'legend.frameon':False,'legend.handlelength':1.4,
 'figure.dpi':220,'savefig.dpi':220,'axes.axisbelow':True})
def frame(ax,lo=1970,hi=2022,bands=True):
    if bands:
        for g in GL: ax.axvspan(g-0.5,g+0.5,color=BAND,zorder=0,lw=0)
    ax.set_xlim(lo-0.8,hi+0.8); ax.set_xticks([1970,1980,1990,2000,2010,2020]); ax.set_xticklabels(["'70","'80","'90","'00","'10","'20"])
def zero(ax): ax.axhline(0,color=BASE,lw=0.7,zorder=1)
def note(ax,txt): pass
def T(ax,title,sub=None):
    ax.set_title(title,pad=(9 if sub else 4))
    if sub: ax.text(0,1.012,sub,transform=ax.transAxes,ha='left',va='bottom',fontsize=5.7,color=INK2)
def leg(ax,ncol): ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=ncol,columnspacing=0.9)

def country(iso):
    d=P[P.iso==iso].set_index('year').loc[1970:2022]; st=S[iso]
    fig,axs=plt.subplots(3,3,figsize=(7.25,6.15),constrained_layout=True)
    # 1 growth
    ax=axs[0,0]; g=d.growth
    ax.bar(g.index,g.where(g>=0),color=BLUE,width=0.78,label='growth'); ax.bar(g.index,g.where(g<0),color=RED,width=0.78,label='contraction')
    zero(ax); frame(ax); T(ax,'Real GDP growth, %',f"mean {st['growth_mean']:.1f}% · s.d. {st['growth_sd']:.1f} · worst {st['worst'][0]:.1f}% ({st['worst'][1]})"); leg(ax,2)
    # 2 contributions
    ax=axs[0,1]; c=d[['c_C','c_I','c_NX']].loc[1971:]
    pos=np.zeros(len(c)); neg=np.zeros(len(c))
    for k,col,lab in [('c_C',BLUE,'consumption'),('c_I',ORANGE,'investment'),('c_NX',AQUA,'net exports')]:
        v=c[k].fillna(0).values; up=np.where(v>0,v,0); dn=np.where(v<0,v,0)
        ax.bar(c.index,up,bottom=pos,color=col,width=0.82,edgecolor='white',linewidth=0.25,label=lab); pos+=up
        ax.bar(c.index,dn,bottom=neg,color=col,width=0.82,edgecolor='white',linewidth=0.25); neg+=dn
    ax.plot(d.loc[1971:].index,d.growth.loc[1971:],color=INK,lw=0.8,label='GDP growth')
    bl=st['fixes'].get('contrib_blank',[])
    if bl: ax.plot(bl,[0]*len(bl),ls='none',marker='x',ms=3.2,mew=0.8,color=MUTED,zorder=5)
    zero(ax); frame(ax); A=st['anat']; T(ax,'Where the swing lives: contributions, pp',f"share of growth variance: C {A['C']:.0%} · I {A['I']:.0%} · net exports {A['NX']:+.0%}"); leg(ax,2)
    # 3 cycle vs world
    ax=axs[0,2]; ax.plot(d.index,d.cycle_z,color=BLUE,lw=1.1,label=st['name'])
    ax.plot(d.index,d.row_cycle/np.nanstd(d.row_cycle),color=MUTED,lw=1.0,ls=(0,(3,1.5)),label=('the 26 economies' if iso in XISOS else 'other 25 economies'))
    zero(ax); frame(ax); T(ax,'In step with the world?',f"correlation '70–89 {st['coup_7089']:+.2f} · '90–22 {st['coup_9022']:+.2f}"); leg(ax,2)
    # 4 budget
    ax=axs[1,0]; r=d.govrev_GDP; s=d.govexp_GDP; hist=d.fiscal_hist.astype(bool); fx=st['fixes']['fiscal']
    cuts=[1970]+fx.get('breaks',[])+[2023]
    for k,(lo,hi) in enumerate(zip(cuts[:-1],cuts[1:])):
        idx=(d.index>=lo)&(d.index<hi); rr=r.where(idx); ss=s.where(idx)
        ax.fill_between(d.index,rr,ss,where=(ss>=rr),color=RED,alpha=0.16,lw=0,interpolate=True,label='deficit' if k==0 else None)
        ax.fill_between(d.index,rr,ss,where=(rr>ss),color=BLUE,alpha=0.16,lw=0,interpolate=True,label='surplus' if k==0 else None)
        jn=fx['weo_from']
        for ser,col,lab in [(rr,BLUE,'revenue'),(ss,ORANGE,'spending')]:
            ax.plot(d.index,ser.where(~hist),color=col,lw=1.1,label=lab if k==0 else None)
            if hist.any(): ax.plot(d.index,ser.where(hist|(d.index==jn)),color=col,lw=1.0,ls=(0,(1,1.2)))
    if hist.any(): ax.axvline(fx['weo_from']-0.5,color=MUTED,lw=0.6,ls=(0,(1,1.5)),zorder=1)
    for bk in fx.get('breaks',[]): ax.axvline(bk-0.5,color=MUTED,lw=0.6,ls=(0,(1,1.5)),zorder=1)
    sub=f"mean balance {st['bal_mean']:+.1f} · corr with cycle {st['bal_cyc']:+.2f}"+(f" · from {st['fiscal_from']}" if st['fiscal_from']>1970 else '')
    frame(ax); T(ax,'Government budget, % of GDP',sub); leg(ax,2)
    # 5 debt
    ax=axs[1,1]; db=d.govdebt_GDP; dh=d.debt_hist.astype(bool); ax.fill_between(db.index,0,db,color=BLUE,alpha=0.12,lw=0)
    ax.plot(db.index,db.where(~dh),color=BLUE,lw=1.2)
    if dh.any():
        jn=st['fixes']['debt']['weo_from']; ax.plot(db.index,db.where(dh|(db.index==jn)),color=BLUE,lw=1.1,ls=(0,(1,1.2)))
        ax.axvline(jn-0.5,color=MUTED,lw=0.6,ls=(0,(1,1.5)),zorder=1)
    frame(ax); ax.set_ylim(bottom=0); T(ax,'Government debt, % of GDP',f"{st['debt_start'][0]:.0f}% ({st['debt_start'][1]}) → {st['debt_2022']:.0f}% (2022) · peak {st['debt_peak'][0]:.0f}% ({st['debt_peak'][1]})")
    # 6 rates & inflation
    ax=axs[1,2]; fx=st['fixes']; has_r=d.strate.notna().any()
    if has_r: ax.plot(d.index,d.strate,color=BLUE,lw=1.1,label='policy rate' if fx.get('strate_is_policy_rate') else 'short-term rate')
    if d.ltrate.notna().any(): ax.plot(d.index,d.ltrate,color=ORANGE,lw=1.0,label='long-term rate')
    ax.plot(d.index,d.infl,color=AQUA,lw=1.0,label='CPI inflation')
    logy=(iso=='BRA')
    if logy:
        ax.set_yscale('log'); ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v,_: f"{v:g}")); ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    else: zero(ax)
    sub=f"inflation peak {st['infl_peak'][0]:,.0f}% ('{str(st['infl_peak'][1])[2:]})"+(' · log scale' if logy else (f" · zero-rate years {st['zlb_years']}" if has_r else ' · no interest-rate series'))
    frame(ax); T(ax,'Interest rates and inflation, %',sub); leg(ax,2)
    # 7 real money
    ax=axs[2,0]; m=d.real_money_growth
    ax.bar(m.index,m.where(m>=0),color=BLUE,width=0.78,label='expansion'); ax.bar(m.index,m.where(m<0),color=RED,width=0.78,label='contraction')
    src=d.money_src.dropna(); alts=[v for v in pd.unique(src.values) if v!='M2']
    parts=['M2' if not alts else f"M2, then {alts[0]} from {int(src[src==alts[0]].index.min())}"]
    if st['money_end'] and st['money_end']<2022: parts.append(f"ends {st['money_end']}")
    dr=st['fixes'].get('money_dropped',[])
    if dr: parts.append('breaks dropped: '+', '.join(str(y) for y in dr))
    zero(ax); frame(ax); T(ax,'Real broad-money growth, %',' · '.join(parts)); leg(ax,2)
    # 8 trade
    ax=axs[2,1]; ax.plot(d.index,d.exports_GDP,color=AQUA,lw=1.2,label='exports'); ax.plot(d.index,d.imports_GDP,color=YELLOW,lw=1.2,label='imports')
    frame(ax); ax.set_ylim(bottom=0); T(ax,'Trade, % of GDP',f"exports + imports: {st['open_1970']:.0f}% ({st.get('open_from',1970)}) → {st['open_2022']:.0f}% (2022)"); leg(ax,2)
    # 9 current account
    ax=axs[2,2]; ca=d.CA_GDP
    ax.bar(ca.index,ca.where(ca>=0),color=BLUE,width=0.78,label='surplus'); ax.bar(ca.index,ca.where(ca<0),color=RED,width=0.78,label='deficit')
    zero(ax); frame(ax); T(ax,'Current account, % of GDP',f"mean {st['ca_mean']:+.1f} · low {st['ca_min'][0]:+.1f} ('{str(st['ca_min'][1])[2:]}) · high {st['ca_max'][0]:+.1f} ('{str(st['ca_max'][1])[2:]})"); leg(ax,2)
    fig.savefig(f'fig/{iso}.png'); plt.close(fig)

def global_figs():
    y=GB.loc[1970:2022]
    fig,axs=plt.subplots(3,2,figsize=(7.25,6.6),constrained_layout=True)
    ax=axs[0,0]; g=y.world_growth; ax.bar(g.index,g.where(g>=0),color=BLUE,width=0.78,label='growth'); ax.bar(g.index,g.where(g<0),color=RED,width=0.78,label='contraction')
    zero(ax); frame(ax); ax.set_title('World growth: the 26 economies, GDP-weighted, %'); ax.legend(loc='lower left',ncol=2)
    ax=axs[0,1]; n=y.n_contracting; ax.bar(n.index,n,color=ORANGE,width=0.78); frame(ax); ax.set_title('How many of the 26 economies shrank that year')
    ax.set_ylim(0,27); ax.set_yticks([0,5,10,15,20,25])
    for yr in [1975,1982,1991,2009,2020]: ax.text(yr,n.loc[yr]+0.6,f"{int(n.loc[yr])}",ha='center',fontsize=5.8,color=INK)
    ax=axs[1,0]; o=y.oil_real_2015usd; ax.plot(o.index,o,color=INK,lw=1.2); ax.fill_between(o.index,0,o,color=BLUE,alpha=0.1,lw=0)
    frame(ax); ax.set_title('Real oil price, 2015 US$ per barrel'); ax.set_ylim(bottom=0)
    ax=axs[1,1]; t=y.world_imports_GDP; ax.plot(t.index,t,color=AQUA,lw=1.3); ax.fill_between(t.index,0,t,color=AQUA,alpha=0.12,lw=0)
    frame(ax); ax.set_ylim(bottom=0); ax.set_title('Imports of the 26, % of GDP (GDP-weighted)')
    ax=axs[2,0]; ax.fill_between(y.index,y.infl_q25,y.infl_q75,color=BLUE,alpha=0.16,lw=0,label='middle half of economies'); ax.plot(y.index,y.infl_med,color=BLUE,lw=1.2,label='median')
    zero(ax); frame(ax); ax.set_title('Inflation across the 26 economies, %'); ax.legend(loc='upper right',ncol=1)
    ax=axs[2,1]
    SY=json.load(open('sync.json'))
    for col,c,lab in [('GDP',BLUE,'real GDP'),('inv',ORANGE,'investment'),('strate',AQUA,'short-term rates')]:
        ax.plot(SY['years'],SY['r_t'][col],color=c,lw=1.0,label=lab+(f" (n={SY['n'][col]})" if SY['n'][col]<26 else ''))
    frame(ax); ax.set_ylim(0,1.02); T(ax,'Synchronization r(t) across the 26, by channel','1 = all economies at the same point of their cycle · last 2–3 years less reliable (filter edge)'); leg(ax,3)
    fig.savefig('fig/global_real.png'); plt.close(fig)
    fig,axs=plt.subplots(2,2,figsize=(7.25,4.6),constrained_layout=True)
    ax=axs[0,0]; ax.plot(y.index,y.us_strate,color=BLUE,lw=1.2,label='United States'); ax.plot(y.index,y.strate_med_ex_us,color=ORANGE,lw=1.2,label='median of the other economies')
    zero(ax); frame(ax); ax.set_title('Short-term interest rates, %'); ax.legend(loc='upper right')
    ax=axs[0,1]; s=100*y.share_raising; ax.bar(s.index,s,color=ORANGE,width=0.78); ax.axhline(50,color=BASE,lw=0.7)
    frame(ax); ax.set_ylim(0,100); ax.set_title('Share of economies raising short-term rates, %')
    ax=axs[1,0]; ax.plot(y.index,y.us_reer,color=INK,lw=1.2); frame(ax); ax.set_title('US dollar, real effective exchange rate (index)')
    ax=axs[1,1]; b=y.banking_onsets.fillna(0); cu=y.currency_onsets.fillna(0)
    ax.bar(b.index,b,color=BLUE,width=0.78,edgecolor='white',linewidth=0.25,label='banking-crisis onsets')
    ax.bar(cu.index,cu,bottom=b,color=ORANGE,width=0.78,edgecolor='white',linewidth=0.25,label='currency-crisis onsets')
    frame(ax); ax.set_title('Crisis onsets among the 26 economies (count)'); ax.legend(loc='upper left')
    fig.savefig('fig/global_money.png'); plt.close(fig)

def overview():
    isos=[o[0] for o in ORDER]; names=[o[1] for o in ORDER]
    decs=['1970s','1980s','1990s','2000s','2010-22']
    M=np.array([[S[i]['coup_dec'][k] for k in decs] for i in isos])
    R=np.array([[S[i]['gr_global'][str(y)] if S[i]['gr_global'][str(y)] is not None else np.nan for y in GL] for i in isos])
    cm=LinearSegmentedColormap.from_list('div',['#256abf','#9ec5f4','#f0efec','#f2a3a2','#c22f2f'])
    fig,axs=plt.subplots(1,2,figsize=(7.25,6.3),constrained_layout=True,gridspec_kw={'width_ratios':[1,1]})
    for ax,data,cols,title,norm,fmt,cmap in [
        (axs[0],M,['1970s','1980s','1990s','2000s','2010–22'],'Coupling to the other 25 economies\n(correlation of business cycles, by decade)',TwoSlopeNorm(0,-0.6,1.0),'{:+.2f}',cm),
        (axs[1],R,[str(y) for y in GL],'Real GDP growth in each global recession, %',TwoSlopeNorm(0,-10,8),'{:+.1f}',cm.reversed())]:
        ax.imshow(data,cmap=cmap,norm=norm,aspect='auto')
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if not np.isnan(data[i,j]):
                    lab=fmt.format(data[i,j]); lab=('0.00' if lab in ('+0.00','-0.00') else '0.0' if lab in ('+0.0','-0.0') else lab)
                    ax.text(j,i,lab,ha='center',va='center',fontsize=5.8,color=INK)
        ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols); ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
        ax.tick_params(axis='both',length=0); ax.grid(False); ax.set_title(title)
        for sp in ax.spines.values(): sp.set_visible(False)
        prev=None
        for i,o in enumerate(ORDER):
            if prev and o[2]!=prev: ax.axhline(i-0.5,color='white',lw=2)
            prev=o[2]
        ax.xaxis.tick_top(); ax.xaxis.set_label_position('top')
    fig.savefig('fig/overview_heat.png'); plt.close(fig)

def overview_extra():
    isos=[o[0] for o in EXTRA]; names=[o[1] for o in EXTRA]
    decs=['1970s','1980s','1990s','2000s','2010-22']
    nz=lambda v: np.nan if v is None else v
    M=np.array([[nz(S[i]['coup_dec'][k]) for k in decs] for i in isos])
    R=np.array([[nz(S[i]['gr_global'][str(y)]) for y in GL] for i in isos])
    cm=LinearSegmentedColormap.from_list('div',['#256abf','#9ec5f4','#f0efec','#f2a3a2','#c22f2f'])
    fig,axs=plt.subplots(1,2,figsize=(7.25,1.75),constrained_layout=True)
    for ax,data,cols,title,norm,fmt,cmap in [
        (axs[0],M,['1970s','1980s','1990s','2000s','2010–22'],'Coupling to the 26 economies (correlation of cycles)',TwoSlopeNorm(0,-0.6,1.0),'{:+.2f}',cm),
        (axs[1],R,[str(y) for y in GL],'Real GDP growth in each global recession, %',TwoSlopeNorm(0,-10,8),'{:+.1f}',cm.reversed())]:
        ax.imshow(np.ma.masked_invalid(data),cmap=cmap,norm=norm,aspect='auto')
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if np.isnan(data[i,j]): ax.text(j,i,'n/a',ha='center',va='center',fontsize=5.6,color=MUTED)
                else:
                    lab=fmt.format(data[i,j]); lab=('0.00' if lab in ('+0.00','-0.00') else '0.0' if lab in ('+0.0','-0.0') else lab)
                    ax.text(j,i,lab,ha='center',va='center',fontsize=5.8,color=INK)
        ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols); ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
        ax.tick_params(axis='both',length=0); ax.grid(False); ax.set_title(title)
        for sp in ax.spines.values(): sp.set_visible(False)
        ax.xaxis.tick_top(); ax.xaxis.set_label_position('top')
    fig.savefig('fig/overview_extra.png'); plt.close(fig)

if __name__=='__main__':
    which=sys.argv[1] if len(sys.argv)>1 else 'all'
    if which in ('all','global'): global_figs(); overview()
    if which in ('all','extra'):
        for o in EXTRA: country(o[0])
        overview_extra()
    if which=='all':
        for o in ORDER: country(o[0])
    elif which not in ('global','extra'): country(which)
    print('done',which)
