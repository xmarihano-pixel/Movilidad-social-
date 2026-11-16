import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, ""+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"")
import numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from src.evaluation import interpret as I
from src.models import train as T
df = pd.read_parquet(""+str(__import__("pathlib").Path(__file__).resolve().parents[3])+"/data/processed/emovi_movilidad.parquet")
q1 = df[df.sigue_q1.notna()].copy()
w_or,_ = I.logit_explicativo(q1)
# sin pesos
d=q1.dropna(subset=["hermanos"]).copy()
for c in ["educ_madre","educ_padre"]: d[c]=d[c].replace({"Secundaria":"Secundaria o más","Preparatoria":"Secundaria o más","Profesional":"Secundaria o más"})
f=("sigue_q1 ~ indice_origen + C(educ_madre, Treatment('Primaria o menos')) + C(educ_padre, Treatment('Primaria o menos')) + C(localidad_14, Treatment('Metrópoli'))"
   " + C(region_14, Treatment('Centro')) + C(tono_piel, Treatment('Medio (F-G)')) + mujer + lengua_indigena + hermanos + C(cohorte)")
mod=smf.glm(f,data=d,family=sm.families.Binomial()); d=d.loc[mod.data.row_labels]
m=smf.glm(f,data=d,family=sm.families.Binomial()).fit(cov_type="cluster",cov_kwds={"groups":pd.factorize(d.upm)[0]})
# sandwich manual para la logit ponderada (pseudo-verosimilitud) para verificar errores estándar
from scipy.special import expit
dw=d.copy(); dw["w"]=dw.factor/dw.factor.mean()
mw=smf.glm(f,data=dw,family=sm.families.Binomial(),var_weights=dw["w"]).fit()
Xw=mw.model.exog; pw=expit(Xw@mw.params.values); ww=dw.w.values; y=dw.sigue_q1.values
B=(Xw*(ww*pw*(1-pw))[:,None]).T@Xw; U=Xw*(ww*(y-pw))[:,None]
g=pd.factorize(dw.upm)[0]; G=g.max()+1; Ug=np.zeros((G,Xw.shape[1])); np.add.at(Ug,g,U)
n=len(y); k=Xw.shape[1]; c=G/(G-1)*(n-1)/(n-k)
V=np.linalg.inv(B)@(c*Ug.T@Ug)@np.linalg.inv(B); se_man=np.sqrt(np.diag(V))
mw2=smf.glm(f,data=dw,family=sm.families.Binomial(),var_weights=dw["w"]).fit(cov_type="cluster",cov_kwds={"groups":g})
print("EE: statsmodels(var_weights+cluster) vs sandwich manual — razón máx/mín:", np.round((mw2.bse.values/se_man).max(),3), np.round((mw2.bse.values/se_man).min(),3))
print(pd.DataFrame({"EE statsmodels":mw2.bse.round(3),"EE manual":np.round(se_man,3)}).head(25).to_string())
uw=np.exp(m.params).drop("Intercept").round(2).values
cmp=pd.DataFrame({"RM ponderada":w_or["Razón de momios"].values,"p pond":w_or["p-valor"].values,"RM sin pesos":uw,"p sin pesos":m.pvalues.drop("Intercept").round(3).values},index=w_or.index)
print(cmp.to_string())
X=pd.DataFrame(m.model.exog,columns=m.model.exog_names).drop(columns="Intercept")
vif=pd.Series([variance_inflation_factor(X.values,i) for i in range(X.shape[1])],index=X.columns).round(1)
print("VIF máx:", vif.max(), vif.idxmax())
print("Metrópoli como referencia: n en Q1 =", (q1.localidad_14=="Metrópoli").sum())
# test set composition vs full
tr,te=T.split(df)
print("tasa real tono oscuro: prueba", round(te[te.tono_piel=='Oscuro (A-E)'].sigue_q1.mean(),3), "| entrenamiento", round(tr[tr.tono_piel=='Oscuro (A-E)'].sigue_q1.mean(),3))
# estado: n por entidad_14 en Q1 y ESS
k=lambda x:x.sum()**2/(x**2).sum()
st=q1.groupby("entidad_14").factor.agg(['size',k]).rename(columns={'size':'n','<lambda_0>':'ESS'}).sort_values('n')
print("estados con n>=40:", (st.n>=40).sum(), "| ESS mediana de esos:", round(st[st.n>=40].ESS.median()), "| CDMX:", st.loc['Ciudad de México'].round(0).to_dict())
# escenarios: proporción de personas ya en Profesional (no cambian con +1 nivel)
print("Q1 con educ Profesional:", (q1.educ=="Profesional").sum(), "| no ocupados (no cambian en escenario empleo):", (q1.empleo=="No ocupado").sum())
print("ingreso imputado? ingc_pc descripción: 'Ingreso per cápita del hogar - imputado'")
