"""Write atlas.tex from stats.json / meta.json / global.csv / sync.json and the figures in fig/."""
import json, numpy as np, pandas as pd
S=json.load(open('stats.json')); META=json.load(open('meta.json')); ORDER=META['order']; FIX=META['fixes']
EXTRA=META.get('extra',[]); XISOS=[o[0] for o in EXTRA]; I26=[o[0] for o in ORDER]
GB=pd.read_csv('global.csv').set_index('year').loc[1970:2022]; SY=json.load(open('sync.json'))
P=pd.read_csv('panel.csv')
GL=[1975,1982,1991,2009,2020]
M='\u2212'

def esc(s): return str(s).replace('&','\\&').replace('%','\\%').replace('#','\\#').replace('_','\\_')
def f(x,d=1):
    if x is None or (isinstance(x,float) and np.isnan(x)): return '–'
    t=f"{x:,.0f}" if abs(x)>=1000 else f"{x:.{d}f}"
    if float(t.replace(',',''))==0: t=t.lstrip('-')
    return t.replace('-',M)
def sg(x,d=1):
    if x is None or (isinstance(x,float) and np.isnan(x)): return '–'
    t=f"{x:+.{d}f}"
    if float(t)==0: t=t[1:]
    return t.replace('-',M)
def pc(x,d=0): return f(x,d)+'\\%'
def yy(y): return f"’{str(y)[2:]}"
def lst(v): return ', '.join(str(x) for x in v) if v else 'none'
def share(x): return f"{x*100:.0f}\\%".replace('-',M)

CONTEXT={
'USA':"The world's largest economy and issuer of the main reserve currency. Episodes: 1973–75 oil shock; the Volcker disinflation and the 1980–82 double-dip recession; the 2001 dot-com bust; the 2007–09 financial crisis; the 2020 pandemic shock.",
'CAN':"Commodity-rich and closely tied to the US, its main export market. Episodes: recessions in 1982 and 1990–92; fiscal consolidation from the mid-1990s that turned large deficits into surpluses; the 2009 recession; 2020.",
'MEX':"Oil exporter turned manufacturing hub integrated with the US (NAFTA from 1994). Episodes: the 1982 debt crisis; very high inflation in the 1980s; the 1994–95 Tequila crisis; the US-led 2009 recession; 2020.",
'DEU':"Export-oriented industrial core of Europe (West Germany before 1991). Episodes: the 1970s oil shocks; reunification in 1990 and a slow 1990s; early-2000s stagnation and labour-market reforms; the 2009 export collapse; 2020.",
'FRA':"Large, diversified economy with a big public sector. Episodes: the 1981 expansion and the 1983 austerity turn; the franc fort years; the euro from 1999; the 2009 recession; 2020.",
'GBR':"Services- and finance-heavy economy with a floating pound. Episodes: the 1976 IMF loan; the 1980–81 recession; the 1990–91 recession and 1992 exit from the ERM; the 2008–09 banking crisis; the 2016 Brexit vote; 2020.",
'ITA':"Industrial north, high public debt since the 1980s. Episodes: 1970s inflation; the 1992 lira crisis and ERM exit; the euro from 1999; the 2008–09 recession; the 2011–12 euro-area debt crisis; 2020.",
'NLD':"Very open trading economy and natural-gas producer. Episodes: the 1970s gas boom (the original 'Dutch disease'); the 1982 Wassenaar wage-moderation agreement; 2008 bank rescues; 2020.",
'BEL':"Very open small economy at the centre of the EU, with high public debt in the 1980s–90s. Episodes: the early-1980s fiscal crisis; the euro from 1999; 2008 bank rescues; 2020.",
'AUT':"Small open economy tied to Germany (schilling pegged to the D-mark, euro from 1999). Episodes: the 'Austro-Keynesian' policy mix of the 1970s–80s; EU entry in 1995; the 2009 recession; 2020.",
'CHE':"Small open economy and financial centre with a safe-haven franc. Episodes: franc appreciation and the 1975 recession; stagnation in the 1990s; the 2011–15 floor against the euro; negative policy rates 2015–22; 2020.",
'SWE':"Open industrial economy with a large welfare state. Episodes: devaluations in 1981–82; the 1990–93 banking crisis and the 1992 float of the krona; inflation targeting from 1993; the 2009 recession; 2020.",
'NOR':"Oil and gas exporter that saves its petroleum revenue in a sovereign fund (set up in 1990). Episodes: the 1970s oil boom; the 1986 oil-price collapse; the 1988–92 banking crisis; the 2014 oil-price fall; the 2022 gas windfall.",
'DNK':"Small open economy with a fixed exchange rate (to the D-mark, then the euro). Episodes: fiscal crises in the 1970s–early 1980s; the fixed-rate policy from 1982; the 2008–09 banking and housing bust; 2020.",
'FIN':"Forest and engineering exporter, once tied to Soviet trade. Episodes: the 1990–93 depression (collapse of Soviet trade plus a banking crisis); the late-1990s Nokia-led boom; the euro from 1999; the 2009 export collapse; 2020.",
'ESP':"Late industrializer; democracy from 1977, EU member from 1986. Episodes: the 1977–85 banking crisis; the 1992–93 recession; the euro from 1999; the 2000s housing boom and 2008–13 bust, with the 2012 bank rescue; 2020.",
'PRT':"Small catching-up economy; democracy from 1974, EU member from 1986. Episodes: the 1974–75 revolution; IMF programmes in 1977–78 and 1983–85; the euro from 1999; the 2011–14 bailout programme; 2020.",
'GRC':"Small economy built on tourism and shipping; EU member from 1981, euro from 2001. Episodes: return to democracy in 1974; high deficits and inflation in the 1980s; the 2010 sovereign-debt crisis and successive bailouts; 2020.",
'TUR':"Large emerging economy with a long history of high inflation and boom–bust cycles. Episodes: the 1978–80 balance-of-payments crisis and 1980 liberalization; the 1994 and 2001 financial crises; disinflation in the 2000s; the 2018 currency crisis; the 2021–22 inflation surge.",
'JPN':"Export-led high growth followed by long stagnation. Episodes: the 1973 oil shock; the 1985 Plaza Accord and the late-1980s asset bubble; the 1990–91 bust; the 1997–98 banking crisis; zero rates from 1999; Abenomics from 2013.",
'KOR':"Export-led industrializer that became a high-income economy. Episodes: the 1980 contraction (oil shock and political crisis); the 1997–98 Asian financial crisis and IMF programme; the 2009 slowdown; 2020.",
'AUS':"Commodity exporter with a floating dollar since 1983. Episodes: the early-1980s and 1990–91 recessions; the 2000s mining boom; no recession in 2009; the 2020 contraction was the first since 1991.",
'IND':"Large, fast-growing, once heavily regulated economy. Episodes: the 1979 drought and oil shock; the 1991 balance-of-payments crisis and liberalization; faster growth in the 2000s; the 2008–09 slowdown; the 2020 lockdown.",
'IDN':"Populous commodity exporter. Episodes: the 1970s oil booms; diversification in the 1980s; the 1997–98 Asian crisis (rupiah collapse, banking crisis, political transition); steady growth near 5\\% since; 2020.",
'THA':"Manufacturing and tourism economy in Southeast Asia. Episodes: rapid growth from the mid-1980s; the July 1997 float of the baht that set off the Asian financial crisis; the 2011 floods; the 2020 collapse of tourism.",
'ZAF':"Mineral exporter shaped by apartheid-era sanctions and post-1994 reforms. Episodes: 1980s sanctions and the 1985 debt standstill; the 1994 democratic transition; the 2000s commodity boom; the 2009 recession; 2020.",
}

