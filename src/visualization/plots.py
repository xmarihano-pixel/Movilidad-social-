"""Figuras del proyecto. Paleta y estilo comunes para que el reporte y el cartel se vean iguales."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.config import FIGURES

AZUL, NARANJA, GRIS, ROJO, VERDE = "#1f4e79", "#e07b39", "#8c8c8c", "#b2312b", "#3a7d44"
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 200, "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 11, "axes.titleweight": "bold"})


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(FIGURES / f"{name}.png", bbox_inches="tight")
    return fig


def wavg(d, col, w="factor"):
    return np.average(d[col], weights=d[w])


def matriz_transicion(df):
    tm = pd.crosstab(df.q_origen, df.q_destino, values=df.factor, aggfunc="sum", normalize="index") * 100
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    sns.heatmap(tm, annot=True, fmt=".0f", cmap="Blues", cbar_kws={"label": "% de personas"}, ax=ax,
                linewidths=.5, vmin=0, vmax=60)
    ax.set_xlabel("Quintil de riqueza HOY (adulto)")
    ax.set_ylabel("Quintil de riqueza A LOS 14 AÑOS")
    ax.set_title("¿Dónde terminan las personas según dónde empezaron?")
    return _save(fig, "01_matriz_transicion"), tm.round(1)


def barras_grupo(df, col, titulo, nombre, orden=None):
    d = df[df.sigue_q1.notna()]
    g = d.groupby(col).apply(lambda x: pd.Series({"pct": wavg(x, "sigue_q1") * 100, "n": len(x)}))
    g = g[g.n >= 30]
    if orden:
        g = g.reindex([o for o in orden if o in g.index])
    fig, ax = plt.subplots(figsize=(7, 0.55 * len(g) + 1.4))
    cols = [ROJO if v >= 55 else NARANJA if v >= 45 else AZUL for v in g.pct]
    ax.barh(g.index.astype(str), g.pct, color=cols)
    for i, (v, n) in enumerate(zip(g.pct, g.n)):
        ax.text(v + 1, i, f"{v:.0f}%  (n={int(n)})", va="center", fontsize=9)
    ax.axvline(wavg(d, "sigue_q1") * 100, color=GRIS, ls="--", lw=1)
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.set_xlabel("% que sigue en el 20% más pobre de adulto")
    ax.set_title(titulo)
    return _save(fig, nombre), g.round(1)


def comparacion_modelos(tab):
    t = tab.set_index("Modelo")
    fig, ax = plt.subplots(figsize=(7.5, 4))
    y = np.arange(len(t))
    ax.barh(y, t["AUC CV (media)"], xerr=t["AUC CV (desv.)"], color=[GRIS, GRIS, AZUL, NARANJA, NARANJA, NARANJA])
    ax.scatter(t["AUC prueba"], y, color="black", zorder=3, label="Conjunto de prueba")
    ax.set_yticks(y, t.index)
    ax.invert_yaxis()
    ax.set_xlim(0.45, 0.8)
    ax.axvline(0.5, color=GRIS, lw=1, ls=":")
    ax.set_xlabel("AUC (0.5 = azar, 1 = perfecto)")
    ax.set_title("Comparación de modelos: ¿quién sigue en el 20% más pobre?")
    ax.legend(loc="lower right")
    return _save(fig, "05_comparacion_modelos")


def razones_momios(or_):
    o = or_.copy()
    o = o[~o.index.str.startswith("cohorte")]
    o = o.sort_values("Razón de momios")
    fig, ax = plt.subplots(figsize=(7.5, 0.38 * len(o) + 1.2))
    sig = o["p-valor"] < 0.05
    ax.errorbar(o["Razón de momios"], range(len(o)),
                xerr=[o["Razón de momios"] - o["IC 95% inf"], o["IC 95% sup"] - o["Razón de momios"]],
                fmt="none", ecolor=GRIS, lw=1)
    ax.scatter(o["Razón de momios"], range(len(o)), c=np.where(sig, np.where(o["Razón de momios"] > 1, ROJO, AZUL), GRIS), zorder=3)
    ax.axvline(1, color="black", lw=1)
    ax.set_xscale("log")
    ax.set_yticks(range(len(o)), o.index)
    ax.set_xlabel("Razón de momios de seguir en Q1 (escala log; >1 = más pegajosa)")
    ax.set_title("Regresión logística: circunstancias asociadas")
    return _save(fig, "06_razones_momios")


def importancia(imp, top=12):
    i = imp.head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7, 0.4 * top + 1))
    ax.barh(i.Variable, i["Pérdida de AUC"], xerr=i["desv."], color=AZUL)
    ax.set_xlabel("Pérdida de AUC al revolver la variable")
    ax.set_title("Importancia por permutación (modelo elegido)")
    return _save(fig, "07_importancia")


def escenarios(esc):
    e = esc[esc.Escenario != "Situación observada"]
    fig, ax = plt.subplots(figsize=(7.5, 0.6 * len(e) + 1.2))
    ax.barh(e.Escenario, e["Cambio (puntos %)"], color=[AZUL if v < 0 else ROJO for v in e["Cambio (puntos %)"]])
    for i, v in enumerate(e["Cambio (puntos %)"]):
        ax.text(v + (0.5 if v >= 0 else -0.5), i, f"{v:+.1f}", va="center", ha="left" if v >= 0 else "right")
    ax.axvline(0, color="black", lw=1)
    ax.invert_yaxis()
    ax.set_xlabel("Cambio en la probabilidad de seguir en Q1 (puntos porcentuales)")
    ax.set_title("Escenarios hipotéticos (asociación, no causalidad)")
    return _save(fig, "08_escenarios")


def contexto_estatal(df, ctx):
    d = df[df.sigue_q1.notna()].groupby("entidad_14_cve").apply(
        lambda x: pd.Series({"pct": wavg(x, "sigue_q1") * 100, "n": len(x)}))
    d = d[d.n >= 40].join(ctx, how="inner")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(d.pobreza_pct, d.pct, s=d.n / 2, color=AZUL, alpha=.7)
    for _, r in d.iterrows():
        ax.annotate(r.entidad, (r.pobreza_pct, r.pct), fontsize=8, xytext=(3, 3), textcoords="offset points")
    r = np.corrcoef(d.pobreza_pct, d.pct)[0, 1]
    ax.set_xlabel("Pobreza en el estado, 2022 (% CONEVAL)")
    ax.set_ylabel("% que sigue en el 20% más pobre (EMOVI)")
    ax.set_title(f"Estados más pobres, pobreza más pegajosa (r = {r:.2f})")
    return _save(fig, "09_contexto_estatal"), d.round(1), r
