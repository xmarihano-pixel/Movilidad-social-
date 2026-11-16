import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, ""+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"")
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.metrics import roc_auc_score
from src.models import train as T
from src.features.indices import wealth_index, weighted_quintile
df = pd.read_parquet(""+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"/data/processed/emovi_movilidad.parquet")
q1 = df[df.sigue_q1.notna()].copy(); q1["sigue_q1"]=q1.sigue_q1.astype(int)
rng = np.random.default_rng(42)

def cboot(d, col="sigue_q1", B=500):
    up=d.upm.values; ids=pd.unique(up); g={u:np.where(up==u)[0] for u in ids}
    x=d[col].values; w=d.factor.values; out=[]
    for _ in range(B):
        s=np.concatenate([g[u] for u in rng.choice(ids,len(ids))]); out.append(np.average(x[s],weights=w[s])*100)
    return round(np.average(x,weights=w)*100,1), np.percentile(out,[2.5,97.5]).round(1)

print("== IC 95% por conglomerado de cifras titulares")
q1["n_desv"]=(q1.region_14=="Sur").astype(int)+(q1.localidad_14=="Pueblo (<2,500)").astype(int)+q1.lengua_indigena
for name, m in {"Sur": q1.region_14=="Sur", "Norte": q1.region_14=="Norte", "Lengua sí": q1.lengua_indigena==1, "Lengua no": q1.lengua_indigena==0,
                "Educ primaria": q1.educ=="Primaria o menos", "Educ profesional": q1.educ=="Profesional",
                "0 desventajas": q1.n_desv==0, "3 desventajas": q1.n_desv==3, "Tono oscuro": q1.tono_piel=="Oscuro (A-E)", "Tono claro": q1.tono_piel=="Claro (H-K)",
                "Norte & oscuro": (q1.region_14=="Norte")&(q1.tono_piel=="Oscuro (A-E)"), "Norte & claro": (q1.region_14=="Norte")&(q1.tono_piel=="Claro (H-K)"),
                "N-occ & oscuro": (q1.region_14=="Norte-occidente")&(q1.tono_piel=="Oscuro (A-E)"), "N-occ & claro": (q1.region_14=="Norte-occidente")&(q1.tono_piel=="Claro (H-K)")}.items():
    d=q1[m]; print(f"  {name:18s} n={len(d):5d}", cboot(d))
d5=df[df.q_origen==5].assign(s5=(df.q_destino==5).astype(int)); print("  Q5->Q5", cboot(d5,"s5"))

print("== Sesgo por tono con predicciones fuera de muestra (CV 5, todas las 2,674 personas)")
cv=StratifiedKFold(5,shuffle=True,random_state=42)
m=T.candidates(T.NUM,T.CAT)["Regresión logística"]
p=cross_val_predict(m,q1[T.NUM+T.CAT],q1.sigue_q1,cv=cv,method="predict_proba")[:,1]
q1["p"]=p
for t,g in q1.groupby("tono_piel"):
    diffs=[]
    for _ in range(500):
        s=g.sample(len(g),replace=True,random_state=int(rng.integers(1e9))); diffs.append((s.sigue_q1.mean()-s.p.mean())*100)
    print(f"  {t}: n={len(g)} real={g.sigue_q1.mean()*100:.1f} pred={g.p.mean()*100:.1f} brecha={np.mean(diffs):.1f} IC95={np.percentile(diffs,[2.5,97.5]).round(1)}")
print("  AUC fuera de muestra global", round(roc_auc_score(q1.sigue_q1,p),3))

print("== ¿Autoadscripción / tono autopercibido introducen sesgo de medición actual?")
def auc(num,cat): return round(cross_val_score(T.candidates(num,cat)["Regresión logística"],q1[num+cat],q1.sigue_q1,cv=cv,scoring="roc_auc").mean(),3)
print("  modelo original", auc(T.NUM,T.CAT))
cat2=[c for c in T.CAT if c not in ("autoadscripcion",)]; print("  sin autoadscripción", auc(T.NUM,cat2))
cat3=[c for c in T.CAT if c not in ("autoadscripcion","tono_piel")]; print("  sin autoadscripción ni tono autopercibido + colorímetro", auc(T.NUM+["luminosidad_piel"],cat3))
print("  autoadscripción vs quintil destino (% indígena por q_destino):", df.groupby("q_destino").apply(lambda x: round((x.autoadscripcion=="Indígena").mean()*100,1)).to_dict())
print("  autoadscripción indígena vs habla lengua, en Q1:", pd.crosstab(q1.autoadscripcion, q1.lengua_indigena).loc[["Indígena","Mestiza","Ninguna"]].to_dict())

print("== Efecto de cohorte: índice de origen solo con bienes disponibles en todas las generaciones")
modern=["o_p31j","o_p31k","o_p31l","o_p31h","o_p31i","o_p31m","o_p32h","o_p32i","o_p32j"]
cols=[c for c in df.columns if c.startswith("o_p") and not c.startswith("o_p33") and c not in modern]+["piso_tierra_14","autos_14","cuartos_14"]
d=df.copy(); d["piso_tierra_14"]=-d.piso_tierra_14
idx,_=wealth_index(d,cols,d.factor); d["io2"]=idx
d["qo2"]=0
for _,g in d.groupby("cohorte"): d.loc[g.index,"qo2"]=weighted_quintile(g.io2,g.factor)
for coh,g in d.groupby("cohorte"):
    a=g[g.q_origen==1]; b=g[g.qo2==1]
    print(f"  {coh}: original {np.average(a.q_destino==1,weights=a.factor)*100:.1f}% | sin bienes modernos {np.average(b.q_destino==1,weights=b.factor)*100:.1f}%")
print("  % por cohorte que tenía a los 14: celular", d.groupby("cohorte").o_p31j.mean().round(2).to_dict(), "| internet", d.groupby("cohorte").o_p31l.mean().round(2).to_dict())
print("  cargas originales de bienes modernos:", pd.read_csv('"+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"/reports/tables/cargas_origen.csv',index_col=0).loc[modern].carga.to_dict())