THE={'USA':'the United States','GBR':'the United Kingdom','NLD':'the Netherlands'}
def nm_(iso,cap=False):
    n=THE.get(iso,S[iso]['name']); return n[0].upper()+n[1:] if cap else n
CA=P[(P.year>=1970)&(P.year<=2022)].groupby('iso').CA_GDP.apply(lambda x:(x.dropna()<0).mean())
def word_coup(r):
    return 'barely' if r<0.2 else ('loosely' if r<0.5 else ('clearly' if r<0.75 else 'tightly'))
NUM={0:'none',1:'one',2:'two',3:'three',4:'four',5:'five'}
def yrs(n): return f"{n} year" if n==1 else f"{n} years"
def v1(r): return 'ran against' if r<-0.2 else ('was barely related to' if r<0.2 else ('moved loosely with' if r<0.5 else ('moved clearly with' if r<0.75 else 'moved tightly with')))
def v2(r): return 'run against' if r<-0.2 else ('been barely related to' if r<0.2 else ('moved loosely with' if r<0.5 else ('moved clearly with' if r<0.75 else 'moved tightly with')))

def reading(iso):
    s=S[iso]; A=s['anat']; nm=nm_(iso,True); ref='the 26' if iso in XISOS else 'the other 25'
    out=[]
    # 1 swing anatomy
    if A['I']>=A['C']+0.15: drv=f"Growth swings are investment-led: investment accounts for {share(A['I'])} of the variance of GDP growth, consumption for {share(A['C'])}"
    elif A['C']>=A['I']+0.15: drv=f"Growth swings run mainly through consumption ({share(A['C'])} of the variance of GDP growth) more than investment ({share(A['I'])})"
    else: drv=f"Consumption and investment carry the swings about equally ({share(A['C'])} and {share(A['I'])} of the variance of GDP growth)"
    if A['NX']<=-0.1: nx="; net exports cushion them (they rise when domestic demand falls, mostly because imports drop)"
    elif A['NX']>=0.1: nx="; net exports add to them, a sign of export-driven cycles"
    else: nx="; net exports matter little for the swings"
    out.append(drv+nx+'.')
    # 2 global recessions
    neg=[y for y in GL if s['gr_global'][str(y)] is not None and s['gr_global'][str(y)]<0]
    ncov=sum(1 for y in GL if s['gr_global'][str(y)] is not None); of=('the five global recession years' if ncov==5 else f"the {NUM[ncov]} global recession years its data cover")
    if len(neg)==0: gtxt=f"{nm} did not contract in any of {of}."
    elif len(neg)==ncov: gtxt=f"{nm} contracted in all {'five' if ncov==5 else NUM[ncov]} global recession years{'' if ncov==5 else ' its data cover'}."
    else: gtxt=f"It contracted in {NUM[len(neg)]} of {of} ({', '.join(map(str,neg))})."
    out.append(gtxt)
    # 3 coupling
    a,b=s['coup_7089'],s['coup_9022']
    if b-a>0.15 and v1(a)==v1(b): ctxt=f"Its business cycle {v1(a)} {ref} before 1990 (correlation {sg(a,2)}) and even more so since (correlation {sg(b,2)})."
    elif b-a>0.15: ctxt=f"Before 1990 its business cycle {v1(a)} {ref} (correlation {sg(a,2)}); since then it has {v2(b)} them (correlation {sg(b,2)})."
    elif a-b>0.15: ctxt=f"Unusually, its cycle was more tied to {ref} before 1990 (correlation {sg(a,2)}) than since (correlation {sg(b,2)})."
    else: ctxt=f"Its cycle was {word_coup((a+b)/2)} tied to {ref} in both halves of the period (correlation {sg(a,2)} before 1990, {sg(b,2)} since)."
    out.append(ctxt)
    # 4 budget and debt
    bc=s['bal_cyc']; fr=s['fiscal_from']
    since='' if fr<=1970 else f" (data from {fr})"
    if bc>=0.3: btxt=f"The budget works as a shock absorber{since}: the balance improves in booms and worsens in slumps (correlation with the cycle {sg(bc,2)})"
    elif bc>-0.1: btxt=f"The budget balance{since} is only loosely tied to the cycle (correlation {sg(bc,2)})"
    else: btxt=f"The budget balance{since} has tended to move against the cycle's stabilizing direction (correlation {sg(bc,2)})"
    d0,y0=s['debt_start']; d1=s['debt_2022']; pk,py=s['debt_peak']
    rev=(d1 is not None) and pk>d1*1.3 and py not in (y0,2022)
    if d1 is not None and d1>d0*1.5 and not rev: dtxt=f", and public debt has ratcheted up from {pc(d0)} of GDP in {y0} to {pc(d1)} in 2022"
    elif d1 is not None and d1>d0*1.15: dtxt=f", and public debt rose from {pc(d0)} of GDP in {y0} to {pc(d1)} in 2022"
    elif d1 is not None and d1<d0*0.75: dtxt=f", and public debt has fallen from {pc(d0)} of GDP in {y0} to {pc(d1)} in 2022"
    elif d1 is not None and d1<d0*0.87: dtxt=f", and public debt eased from {pc(d0)} of GDP in {y0} to {pc(d1)} in 2022"
    else: dtxt=f", and public debt ended near where it started ({pc(d0)} of GDP in {y0}, {pc(d1)} in 2022)"
    if py not in (y0,2022) and pk>max(d0,d1 or 0)*1.15: dtxt+=f" after peaking at {pc(pk)} in {py}"
    out.append(btxt+dtxt+'.')
    # 5 money and rates
    ip,iy=s['infl_peak']
    rt=f"Inflation peaked at {pc(ip)} in {iy} (median {pc(s['infl_median'],1)} over the period)"
    if s['zlb_years']>0: rt+=f"; short-term rates sat at or near zero in {yrs(s['zlb_years'])} from {s['zlb_first']}"
    if s['rr_mean'] is not None: rt+=f"; the real short rate averaged {sg(s['rr_mean'])}\\%"+(f" from {s['rr_from']}" if s.get('rr_from') else '')+f" and was negative in {yrs(s['rr_neg_years'])}"
    out.append(rt+'.')
    # 6 external
    o0,o1=s['open_1970'],s['open_2022']
    et=f"Trade rose from {pc(o0)} to {pc(o1)} of GDP" if o1>o0*1.2 else (f"Trade fell from {pc(o0)} to {pc(o1)} of GDP" if o1<o0*0.85 else f"Trade stayed near {pc((o0+o1)/2)} of GDP")
    cm=s['ca_mean']; nd=CA[iso]; et+=f"; the current account averaged {sg(cm)}\\% of GDP" + (f", in surplus in {100*(1-nd):.0f}\\% of years" if cm>0 else f", in deficit in {100*nd:.0f}\\% of years")
    out.append(et+'.')
    return ' '.join(out)

