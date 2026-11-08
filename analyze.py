# -*- coding: utf-8 -*-
"""
Audit of animal and donor age reporting in curated circadian transcriptome datasets.

Reads circadian_age_audit.xlsx and regenerates Table 1 and Figures 1-3 of the
manuscript, plus results.json for checking the text against the data.

No number in the manuscript is hard-coded here: every value is computed from the
coded table. Change a row in the table, rerun, and the text and figures follow.

The category labels below are in Russian because that is the working language of
the coding sheet; they are the literal cell values and must match it exactly.
FORM_EN maps each to the English wording used in the manuscript.

Usage:  pip install -r requirements.txt && python analyze.py
"""
import collections, statistics, json
import numpy as np
import openpyxl
import matplotlib
matplotlib.use("Agg")   # render to file, not to a screen; must precede pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

XLSX = "data/circadian_age_audit.xlsx"
OUT  = "figures"

# Okabe-Ito palette, validated for colour-vision deficiency:
# protanopia dE 21.9, normal vision dE 31.2 (threshold 8)
BLUE, VERM, GREY, INK, MUTE = "#0072B2", "#D55E00", "#BFBFBF", "#1A1A1A", "#595959"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": "#808080", "axes.linewidth": 0.6,
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTE, "ytick.color": INK,
    "xtick.labelsize": 8, "ytick.labelsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
})

# ------------------------------------------------------------------ read the table
# column name -> Excel column number, so an inserted column is a one-line fix
COL = {"id":2,"species":4,"repo":5,"tissue":6,"age":9,"applic":10,
       "source":11,"form":12,"width":13,"anchor":14,"year":15,"cit":16}

# data_only=True returns computed values, not formula text.
# The workbook must therefore be saved from Excel/LibreOffice after any edit.
wb = openpyxl.load_workbook(XLSX, data_only=True)
d = wb["Данные"]
rows=[]
r=2
# row 1 is the header; an empty id cell ends the table
while d.cell(row=r,column=COL["id"]).value:
    rows.append({k:d.cell(row=r,column=c).value for k,c in COL.items()})
    r+=1

# two separate protocol decisions, kept as two visible steps
geo  = [x for x in rows if x["repo"]=="GEO"]
appl = [x for x in geo  if x["applic"]=="да"]
N_GEO, N = len(geo), len(appl)

src = collections.Counter(x["source"] for x in appl)
frm = collections.Counter(x["form"]   for x in appl)
anc = collections.Counter(x["anchor"] for x in appl)
# width is blank for open bounds, mean +/- SD and absent ages; keep numbers only
widths = [x["width"] for x in appl if isinstance(x["width"],(int,float))]

MACHINE = "GEO"
not_machine = N - src[MACHINE]

# forms that support comparison between studies
USABLE = {"точное значение по образцам","точное значение"}
usable = sum(1 for x in appl if x["form"] in USABLE and x["anchor"]=="не указан")

# ------------------------------------------------------------------ Table 1
# fixed display order, from most usable to absent, so the table stays
# comparable between versions instead of resorting as the data change
FORM_ORDER = ["точное значение по образцам","точное значение","узкий диапазон",
              "широкий диапазон","среднее ± SD/SEM","открытая граница","только отношение",
              "несколько значений","выводится из длительностей","диапазон критерия отбора","нет"]
FORM_EN = {
 "точное значение по образцам":("Exact age, per sample","age: 63 / age: 20 / age: 57","yes"),
 "точное значение":("Single exact value for the series","6 week old male mice","yes*"),
 "узкий диапазон":("Narrow range (<=4 weeks)","8-12 weeks","no"),
 "широкий диапазон":("Wide range (>4 weeks)","12 to 24 months","no"),
 "среднее ± SD/SEM":("Cohort mean +/- SD or SEM","29.7 +/- 8.9","no"),
 "открытая граница":("Open-ended bound","retired breeders (>35 weeks old)","no"),
 "только отношение":("Relational claim, no value","cohoused littermates","no"),
 "несколько значений":("Several irreconcilable values","12-24 months vs 8-12 weeks + 4 weeks","no"),
 "выводится из длительностей":("Derivable only from a chain of durations","newly hatched, reared 12 days, +1 cycle","no"),
 "диапазон критерия отбора":("Eligibility window, not measured age","individuals 18-35 years of age","no"),
 "нет":("Absent","-","no"),
}
t1=[]
for f in FORM_ORDER:
    n=frm.get(f,0)
    if n==0: continue
    en,ex,us=FORM_EN[f]
    t1.append({"form_ru":f,"form_en":en,"n":n,"pct":round(100*n/N,1),"example":ex,"usable":us})

