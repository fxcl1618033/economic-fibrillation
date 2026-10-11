# Executed inside build_tex.py (shared namespace): context lines, page notes and the section for the added economies.
CONTEXT.update({
'CHN':"The world's second-largest economy, transformed by reform and opening from 1978. Episodes: the end of the Cultural Revolution (the 1976 contraction); market reforms from 1978; the 1988–89 inflation and slowdown; the 1994 inflation peak; WTO entry in 2001; the 2008–09 stimulus; 2020.",
'BRA':"Latin America's largest economy. Episodes: the 1968–73 'miracle' boom; the 1980s debt crisis; hyperinflation and failed stabilization plans (Cruzado 1986, Collor 1990); the 1994 Real Plan; the 1999 devaluation and inflation targeting; the 2015–16 recession; 2020.",
'SAU':"The largest oil exporter; growth and budgets follow oil prices and output decisions. Episodes: the 1973–74 and 1979–80 oil booms; the 1980s glut, when output was cut sharply; the riyal's peg to the dollar from 1986; the 2014–16 oil-price fall; Vision 2030 reforms from 2016; the 2022 windfall.",
'ARE':"A federation formed in 1971, combining oil wealth (Abu Dhabi) with trade, aviation and finance (Dubai). Episodes: the 1970s oil boom; the 1980s oil glut; Dubai's rise as a re-export and services hub; the 2009 Dubai World debt crisis; the 2014–16 oil-price fall; 2020.",
'IRN':"A large oil exporter reshaped by revolution, war and sanctions. Episodes: the 1970s oil boom; the 1979 revolution and the 1980–88 war with Iraq; the 1993 exchange-rate unification and high inflation in the mid-1990s; sanctions from 2012, eased in 2016 and reimposed in 2018.",
})
THE['ARE']='the United Arab Emirates'
AG=FIX.get('CHN',{}).get('alt_growth',{})
PCT='\\%'
EXTRA_NOTES={
'CHN':(f"Official national accounts. The alternative estimates by Harry Wu, used by Penn World Table and Maddison, average {f(AG.get('pwt_mean_1978_2019'))}{PCT} growth in 1978–2019 against {f(AG.get('official_mean_1978_2019'))}{PCT} official, which also weakens the validation below." if AG else ''),
'BRA':f"Expenditure components before 1981 do not add up (consumption, investment and trade sum to as much as 141{PCT} of GDP) and are not used; the demand split starts in 1996 because annual averages cannot deflate hyperinflation-era flows reliably; debt ratios in 1985–94 are distorted by hyperinflation.",
'SAU':"GDP from 1970 (earlier levels are spliced estimates). The short rate is the central bank's policy rate, 1999–2022. The source has no crisis dating for Saudi Arabia.",
'ARE':"GDP from 1975 and inflation from 1980 (earlier values are estimates or a constant placeholder). The source has no interest-rate series and no crisis dating for the UAE.",
'IRN':"No market interest-rate series: rates are administered, and the central-bank rate in the source stops in 2003. The 1993 budget break coincides with exchange-rate unification.",
}

def span_txt(iso,col):
    s=P[(P.iso==iso)&(P.year>=1970)&P[col].notna()].year
    if not len(s): return r'\textcolor{muted}{none}'
    a,b=int(s.min()),int(s.max())
    return f"{a}–" if b>=2022 else f"{a}–{str(b)[2:]}"

def coverage_table():
    cols=[('growth','GDP growth'),('c_C','Demand split'),('govdef_GDP','Budget'),('govdebt_GDP','Debt'),('strate','Short rate'),
          ('infl','Inflation'),('real_money_growth','Money'),('CA_GDP','Current acc.'),('BankingCrisis','Crisis dates')]
    rows=[]
    for iso,name,reg in EXTRA:
        rows.append(r'\hyperref[c:'+iso+']{'+esc(name)+'} & '+' & '.join(span_txt(iso,c) for c,_ in cols)+r' \\')
    head=' & '.join(h for _,h in cols)
    return (r'{\sffamily\fontsize{7.3}{9.6}\selectfont\setlength{\tabcolsep}{3pt}'+'\n'
            +r'\begin{tabularx}{\textwidth}{@{}X'+'r'*len(cols)+'@{}}\n'+r'\toprule'+'\n'
            +'Years covered & '+head+r' \\'+'\n'+r'\midrule'+'\n'+'\n'.join(rows)+'\n'+r'\bottomrule'+'\n'+r'\end{tabularx}}\par'+'\n')