def notes(iso):
    s=S[iso]; fx=FIX[iso]; n=[]
    for y,old,new in fx.get('growth_patch',[]):
        n.append(f"GDP growth in {y} set to {f(new)}\\% (Penn World Table) instead of {f(old)}\\% in the source (splice error).")
    if iso in EXTRA_NOTES: n.append(EXTRA_NOTES[iso])
    v=fx['contrib_validation']; meth='CPI-deflated consumption and investment' if fx['contrib_method']=='cpi' else 'GDP-deflated components'
    vw=max(1971,fx.get('contrib_from',0),fx.get('components_from',0)+1,fx.get('gdp_from',0)+1)
    n.append(f"Contributions use {meth}; correlation with Penn World Table volume contributions {vw}–2019: C {f(v['C'],2)}, I {f(v['I'],2)}, NX {f(v['NX'],2)}"+(" (PWT timing averaged to calendar years)" if iso=='AUS' else '')+('; agreement is weak, so read the split with caution' if min(v.values())<0.6 else '')+'.')
    if fx.get('contrib_blank'): n.append(f"Contributions not shown for {lst(fx['contrib_blank'])} (national-accounts break: components miss GDP growth by more than 3 points).")
    fs=fx['fiscal']
    if fs.get('hist_from') is not None and fs['hist_from']<fs['weo_from'] and fs['weo_from']>1970:
        n.append(f"Budget: IMF World Economic Outlook from {fs['weo_from']}; earlier years (dotted) from the IMF's historical public-finance database, level-matched at {fs['weo_from']}.")
    elif fs['weo_from']>1970:
        n.append(f"Budget series start in {fs['weo_from']} (earlier sources use a different coverage of government).")
    if fs.get('breaks'): n.append(f"Budget coverage changes in {lst(fs['breaks'])} (dotted vertical line).")
    db=fx['debt']
    if db.get('hdd_ratio') and db['weo_from']>1970: n.append(f"Debt: WEO from {db['weo_from']}; earlier years (dotted) from the IMF Historical Public Debt Database, rescaled by {f(db['hdd_ratio'],2)} to meet WEO.")
    if db.get('hdd_ratio') and FIX[iso].get('debt_interp'): n.append(f"Debt interpolated for {lst(FIX[iso]['debt_interp'])} (gap in the historical series).")
    elif db.get('hdd_ratio_too_far'): n.append(f"Debt series start in {db['weo_from']} (the historical series differs too much in coverage to splice).")
    if fx.get('money_dropped'): n.append(f"Money growth dropped for {lst(fx['money_dropped'])} (definitional breaks).")
    if fx.get('ltrate_dropped'): n.append(f"Long-term rate dropped for {lst(fx['ltrate_dropped'])} (placeholder value in the source).")
    if fx.get('unemp_break'): n.append(f"Unemployment definition changes in {fx['unemp_break']}.")
    cov=[]
    if s['strate_start'] and s['strate_start']>1970: cov.append(f"short rate from {s['strate_start']}")
    if s['ltrate_start'] and s['ltrate_start']>1970: cov.append(f"long rate from {s['ltrate_start']}")
    if s['money_end'] and s['money_end']<2022: cov.append(f"money to {s['money_end']}")
    if s['unemp_start'] and s['unemp_start']>1970: cov.append(f"unemployment from {s['unemp_start']}")
    if s['ca_start']>1970: cov.append(f"current account from {s['ca_start']}")
    if cov: n.append('Coverage: '+'; '.join(cov)+'.')
    return ' '.join(n)

def table(iso):
    s=S[iso]; A=s['anat']; g=s['gr_global']
    sh1,sh2=s['shares_1970'],s['shares_2022']
    def ar(a,b,d=0): return f"{f(a,d)} → {f(b,d)}"
    L=[('GDP growth, mean (s.d.)',f"{pc(s['growth_mean'],1)} ({f(s['growth_sd'])})"),
       ('Contractions · worst year',f"{s['n_neg']} · {pc(s['worst'][0],1)} ({s['worst'][1]})"),
       ('Growth ’75 · ’82 · ’91 · ’09 · ’20',' · '.join(sg(g[str(y)]) for y in GL)),
       ('Variance share C · I · NX',f"{share(A['C'])} · {share(A['I'])} · {share(A['NX'])}"),
       (f"Consumption, \\% GDP {yy(s.get('shares_from',1970))}→’22",ar(sh1['cons'],sh2['cons'])),
       (f"Investment, \\% GDP {yy(s.get('shares_from',1970))}→’22",ar(sh1['inv'],sh2['inv'])+f" · peak {f(s['inv_peak'][0],0)} ({s['inv_peak'][1]})"),
       ('Cycle corr. ’70–89 → ’90–22',f"{sg(s['coup_7089'],2)} → {sg(s['coup_9022'],2)}"),
       ('Unemployment, mean (peak)',(f"{pc(s['unemp_mean'],1)} ({pc(s['unemp_peak'][0],1)}, {s['unemp_peak'][1]})" if s['unemp_mean'] is not None else '–')),
       ('Crisis onsets (GMD dating)',(f"banking {lst(s['crisis_bank'])}; currency {lst(s['crisis_curr'])}"+(f"; sovereign {lst(s['crisis_sov'])}" if s['crisis_sov'] else '')) if s.get('crisis_covered',True) else 'not dated in the source')]
    R=[('Budget balance, mean (worst)',f"{sg(s['bal_mean'])} ({sg(s['bal_worst'][0])}, {s['bal_worst'][1]})"),
       ('Spending, \\% GDP',f"{f(s['spend_first'][0],0)} ({s['spend_first'][1]}) → {f(s['spend_2022'],0)} (2022)"),
       ('Debt, \\% GDP',f"{f(s['debt_start'][0],0)} ({s['debt_start'][1]}) → {f(s['debt_2022'],0)} · peak {f(s['debt_peak'][0],0)} ({s['debt_peak'][1]})"),
       ('Inflation mean · median (peak)',f"{f(s['infl_mean'])} · {f(s['infl_median'])} ({pc(s['infl_peak'][0],0)}, {s['infl_peak'][1]})"),
       ('Short rate peak · zero-rate yrs',(f"{pc(s['strate_peak'][0],1)} ({s['strate_peak'][1]}) · {s['zlb_years']}" if s['strate_peak'] else '–')+(f" (from {s['zlb_first']})" if s['zlb_first'] else '')),
       ('Real short rate · years below 0',(f"{sg(s['rr_mean'])}\\% · {s['rr_neg_years']}"+(f" (from {s['rr_from']})" if s.get('rr_from') else '') if s['rr_mean'] is not None else '–')),
       ('Real broad money, mean (s.d.)',(f"{sg(s['rmoney_mean'])}\\% ({f(s['rmoney_sd'])})" if s['rmoney_mean'] is not None else '–')),
       (f"Trade, \\% GDP {yy(s.get('open_from',1970))}→’22",f"{f(s['open_1970'],0)} → {f(s['open_2022'],0)}"),
       ('Current account, mean (range)',f"{sg(s['ca_mean'])} ({sg(s['ca_min'][0])} to {sg(s['ca_max'][0])})")]
    rows=[]
    for (a,b),(c,d) in zip(L,R):
        rows.append(f"{a} & {b} & {c} & {d} \\\\")
    return ("{\\sffamily\\fontsize{7.2}{8.9}\\selectfont\\setlength{\\tabcolsep}{3pt}\\renewcommand{\\arraystretch}{1.0}\n"
            "\\begin{tabularx}{\\textwidth}{@{}>{\\raggedright\\leavevmode\\color{ink2}}p{0.2\\textwidth}>{\\raggedright\\leavevmode}X@{\\hspace{10pt}}>{\\raggedright\\leavevmode\\color{ink2}}p{0.2\\textwidth}>{\\raggedright\\leavevmode\\arraybackslash}X@{}}\n"
            "\\toprule\n\\multicolumn{2}{@{}l}{\\bfseries Growth, demand and the cycle} & \\multicolumn{2}{l@{}}{\\bfseries Budget, money, prices and the outside world} \\\\\n\\midrule\n"
            +'\n'.join(rows)+"\n\\bottomrule\n\\end{tabularx}}\n")