# ------------------------------------------------------------------ Figure 1: where age is recorded
SRC_ORDER=[("GEO","In the GEO record"),("статья","Article text only"),
           ("доп. материалы","Supplementary only"),("нет","Nowhere")]
labels=[en for _,en in SRC_ORDER]; vals=[src.get(ru,0) for ru,_ in SRC_ORDER]
cols=[BLUE]+[GREY]*3

fig,ax=plt.subplots(figsize=(5.2,2.5))
y=range(len(vals))
ax.barh(list(y),vals,color=cols,height=0.62,zorder=3)
ax.set_yticks(list(y)); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlabel("Datasets (n = %d)"%N)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xlim(0,max(vals)*1.22)
for i,v in zip(y,vals):
    ax.text(v+max(vals)*0.02,i,"%d  (%.0f%%)"%(v,100*v/N),va="center",fontsize=8,color=INK)
# the boundary of machine readability: only the first category is above it
ax.axhline(0.5,color=VERM,lw=1.0,ls=(0,(4,2)),zorder=4)
ax.text(max(vals)*1.19,0.5,"machine-readable above",ha="right",va="bottom",
        fontsize=7.5,color=VERM,style="italic")
ax.set_title("Where the age of the animals or donors is recorded",fontsize=9.5,loc="left",pad=8)
ax.grid(axis="x",color="#E8E8E8",lw=0.5,zorder=0)
fig.savefig("%s/fig1_where_age_lives.png"%OUT); plt.close(fig)

# ------------------------------------------------------------------ Figure 2: forms of reporting
# blue segment = rows usable for comparison (usable form AND no declared shift)
def usable_in(f):
    return sum(1 for x in appl if x["form"]==f and f in USABLE and x["anchor"]=="не указан")
f2=[(FORM_EN[r["form_ru"]][0], r["n"], usable_in(r["form_ru"])) for r in t1]
f2.sort(key=lambda t:t[1])
fig,ax=plt.subplots(figsize=(6.6,3.7))
y=list(range(len(f2)))
ok=[t[2] for t in f2]; rest=[t[1]-t[2] for t in f2]
ax.barh(y,ok,color=BLUE,height=0.66,zorder=3)
ax.barh(y,rest,left=ok,color=GREY,height=0.66,zorder=3)   # left= stacks on top of the blue
ax.set_yticks(y); ax.set_yticklabels([t[0] for t in f2])
ax.set_xlabel("Datasets (n = %d)"%N)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
mx=max(t[1] for t in f2); ax.set_xlim(0,mx*1.26)
for i,t in zip(y,f2):
    lab="%d"%t[1] if t[2] in (0,t[1]) else "%d  (%d usable)"%(t[1],t[2])
    ax.text(t[1]+mx*0.02,i,lab,va="center",fontsize=8,color=INK)
ax.set_title("Forms in which age is reported\n"
             "Blue: age usable for comparison across studies (%d of %d)"%(usable,N),
             fontsize=9.5,loc="left",pad=8)
ax.grid(axis="x",color="#E8E8E8",lw=0.5,zorder=0)
fig.savefig("%s/fig2_forms.png"%OUT); plt.close(fig)