def extra_summary():
    rows=[]
    for iso,name,reg in EXTRA:
        s=S[iso]; ncov=sum(1 for y in GL if s['gr_global'][str(y)] is not None)
        cells=[r'\hyperref[c:'+iso+']{'+esc(name)+'}', f(s['growth_mean']), f(s['growth_sd']), f"{sg(s['worst'][0])} ({yy(s['worst'][1])})",
               f"{s['n_contract_global']}/{ncov}", sg(s['coup_7089'],2), sg(s['coup_9022'],2), share(s['anat']['I']), sg(s['bal_mean']),
               f"{f(s['debt_start'][0],0)}→{f(s['debt_2022'],0)}", f"{f(s['infl_peak'][0],0)} ({yy(s['infl_peak'][1])})",
               f"{f(s['open_1970'],0)}→{f(s['open_2022'],0)}", sg(s['ca_mean'])]
        rows.append(' & '.join(cells)+r' \\')
    return (r'{\sffamily\fontsize{7.1}{8.9}\selectfont\setlength{\tabcolsep}{3.2pt}'+'\n'
            +r'\begin{tabularx}{\textwidth}{@{}Xrrrcrrrrrrrr@{}}'+'\n'+r'\toprule'+'\n'
            +r' & \multicolumn{2}{c}{Growth, \%} & Worst & Global & \multicolumn{2}{c}{Coupling with the 26} & Var. & Budget & Debt, \% & Inflation & Trade, \% & Current \\'+'\n'
            +r'\cmidrule(lr){2-3}\cmidrule(lr){6-7}'+'\n'
            +r'Economy & mean & s.d. & year & recessions & ’70–89 & ’90–22 & share I & balance & first→’22 & peak & first→’22 & account \\'+'\n'
            +r'\midrule'+'\n'+'\n'.join(rows)+'\n'+r'\bottomrule'+'\n'+r'\end{tabularx}}\par'+'\n')

_t=r"""
\clearpage
\section{Five more economies}\label{p:extra}
\begin{multicols}{2}\fontsize{8.8}{11.2}\selectfont
Paper~1 works with 26 economies. This section adds the two largest economies outside that sample, China and Brazil, and three from the Middle East, Saudi Arabia, the United Arab Emirates and Iran, so that the region is represented. They go through the same pipeline and the same repairs as the 26 and get the same page. They are compared with the 26 rather than added to them: none of the averages, global pages, tests or headline tables earlier in the atlas include them, and their \emph{In step with the world?} panel shows the average cycle of all 26.

\textbf{Is the data good enough?} Yes for China, Brazil and Saudi Arabia, with the caveats on the right, and mostly for the UAE and Iran. Iran clears the bar on everything except interest rates, which it administers rather than leaving to a market.

\textbf{For Paper 1.} Maddison, Paper~1's GDP source, has annual GDP per head from 1950 for all five; only the UAE lacks 1991–92. Its Gulf series before the 1970s are rough reconstructions, and its China series follows the lower alternative estimates.

\columnbreak
\begin{itemize}
\item \textbf{China.} Growth here is the official series, @@OFF@@\% a year in 1978–2019. Harry Wu's alternative estimates, which Penn World Table and Maddison use, give @@ALT@@\%, and @@ALT98@@\% in 1998 against an official @@OFF98@@\%.
\item \textbf{Brazil.} Inflation peaked at 2,948\% in 1990 and fell only after the 1994 Real Plan. Expenditure data before 1981 do not add up and are left out; the demand split starts in 1996 and budget figures in 2001.
\item \textbf{Saudi Arabia.} Oil drives output and the GDP deflator. GDP starts in 1970; the short rate is the central bank's policy rate from 1999 (the riyal has been pegged to the dollar since 1986); money ends in 2017.
\item \textbf{United Arab Emirates.} GDP starts in 1975 and inflation in 1980. There is no interest-rate series (the dirham is pegged to the dollar), and money ends in 2015.
\item \textbf{Iran.} No market interest rate: rates are administered under the 1983 interest-free banking law, and the central bank's rate in the source stops in 2003. Money ends in 2016.
\end{itemize}
Neither Saudi Arabia nor the UAE has crisis dates in the source.
\end{multicols}
\vspace{2pt}
@@COVERAGE@@
\vspace{8pt}
\noindent\includegraphics[width=\textwidth]{fig/overview_extra.png}\par
\vspace{8pt}
@@SUMMARY@@
\vspace{3pt}
{\fontsize{7.6}{9.4}\selectfont\color{ink2} Coupling is the correlation of each economy's cycle with the average cycle of the 26 (n/a: fewer than eight years of data). Global recessions counts contractions among the recession years each economy's data cover. Debt and trade start in the first year available.\par}
"""
extra_text=(_t.replace('@@OFF@@',f(AG.get('official_mean_1978_2019'))).replace('@@ALT@@',f(AG.get('pwt_mean_1978_2019')))
              .replace('@@ALT98@@',f(AG.get('pwt_1998'))).replace('@@OFF98@@',f(AG.get('official_1998')))
              .replace('@@COVERAGE@@',coverage_table()).replace('@@SUMMARY@@',extra_summary()))