def country_page(k,iso,total=26,kicker='ECONOMY',figw='0.97'):
    s=S[iso]; reg=esc(s['region'].replace('Added · ',''))
    return f"""
\\clearpage
\\phantomsection\\label{{c:{iso}}}\\addcontentsline{{toc}}{{subsection}}{{{esc(s['name'])}}}
{{\\sffamily\\color{{muted}}\\fontsize{{7.5}}{{9}}\\selectfont {kicker} {k} OF {total} \\enspace·\\enspace {reg.upper()}}}\\\\[-1pt]
{{\\sffamily\\bfseries\\fontsize{{19}}{{22}}\\selectfont {esc(s['name'])}}}\\hfill{{\\sffamily\\color{{muted}}\\fontsize{{11}}{{13}}\\selectfont {iso}}}\\par
\\vspace{{1pt}}{{\\color{{rule}}\\rule{{\\textwidth}}{{0.5pt}}}}\\par\\vspace{{2pt}}
{{\\fontsize{{8.3}}{{10.1}}\\selectfont\\itshape {CONTEXT[iso]}}}\\par
\\vspace{{3pt}}
{{\\centering\\includegraphics[width={figw}\\textwidth]{{fig/{iso}.png}}\\par}}
\\vspace{{1pt}}
{table(iso)}
\\vspace{{3pt}}
{{\\fontsize{{9}}{{11.4}}\\selectfont\\textbf{{\\sffamily Reading.}} {reading(iso)}\\par}}
\\vspace{{3pt}}
{{\\fontsize{{6.9}}{{8.4}}\\selectfont\\color{{ink2}}\\textsf{{Data notes.}} {notes(iso)}\\par}}
"""

# ---------- global and overview numbers ----------
wg=GB.world_growth; nc=GB.n_contracting; oil=GB.oil_real_2015usd; imp=GB.world_imports_GDP; im=GB.infl_med
sr=GB.share_raising; hi_share=[int(y) for y in GB.index[sr>=0.75]]
T=SY['tests']
def trow(lab,ch):
    t=T[ch]; c=lambda k:f"{sg(t[k][0],2)} ({f(t[k][1],3)})"+('$^{*}$' if t[k][1]<0.05 else '')
    return f"{lab} & {SY['n'][ch]} & {c('lead2')} & {c('lead1')} & {c('same')} & {c('after2')} \\\\"
dec=['1970s','1980s','1990s','2000s','2010-22']
cd={d:np.array([S[i]['coup_dec'][d] for i in I26]) for d in dec}

def summary_table2():
    rows=[]; prev=None
    for iso,name,reg in ORDER:
        s=S[iso]
        if prev and reg!=prev: rows.append('\\addlinespace[2pt]')
        prev=reg
        sp=s['strate_peak']
        rows.append(f"\\hyperref[c:{iso}]{{{esc(name)}}} & {f(s['unemp_mean'])} & {f(s['infl_median'])} & "
                    f"{(f(sp[0])+' ('+yy(sp[1])+')') if sp else '–'} & {s['zlb_years']} & {sg(s['rr_mean'])} & {sg(s['rmoney_mean'])} & "
                    f"{sg(s['bal_worst'][0])} ({yy(s['bal_worst'][1])}) & {f(s['debt_peak'][0],0)} ({yy(s['debt_peak'][1])}) & "
                    f"{len(s['crisis_bank'])} & {len(s['crisis_curr'])} & {len(s['crisis_sov'])} \\\\")
    return '\n'.join(rows)

def summary_table():
    rows=[]
    prev=None
    for iso,name,reg in ORDER:
        s=S[iso]
        if prev and reg!=prev: rows.append('\\addlinespace[2pt]')
        prev=reg
        rows.append(f"\\hyperref[c:{iso}]{{{esc(name)}}} & {f(s['growth_mean'])} & {f(s['growth_sd'])} & {sg(s['worst'][0])} ({yy(s['worst'][1])}) & {s['n_contract_global']}/5 & {sg(s['coup_7089'],2)} & {sg(s['coup_9022'],2)} & {share(s['anat']['I'])} & {sg(s['bal_mean'])} & {f(s['debt_start'][0],0)}→{f(s['debt_2022'],0)} & {f(s['infl_peak'][0],0)} ({yy(s['infl_peak'][1])}) & {f(s['open_1970'],0)}→{f(s['open_2022'],0)} & {sg(s['ca_mean'])} \\\\")
    return '\n'.join(rows)