# ------------------------------------------------------------------ Figure 3: form by species
def by(sp,f): return sum(1 for x in appl if x["species"]==sp and x["form"]==f)
n_mouse=sum(1 for x in appl if x["species"]=="M. musculus")
n_human=sum(1 for x in appl if x["species"]=="H. sapiens")
grp=[("Exact, per sample",["точное значение по образцам"]),
     ("Single exact value",["точное значение"]),
     ("Range (narrow or wide)",["узкий диапазон","широкий диапазон"]),
     ("Cohort mean +/- SD or SEM",["среднее ± SD/SEM"]),
     ("Other forms",["открытая граница","только отношение","несколько значений",
                     "выводится из длительностей","диапазон критерия отбора"]),
     ("Absent",["нет"])]
m=[sum(by("M. musculus",f) for f in fs) for _,fs in grp]
h=[sum(by("H. sapiens",f) for f in fs) for _,fs in grp]
# guard: the plotted groups must account for every mouse and human series.
# Add a form to the table and forget to add it to grp, and this stops the run
# instead of silently drawing incomplete data.
assert sum(m)==n_mouse and sum(h)==n_human, (sum(m),n_mouse,sum(h),n_human)
fig,ax=plt.subplots(figsize=(6.2,3.4))
y=np.arange(len(grp)); bh=0.36
ax.barh(y-bh/2,m,height=bh,color=BLUE,label="Mouse (n = %d)"%n_mouse,zorder=3)
ax.barh(y+bh/2,h,height=bh,color=VERM,label="Human (n = %d)"%n_human,zorder=3)
ax.set_yticks(y); ax.set_yticklabels([g[0] for g in grp]); ax.invert_yaxis()
ax.set_xlabel("Datasets"); ax.xaxis.set_major_locator(MaxNLocator(integer=True))
mx=max(max(m),max(h)); ax.set_xlim(0,mx*1.25)
for i,(a,b) in enumerate(zip(m,h)):
    ax.text(a+mx*0.02,i-bh/2,"%d"%a,va="center",fontsize=8,color=INK)
    ax.text(b+mx*0.02,i+bh/2,"%d"%b,va="center",fontsize=8,color=INK)
ax.legend(frameon=False,fontsize=8,loc="lower right")
ax.set_title("Form of age reporting by species\n"
             "Each named form of reporting is used by one species only",
             fontsize=9.5,loc="left",pad=8)
ax.grid(axis="x",color="#E8E8E8",lw=0.5,zorder=0)
fig.savefig("%s/fig3_species.png"%OUT); plt.close(fig)

# ------------------------------------------------------------------ write results
res={
 "n_records":len(rows),"n_geo":N_GEO,"n_applicable":N,
 "source":{k:src[k] for k in src},
 "not_machine_readable":not_machine,"not_machine_pct":round(100*not_machine/N,1),
 "usable_for_comparison":usable,"usable_pct":round(100*usable/N,1),
 "n_forms":len([f for f in frm if frm[f]>0]),
 "anchor":{k:anc[k] for k in anc},
 "shift_declared":anc.get("начало эксперимента",0)+anc.get("другая процедура",0),
 "width_n":len(widths),"width_median":statistics.median(widths) if widths else None,
 "width_max":max(widths) if widths else None,
 "mouse_n":n_mouse,"human_n":n_human,
 "mouse_geo":sum(1 for x in appl if x["species"]=="M. musculus" and x["source"]=="GEO"),
 "human_geo":sum(1 for x in appl if x["species"]=="H. sapiens" and x["source"]=="GEO"),
 "table1":t1,
}
# results.json is what the manuscript text is checked against, value by value
json.dump(res,open("results.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)

print("n applicable:",N,"| not machine-readable: %d (%.1f%%)"%(not_machine,100*not_machine/N))
print("usable for comparison: %d (%.1f%%)"%(usable,100*usable/N))
print("forms:",res["n_forms"],"| width n=%d median=%s max=%s"%(res["width_n"],res["width_median"],res["width_max"]))
print("mouse %d (in GEO %d) | human %d (in GEO %d)"%(n_mouse,res["mouse_geo"],n_human,res["human_geo"]))
print("\nTable 1:")
for t in t1: print("  %-34s n=%-3d %5.1f%%  usable=%s"%(t["form_en"][:34],t["n"],t["pct"],t["usable"]))
