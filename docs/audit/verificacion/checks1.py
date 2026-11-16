import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, ""+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"")
import numpy as np, pandas as pd
df = pd.read_parquet(""+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"/data/processed/emovi_movilidad.parquet")
w = df.factor
print("N", len(df), "cols", df.shape[1])
# 1. Empates en el índice y en el corte de Q1
for c in ["indice_origen","indice_destino"]:
    vc = df[c].round(8).value_counts()
    print(c, "valores únicos", df[c].round(8).nunique(), "| mayor grupo de empates", vc.iloc[0], "| filas en grupos empatados", (vc[vc>1]).sum())
for c,q in [("indice_origen","q_origen"),("indice_destino","q_destino")]:
    amb = 0
    for coh,g in df.groupby("cohorte"):
        v = g[c].round(8)
        cut = v[g[q]==1].max()
        tied = g[(v==cut)]
        amb += (tied[q].nunique()>1) * len(tied)
        print(f"  {q} {coh}: valor de corte Q1 empatado en {len(tied)} filas, quintiles en el empate: {sorted(tied[q].unique())}")
# 2. Tamaño efectivo de muestra (Kish)
def kish(x): return x.sum()**2/(x**2).sum()
q1 = df[df.sigue_q1.notna()]
print("Kish ESS total", round(kish(w)), "| Q1", round(kish(q1.factor)), "de", len(q1))
for c in ["region_14","tono_piel","lengua_indigena"]:
    print(c, {k: (len(g), round(kish(g.factor))) for k,g in q1.groupby(c)})
print("factor máx/mediana", round(w.max()/w.median(),1), "| top 1% de filas concentra", round(w.nlargest(int(len(w)*.01)).sum()/w.sum()*100,1), "% del peso")
# 3. Bootstrap por conglomerado (UPM) de sigue_q1 vs bootstrap simple
rng = np.random.default_rng(42)
up = q1.upm.values; ids = pd.unique(up); grp = {u: np.where(up==u)[0] for u in ids}
x = q1.sigue_q1.values; ww = q1.factor.values
bs=[]
for _ in range(1000):
    s = np.concatenate([grp[u] for u in rng.choice(ids, len(ids))])
    bs.append(np.average(x[s], weights=ww[s])*100)
print("sigue_q1", round(np.average(x,weights=ww)*100,1), "IC95 cluster-UPM", np.percentile(bs,[2.5,97.5]).round(1), "UPM en Q1:", len(ids))
# 4. ¿Q1 de origen al 20% ponderado?
print("peso de Q1 origen", round(w[df.q_origen==1].sum()/w.sum()*100,1), "% | Q1 destino", round(w[df.q_destino==1].sum()/w.sum()*100,1))
print("n por quintil origen", df.q_origen.value_counts().sort_index().to_dict())
# 5. Validación escala de tono vs colorímetro
print(df.groupby("tono_piel").luminosidad_piel.mean().round(1).to_dict())