pre=r"""\documentclass[10pt]{article}
\usepackage[a4paper,top=12mm,bottom=15mm,left=12mm,right=12mm,footskip=7mm]{geometry}
\usepackage{fontspec}
\setmainfont{texgyrepagella}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic,Ligatures=TeX,Numbers=Lining]
\setsansfont{Inter}[Numbers={Lining,Monospaced}]
\usepackage{unicode-math}\setmathfont{latinmodern-math.otf}
\usepackage{xcolor,graphicx,booktabs,tabularx,array,fancyhdr,titlesec,enumitem,multicol}
\usepackage[hidelinks]{hyperref}
\definecolor{ink}{HTML}{0B0B0B}\definecolor{ink2}{HTML}{52514E}\definecolor{muted}{HTML}{898781}
\definecolor{rule}{HTML}{C3C2B7}\definecolor{band}{HTML}{EFEEE9}\definecolor{accent}{HTML}{2A78D6}
\color{ink}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\pagestyle{fancy}\fancyhf{}\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\sffamily\fontsize{7}{8}\selectfont\color{muted}Economic Fibrillation · The 26 economies, 1970–2022}
\fancyfoot[R]{\sffamily\fontsize{7}{8}\selectfont\color{muted}\thepage}
\titleformat{\section}{\sffamily\bfseries\fontsize{15}{18}\selectfont}{}{0pt}{}
\titlespacing*{\section}{0pt}{0pt}{6pt}
\titleformat{\subsection}{\sffamily\bfseries\fontsize{10.5}{13}\selectfont}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{8pt}{3pt}
\setlist{itemsep=1pt,topsep=2pt,leftmargin=12pt}
\renewcommand{\arraystretch}{1.12}
\begin{document}
"""

def cover():
    c7=np.mean([S[i]['coup_7089'] for i in I26]); c9=np.mean([S[i]['coup_9022'] for i in I26])
    imp=GB.world_imports_GDP; nc=GB.n_contracting; tl=SY['tests']['strate']['lead2']
    glance=(f"{{\\sffamily\\fontsize{{8}}{{10}}\\selectfont\\color{{muted}} AT A GLANCE}}\\par\\vspace{{3mm}}\n"
      "{\\sffamily\\setlength{\\tabcolsep}{0pt}\\begin{tabularx}{\\textwidth}{@{}>{\\raggedright\\arraybackslash}X@{\\hspace{6mm}}>{\\raggedright\\arraybackslash}X@{\\hspace{6mm}}>{\\raggedright\\arraybackslash}X@{\\hspace{6mm}}>{\\raggedright\\arraybackslash}X@{}}\n"
      f"{{\\bfseries\\fontsize{{17}}{{20}}\\selectfont {int(nc[2020])} of 26}} & {{\\bfseries\\fontsize{{17}}{{20}}\\selectfont {f(c7,2)}\\,→\\,{f(c9,2)}}} & {{\\bfseries\\fontsize{{17}}{{20}}\\selectfont {f(imp[1970],0)}\\%\\,→\\,{f(imp[2022],0)}\\%}} & {{\\bfseries\\fontsize{{17}}{{20}}\\selectfont 2 years}} \\\\[3pt]\n"
      f"{{\\fontsize{{8}}{{10.5}}\\selectfont\\color{{ink2}} economies shrank in 2020; {int(nc[2009])} did in 2009, against {int(nc[1982])}–{int(nc[1975])} in 1975, 1982 and 1991}} & "
      f"{{\\fontsize{{8}}{{10.5}}\\selectfont\\color{{ink2}} average correlation of each economy's cycle with the other 25, 1970–89 and 1990–2022}} & "
      f"{{\\fontsize{{8}}{{10.5}}\\selectfont\\color{{ink2}} imports as a share of the combined GDP of the 26, 1970 and 2022}} & "
      f"{{\\fontsize{{8}}{{10.5}}\\selectfont\\color{{ink2}} how far synchronized interest-rate rises run ahead of global recessions (\\textit{{p}} = {f(tl[1],3)})}} \\\\\n"
      "\\end{tabularx}}\n")
    return r"""
\thispagestyle{empty}
\vspace*{20mm}
{\sffamily\color{muted}\fontsize{9}{11}\selectfont ECONOMIC FIBRILLATION \enspace·\enspace RESEARCH ATLAS}\par\vspace{6mm}
{\sffamily\bfseries\fontsize{34}{38}\selectfont The 26 economies,\\[2pt] 1970–2022}\par\vspace{5mm}
{\fontsize{13}{17}\selectfont\itshape Growth, demand, budgets, debt, money, interest rates and trade,\\ country by country, with the global forces that tie them together}\par
\vspace{8mm}{\color{rule}\rule{\textwidth}{0.6pt}}\par\vspace{5mm}
\begin{minipage}[t]{0.48\textwidth}\fontsize{9.5}{12.5}\selectfont
This atlas sets out, for each of the 26 economies in Paper~1, the statistics that sit underneath its business cycle: what grew and what shrank, how the budget and public debt behaved, what money, inflation and interest rates did, and how open each economy became. It is descriptive by design. It does not test a hypothesis; it shows the ground the hypotheses have to stand on.
\end{minipage}\hfill
\begin{minipage}[t]{0.46\textwidth}\sffamily\fontsize{8.3}{11.5}\selectfont
\textbf{Inside}\\[2pt]
How to read the pages \dotfill\ \pageref{p:read}\\
What the numbers mean \dotfill\ \pageref{p:defs}\\
Global forces \dotfill\ \pageref{p:global}\\
The 26 side by side \dotfill\ \pageref{p:overview}\\
Headline numbers \dotfill\ \pageref{p:summary}\\
Country pages \dotfill\ \pageref{c:USA}--\pageref{c:ZAF}\\
Five more economies \dotfill\ \pageref{p:extra}--\pageref{c:IRN}\\
Data sources and repairs \dotfill\ \pageref{p:data}
\end{minipage}
\par\vfill
"""+glance+r"""
\vfill
{\sffamily\fontsize{8}{11}\selectfont\color{ink2}
\begin{tabularx}{\textwidth}{@{}XXXX@{}}
\textbf{North America} & \textbf{Western Europe} & \textbf{Nordics, South \& Turkey} & \textbf{Asia-Pacific \& Africa}\\
United States\newline Canada\newline Mexico & Germany, France\newline United Kingdom, Italy\newline Netherlands, Belgium\newline Austria, Switzerland & Sweden, Norway\newline Denmark, Finland\newline Spain, Portugal\newline Greece, Turkey & Japan, South Korea\newline Australia, India\newline Indonesia, Thailand\newline South Africa\\
\end{tabularx}}\par
\vspace{7mm}
{\sffamily\fontsize{7.5}{10}\selectfont\color{muted}October 2026 \enspace·\enspace Annual data, reproducible from the accompanying scripts and CSV files}
"""

howto=r"""
\clearpage
\section{How to read the pages}\label{p:read}
Every country gets one page with the same nine panels in the same places, so you can flip between economies and compare like with like. All panels run from 1970 to 2022 (annual data). The pale grey vertical bands mark the five \textbf{global recession years}, 1975, 1982, 1991, 2009 and 2020, the same dating used in Paper~1.

\begin{multicols}{2}\fontsize{8.6}{10.9}\selectfont
\textbf{Top row: growth and the cycle.}
\begin{itemize}
\item \textbf{Real GDP growth.} Blue bars are growth, red bars contraction.
\item \textbf{Where the swing lives.} Each year's growth split into what consumption (household plus government), investment and net exports added, in percentage points. The black line is GDP growth. The subtitle gives each part's share of the \emph{variance} of growth: the part that moves with the ups and downs, not the part that is large on average. Grey crosses mark years where the national accounts break and the split is not shown.
\item \textbf{In step with the world?} The country's business cycle (blue) against the average cycle of the other 25 (grey dashed), both standardized. The subtitle gives their correlation before and after 1990.
\end{itemize}
\textbf{Middle row: the state.}
\begin{itemize}
\item \textbf{Government budget.} General-government revenue (blue) and spending (orange); the shaded gap is the deficit (red) or surplus (blue). The subtitle gives the average balance and its correlation with the cycle: positive means the budget improves in booms and worsens in slumps, the normal stabilizing pattern.
\item \textbf{Government debt.} Gross general-government debt.
\item \textbf{Interest rates and inflation.} Short-term (money-market) rate, long-term (government bond) rate and consumer-price inflation.
\end{itemize}
\columnbreak
\textbf{Bottom row: money and the outside world.}
\begin{itemize}
\item \textbf{Real broad-money growth.} Growth of broad money (M2, or M3 where M2 stops) minus inflation, in log points.
\item \textbf{Trade.} Exports and imports as shares of GDP.
\item \textbf{Current account.} Surplus (blue) or deficit (red) as a share of GDP.
\end{itemize}
\textbf{Two marks that signal a data seam.} A \emph{dotted} line segment means an older series spliced onto the main one (the vertical dotted line marks the join). Treat the level before the join as approximate and the year-to-year movement as reliable. A blank stretch means the data are missing or were removed because the source series breaks; each page's \emph{Data notes} line says which.

\textbf{Under each figure} sits a table of headline numbers and a short \emph{Reading} paragraph generated from those numbers by fixed rules, so every economy is described by the same yardstick. The one-line context under each country's name lists well-known episodes, as a map for the charts rather than a claim made by them.

\textbf{Colours} keep one meaning within a chart: blue is the main series (or something positive), red marks contraction, deficit or falling, orange and green are the second and third series. Every chart with more than one series has a legend, so nothing depends on colour alone.
\end{multicols}
"""

defs=r"""
\vspace{4pt}
\section{What the numbers mean}\label{p:defs}
\begin{multicols}{2}\fontsize{8.6}{10.9}\selectfont
\textbf{Growth.} $g_t = 100\,(Y_t/Y_{t-1}-1)$, where $Y$ is real GDP in national currency at constant prices.

\textbf{Contributions to growth.} With nominal shares $s_{k,t-1}=K_{t-1}/\mathit{GDP}_{t-1}$ and real growth $g_{k,t}$ of component $k$,
\[ c_{k,t} = s_{k,t-1}\, g_{k,t}, \qquad g_t = c_{C,t}+c_{I,t}+c_{\mathit{NX},t}. \]
Consumption $C$ includes government consumption; investment $I$ includes inventories; net exports $\mathit{NX}$ is what is left of growth after $C$ and $I$. Exports and imports are shown only as \emph{net} exports because no export or import price indices exist for all 26 economies; deflating them separately would mix price and volume. For each economy we deflate $C$ and $I$ either by the GDP deflator or by consumer prices, whichever better reproduces the volume-based contributions in the Penn World Table over 1971–2019 (median correlation 0.92 for $C$, 0.95 for $I$, 0.83 for $\mathit{NX}$).

\textbf{Share of growth variance.} $\beta_k = \mathrm{cov}(c_k,g)/\mathrm{var}(g)$. The $\beta_k$ add up to one, so a component that moves against growth gets a negative share (net exports usually do: imports fall in a slump). A share above 100\% is possible when another component offsets it.

\textbf{Business cycle.} The 2–9 year band of log real GDP, isolated with the same zero-phase Butterworth band-pass filter as Paper~1 (run-in from 1950). \emph{Correlation with the rest} is the correlation between an economy's cycle and the average of the other 25 standardized cycles over 1970–89 and 1990–2022 (and by decade in the overview).

\textbf{Synchronization $r(t)$.} The Kuramoto order parameter $r(t)=\left|\tfrac{1}{N}\sum_j e^{i\theta_j(t)}\right|$, where $\theta_j(t)$ is the Hilbert phase of economy $j$'s band-passed series. $r=1$ when all economies sit at the same point of their cycles; for 26 independent cycles it would hover around 0.2.

\textbf{Budget balance} is general-government revenue minus spending (net lending), as \% of GDP; revenue is computed as spending plus balance so the two always agree. \textbf{Debt} is gross general-government debt.

\textbf{Real short rate} $=$ short-term nominal rate $-$ CPI inflation. \textbf{Zero-rate years}: years with a short rate at or below 0.5\%.

\textbf{Real broad-money growth} $= 100\,\Delta\ln M_t - 100\ln(1+\pi_t)$, with $M$ = M2 (chain-linked to M3, or M1, where M2 stops) and $\pi$ CPI inflation. Using logs keeps high-inflation years comparable.

\textbf{Trade} is exports and imports of goods and services, \% of GDP. \textbf{Current account} is \% of GDP.

\textbf{Crisis onsets} are the first years of banking, currency and sovereign-debt crises as dated in the Global Macro Database.

\textbf{World aggregates} (global pages) weight each economy by its real GDP in US dollars.
\end{multicols}
"""

g_text=f"""
\\clearpage
\\section{{Global forces, I: output, prices and trade}}\\label{{p:global}}
\\noindent\\includegraphics[width=\\textwidth]{{fig/global_real.png}}\\par
\\begin{{multicols}}{{2}}\\fontsize{{9}}{{11.6}}\\selectfont
\\textbf{{Two recessions were truly global.}} World growth (the GDP-weighted average of the 26) averaged {f(wg.mean())}\\% a year and turned negative only in 2009 ({f(wg[2009])}\\%) and 2020 ({f(wg[2020])}\\%). The count of shrinking economies shows why those two stand apart: {int(nc[2009])} and {int(nc[2020])} of the 26 contracted, against {int(nc[1975])} in 1975 and {int(nc[1982])} in 1982 and 1991. The earlier global recessions were a slowdown in the aggregate and a contraction for a minority, mostly the advanced economies; emerging economies often kept growing.

\\textbf{{Oil and inflation.}} The real oil price more than tripled in 1974 and doubled again in 1979–80, peaking near \\${f(oil[1980],0)} a barrel (2015 dollars) in 1980. It fell to \\${f(oil[1998],0)} in 1998 and climbed to \\${f(oil[2011],0)} in 2011. Both oil shocks came with an inflation surge across the 26 (median {f(im[1974])}\\% in 1974 and {f(im[1980])}\\% in 1980). From the mid-1990s until 2021 the median stayed between {f(im.loc[1995:2021].min())}\\% and {f(im.loc[1995:2021].max())}\\%, before jumping to {f(im[2022])}\\% in 2022.

\\columnbreak
\\textbf{{Trade dependence more than doubled.}} Imports of the 26 rose from {f(imp[1970],0)}\\% of their combined GDP in 1970 to {f(imp[2022],0)}\\% in 2022. The dips in 2009 and 2020 show trade falling faster than output, which is how a shock in one place reaches the others.

\\textbf{{Synchronization.}} The bottom-right panel repeats Paper~1's order parameter on three channels. Real GDP, investment and short-term rates share their peaks around the oil shocks, 2000, 2008 and 2020–21. After 2009 the GDP channel collapses (to near zero by 2012): economies fell together, then recovered at different speeds. The last two or three years of any band-passed series are less reliable because the filter runs out of future data.
\\end{{multicols}}
"""

m_text=f"""
\\clearpage
\\section{{Global forces, II: money, the dollar and crises}}
\\noindent\\includegraphics[width=\\textwidth]{{fig/global_money.png}}\\par
\\begin{{multicols}}{{2}}\\fontsize{{9}}{{11.6}}\\selectfont
\\textbf{{Rates moved together, then apart, then together.}} The US short-term rate and the median of the other economies tracked each other through the 1970s and early 1980s, parted in the late 1980s, when the median kept rising to {f(GB.strate_med_ex_us[1990])}\\% in 1990 (the years of German reunification and strains in Europe's exchange-rate mechanism) while US rates fell, and converged near zero after 2009.

\\textbf{{Tightening in unison.}} The share of economies raising short-term rates reached three quarters or more in {', '.join(map(str,hi_share))}. Five of these runs (1973–74, 1980–81, 1989–90, 2005–07 and 2018) end one or two years before a global recession; 2000, 2011 and 2022 do not. This is the synchronized-tightening pattern found in our earlier analysis. The table below re-runs that test on the repaired data.

\\textbf{{The dollar and crises.}} The real effective dollar peaked in 1985 ({f(GB.us_reer[1985],0)}), 2001–02 ({f(GB.us_reer[2002],0)}) and 2022 ({f(GB.us_reer[2022],0)}), and bottomed in 1995 ({f(GB.us_reer[1995],0)}) and 2011 ({f(GB.us_reer[2011],0)}). Banking-crisis onsets cluster in 1990–92 (the Nordic and Japanese crises) and in 2008, when {int(GB.banking_onsets[2008])} of the 26 economies had one.
\\end{{multicols}}
\\vspace{{2pt}}
{{\\sffamily\\fontsize{{7.6}}{{9.6}}\\selectfont
\\begin{{tabularx}}{{\\textwidth}}{{@{{}}Xcrrrr@{{}}}}
\\toprule
 & & \\multicolumn{{4}}{{c}}{{Correlation of $r(t)$ with global-recession years (permutation $p$)}}\\\\
\\cmidrule(l){{3-6}}
Channel & Economies & $r$ leads by 2 years & leads by 1 year & same year & 2 years after \\\\
\\midrule
{trow('Real GDP','GDP')}
{trow('Real investment','inv')}
{trow('Short-term interest rate','strate')}
\\bottomrule
\\end{{tabularx}}}}\\par
{{\\fontsize{{7.4}}{{9}}\\selectfont\\color{{ink2}} Circular-shift permutation over 1970–2022 (53 years), so the smallest possible $p$ is 1/53 = 0.019; $^{{*}}$ marks $p<0.05$. Five events and twelve tests here, so roughly one false positive is expected by chance at the 5\\% level. The rate result is unchanged from the earlier analysis. With repaired investment data, investment synchronization peaks two years ahead ($p$ 0.038) rather than one ($p$ 0.057). Short-rate data cover 18 economies continuously from 1965.\\par}}
"""

ov_text=f"""
\\clearpage
\\section{{The 26 side by side}}\\label{{p:overview}}
\\noindent\\includegraphics[width=\\textwidth]{{fig/overview_heat.png}}\\par
\\begin{{multicols}}{{2}}\\fontsize{{9}}{{11.6}}\\selectfont
\\textbf{{Coupling rose almost everywhere.}} The left panel shows each economy's cycle correlated with the average of the other 25, decade by decade. The average was {f(cd['1970s'].mean(),2)} in the 1970s, {f(cd['1980s'].mean(),2)} in the 1980s and {f(cd['1990s'].mean(),2)} in the 1990s, then {f(cd['2000s'].mean(),2)} in the 2000s and {f(cd['2010-22'].mean(),2)} in 2010–22. Economies with a correlation of 0.75 or more went from {int((cd['1990s']>=0.75).sum())} in the 1990s to {int((cd['2010-22']>=0.75).sum())} in 2010–22. The biggest risers were India, South Africa, Turkey, Norway and Mexico. One caution: a single very large shared shock can dominate a decade's correlation, and the last two decades each contain one (2009 and 2020). The rise is real, but part of it is those two shocks.

\\columnbreak
\\textbf{{Who shrank, and when.}} The right panel gives growth in each global recession year (red: contraction). In 1975, 1982 and 1991 the damage was concentrated: much of Europe and North America slowed or shrank while South Korea, India, Indonesia and Thailand kept growing. In 2009 all but four contracted (South Korea, Australia, India and Indonesia grew); in 2020 everyone except Turkey did. That shift, from regional to universal contractions, is the pattern Paper~1 measures as rising synchronization.
\\end{{multicols}}
"""

sum_text=f"""
\\clearpage
\\section{{Headline numbers}}\\label{{p:summary}}
{{\\fontsize{{8.8}}{{11}}\\selectfont Averages over 1970–2022 unless stated. Click a name to jump to its page. Variance share I is investment's share of the variance of GDP growth; coupling is the correlation of the cycle with the other 25; global recessions counts contractions in 1975, 1982, 1991, 2009 and 2020.\\par}}
\\vspace{{4pt}}
{{\\sffamily\\fontsize{{7.1}}{{8.75}}\\selectfont\\setlength{{\\tabcolsep}}{{3.2pt}}
\\begin{{tabularx}}{{\\textwidth}}{{@{{}}Xrrrcrrrrrrrr@{{}}}}
\\toprule
 & \\multicolumn{{2}}{{c}}{{Growth, \\%}} & Worst & Global & \\multicolumn{{2}}{{c}}{{Coupling}} & Var. & Budget & Debt, \\% & Inflation & Trade, \\% & Current \\\\
\\cmidrule(lr){{2-3}}\\cmidrule(lr){{6-7}}
Economy & mean & s.d. & year & recessions & ’70–89 & ’90–22 & share I & balance & ’70→’22 & peak & ’70→’22 & account \\\\
\\midrule
{summary_table()}
\\bottomrule
\\end{{tabularx}}}}\\par
\\vspace{{4pt}}
\\vspace{{8pt}}
{{\\sffamily\\fontsize{{7.1}}{{8.75}}\\selectfont\\setlength{{\\tabcolsep}}{{3.2pt}}
\\begin{{tabularx}}{{\\textwidth}}{{@{{}}Xrrrrrrrrccc@{{}}}}
\\toprule
 & Unemploy- & Inflation & Short rate & Zero-rate & Real short & Real money & Worst budget & Debt & \\multicolumn{{3}}{{c}}{{Crisis onsets}} \\\\
\\cmidrule(l){{10-12}}
Economy & ment, mean & median & peak & years & rate, mean & growth, mean & balance & peak & bank & curr. & sov. \\\\
\\midrule
{summary_table2()}
\\bottomrule
\\end{{tabularx}}}}\\par
\\vspace{{4pt}}
{{\\fontsize{{7.6}}{{9.4}}\\selectfont\\color{{ink2}} All in \\% or \\% of GDP. Budget balance and debt start later than 1970 for some economies (see each country's data notes); debt ’70 is the first year available. Values in brackets are years. Short-rate, unemployment and money series start late or end early for some economies (see country pages). Crisis onsets are counts of first years of banking, currency and sovereign-debt crises in the Global Macro Database dating, 1970–2022.\\par}}
"""

# data notes page
def fixcount(key): return sum(1 for i in I26 if FIX[i].get(key))
nblank=sum(len(FIX[i].get('contrib_blank',[])) for i in I26); nmoney=sum(len(FIX[i].get('money_dropped',[])) for i in I26)
weo80=[S[i]['name'] for i in I26 if FIX[i]['fiscal']['weo_from']>1970 and FIX[i]['fiscal'].get('hist_from') is None]
data_text=f"""
\\clearpage
\\section{{Data sources and repairs}}\\label{{p:data}}
\\begin{{multicols}}{{2}}\\fontsize{{8.6}}{{11}}\\selectfont
\\subsection{{Sources}}
\\begin{{itemize}}
\\item \\textbf{{Global Macro Database}} (Müller, Xu, Lehbib and Chen, 2025; release of September 2026): national accounts, prices, interest rates, money, trade, current account, unemployment and crisis dates, and its cleaned copies of the IMF sources below.
\\item \\textbf{{IMF World Economic Outlook}}: general-government spending, balance and debt from the first year each is available (1980 for most advanced economies, 1988–2001 for the rest).
\\item \\textbf{{IMF Public Finances in Modern History}} (Mauro, Romeu, Binder and Zaman, 2015) and \\textbf{{IMF Historical Public Debt Database}} (Abbas and others, 2010): earlier budget and debt years.
\\item \\textbf{{Penn World Table 10.01}} (Feenstra, Inklaar and Timmer, 2015): volume checks on growth and on the contributions.
\\item \\textbf{{Oil}}: BP Statistical Review real price (2015 dollars) to 2015 via Our World in Data, extended with the EIA Brent price deflated by US CPI (the two agree within 0.1\\% on average over 1988–2015).
\\end{{itemize}}
\\subsection{{Repairs made while building the atlas}}
Checking every series against a second source turned up problems that would otherwise sit inside the charts. Each repair is listed on the country page it affects.
\\begin{{itemize}}
\\item \\textbf{{Budgets.}} The database's revenue series jump by 10–23 points of GDP in the year its source switches (for example 1980 for Sweden, Canada, Japan, Belgium, Denmark and Norway), most likely because the older sources cover only central government. We rebuilt spending and balance from the IMF WEO and spliced the IMF historical series only where it meets WEO closely (within 3 points for spending, 1.5 for the balance). Where it does not, the budget panel starts when WEO starts: {', '.join(weo80)}.
\\item \\textbf{{Debt}} had the same jumps (for example +20 points for the US in 2001 and +29 for Sweden in 1993). Debt now follows WEO, with the IMF historical debt series rescaled to meet it.
\\item \\textbf{{Exports and imports}} deflated with the GDP deflator carried large price effects: Indonesia's exports appeared to add 15 points to growth in 1998, when the rupiah collapsed. The atlas reports only net exports. {nblank} country-years where the components miss GDP growth by more than 3 points are left blank.
\\item \\textbf{{GDP growth}} in four country-years disagreed with both Penn World Table and Maddison by more than 2 points and was replaced: Austria 1988, Sweden 1981, Portugal 1988 and 1990.
\\item \\textbf{{Money.}} {nmoney} country-years were dropped where M2 breaks definition (for example the euro changeover in 1999 for Italy and Spain, Greece in 1999, Japan in 2001), flagged when M2 disagrees with both M1 and M3 or implies real growth beyond ±40\\%. Real money growth now uses logs throughout.
\\item \\textbf{{Other}}: a placeholder long-term rate for Mexico in 2021–22 (19.7\\%) was removed; South Africa's unemployment series changes definition in 1995.
\\end{{itemize}}
\\subsection{{What this means for the earlier results}}
\\begin{{itemize}}
\\item The synchronized-rates result does not change: rate synchronization leads the global recessions by two years with $p=0.019$.
\\item The imports and budget-spending channels in the earlier sequence used the series repaired here. Imports carried price effects, and spending carried the source jumps around 1980, the year many economies switch source at once, which can look like synchronization. Those two steps of the sequence should be re-run before they are used. Consistent budget data start in 1980 or later for most economies, which limits that test.
\\item A check of Paper~1's input: Maddison's per-capita growth for Norway, Switzerland and South Africa runs about 2–3 points a year above national-accounts growth for 1991–2011, probably a side-effect of how Maddison links its benchmark years. The band-pass filter removes most of a steady drift, but the kinks at 1991 and 2011 can leak into the cycle. A robustness run with these series is worth doing.
\\end{{itemize}}
\\subsection{{Limits}}
Annual data cannot date turning points within a year. Some series start late (short rates for South Korea, Mexico and Thailand in the late 1970s and Turkey in 1987; long rates for several emerging economies only from the 1990s or 2000s), and broad money ends early for Austria (1997), Greece (2000) and Thailand (2019). The country context lines record well-known episodes and are not derived from the data.
\\end{{multicols}}
"""

exec(open('build_extra.py').read())          # context, notes and section for the economies added in the second edition
body=pre+cover()+howto+defs+g_text+m_text+ov_text+sum_text
for k,(iso,name,reg) in enumerate(ORDER,1): body+=country_page(k,iso)
body+=extra_text
for k,(iso,name,reg) in enumerate(EXTRA,1): body+=country_page(k,iso,total=len(EXTRA),kicker='ADDED ECONOMY',figw='0.95')
body+=data_text+"\n\\end{document}\n"
open('atlas.tex','w').write(body)
print('wrote atlas.tex', len(body))
