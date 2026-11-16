"""Figuras del cartel (90 × 120 cm). Se generan SOLO a partir de las tablas validadas en
`reports/tables/` (tras la auditoría), para que cada cifra sea rastreable.

Uso:  python reports/final/cartel/figuras_cartel.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
TAB = ROOT / "reports" / "tables"
OUT = Path(__file__).resolve().parent / "fig"
OUT.mkdir(exist_ok=True)

AZUL, AZUL2, NARANJA, ROJO, GRIS = "#15558f", "#5b8fc7", "#e07b39", "#b2312b", "#8a8a8a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15, "axes.titlesize": 17,
                     "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 300, "savefig.bbox": "tight"})


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", transparent=False, facecolor="white")
    plt.close(fig)


def matriz():
    m = pd.read_csv(TAB / "matriz_transicion.csv", index_col=0)
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    im = ax.imshow(m.values, cmap="Blues", vmin=0, vmax=60)
    for i in range(5):
        for j in range(5):
            v = m.values[i, j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=19, fontweight="bold",
                    color="white" if v > 35 else "#1b1b1b")
    lab = ["Q1\n(menos)", "Q2", "Q3", "Q4", "Q5\n(más)"]
    ax.set_xticks(range(5), lab); ax.set_yticks(range(5), lab)
    ax.set_xlabel("Posición HOY (adulto)", fontweight="bold")
    ax.set_ylabel("Posición A LOS 14 AÑOS", fontweight="bold")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, fill=False, ec=ROJO, lw=4))
    ax.add_patch(plt.Rectangle((3.5, 3.5), 1, 1, fill=False, ec=ROJO, lw=4))
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03); cb.set_label("% de cada fila")
    save(fig, "f1_matriz")


def grupos():
    g = pd.read_csv(TAB / "sigue_q1_por_grupo.csv")
    sel = [("region", "Sur", "Creció en el Sur"), ("region", "Centro", "Centro"), ("region", "Centro-norte", "Centro-norte"),
           ("region", "Norte-occidente", "Norte-occidente"), ("region", "Norte", "Norte"),
           ("lengua", "Habla lengua indígena", "Habla lengua indígena"), ("lengua", "No habla lengua indígena", "No habla"),
           ("localidad", "Pueblo (<2,500)", "Pueblo (<2,500 hab.)"), ("localidad", "Ciudad chica", "Ciudad chica"),
           ("tono", "Oscuro (A-E)", "Tono de piel oscuro"), ("tono", "Claro (H-K)", "Tono claro"),
           ("educ", "Primaria o menos", "Primaria o menos*"), ("educ", "Profesional", "Profesional*")]
    bloques = {"region": "Región donde creció", "lengua": "Lengua", "localidad": "Localidad a los 14",
               "tono": "Tono de piel (autopercibido)", "educ": "Escolaridad propia*"}
    rows = [g[(g.dimension == d) & (g.Grupo == k)].iloc[0].to_dict() | {"lab": l, "dim": d} for d, k, l in sel]
    d = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(7.0, 8.4))
    y, ys, prev, ticks = 0, [], None, []
    for _, r in d.iterrows():
        if r.dim != prev:
            if prev is not None:
                y += 0.7
            ax.text(-1, y, bloques[r.dim], fontweight="bold", fontsize=14, color=AZUL, va="center")
            y += 1; prev = r.dim
        c = ROJO if r["%"] >= 55 else NARANJA if r["%"] >= 45 else AZUL2
        ax.plot([r["IC 95% inf"], r["IC 95% sup"]], [y, y], color=c, lw=4, solid_capstyle="round")
        ax.plot(r["%"], y, "o", color=c, ms=13, mec="white", mew=1.5)
        ax.text(r["IC 95% sup"] + 1.5, y, f"{r['%']:.0f}%", va="center", fontsize=13, fontweight="bold")
        ys.append(y); ticks.append(r.lab); y += 1
    ax.axvline(51.1, color=GRIS, ls="--", lw=1.5)
    ax.text(51.6, -0.6, "Nacional 51%", color=GRIS, fontsize=12)
    ax.set_yticks(ys, ticks); ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_ylim(y, -1.4)
    ax.set_xlabel("% que sigue en el 20% con menos bienes\n(punto = estimación; línea = IC 95%)")
    ax.tick_params(axis="y", length=0)
    save(fig, "f2_grupos")


def desventajas():
    h = pd.read_csv(TAB / "h005_desventajas_acumuladas.csv")
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    cols = [AZUL2, NARANJA, "#c9562c", ROJO]
    ax.bar(h.Grupo.astype(str), h["% sigue Q1"], color=cols,
           yerr=[h["% sigue Q1"] - h["IC 95% inf"], h["IC 95% sup"] - h["% sigue Q1"]], capsize=6, ecolor="#333")
    for i, r in h.iterrows():
        ax.text(i, r["IC 95% sup"] + 3, f"{r['% sigue Q1']:.0f}%", ha="center", fontsize=19, fontweight="bold")
        ax.text(i, 4, f"n={int(r.n)}", ha="center", color="white", fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Nº de desventajas de origen\n(Sur · pueblo · lengua indígena)")
    ax.set_ylabel("% que sigue en Q1 (IC 95%)")
    save(fig, "f3_desventajas")


def momios():
    o = pd.read_csv(TAB / "razones_momios.csv", index_col=0)
    keep = {"region_14 = Sur": "Creció en el Sur (vs Centro)", "lengua_indigena": "Habla lengua indígena",
            "localidad_14 = Pueblo (<2,500)": "Creció en pueblo (vs ciudad)", "educ_padre = No sabe / ausente": "Padre ausente / sin dato",
            "mujer": "Mujer", "tono_piel = Oscuro (A-E)": "Tono oscuro (vs medio)",
            "indice_origen": "Más bienes a los 14 (+1 pto. índice)", "region_14 = Norte": "Creció en el Norte (vs Centro)"}
    d = o.loc[list(keep)].rename(index=keep).sort_values("Razón de momios")
    fig, ax = plt.subplots(figsize=(7.0, 5.6))
    y = np.arange(len(d))
    sig = d["p-valor"] < 0.05
    col = np.where(~sig, GRIS, np.where(d["Razón de momios"] > 1, ROJO, AZUL))
    ax.hlines(y, d["IC 95% inf"], d["IC 95% sup"], color=col, lw=4)
    ax.scatter(d["Razón de momios"], y, color=col, s=170, zorder=3, ec="white")
    for yy, (_, r) in zip(y, d.iterrows()):
        ax.text(r["IC 95% sup"] * 1.06, yy, f"{r['Razón de momios']:.2f}", va="center", fontsize=13, fontweight="bold")
    ax.axvline(1, color="black", lw=1.2)
    from matplotlib.ticker import NullFormatter, NullLocator
    ax.set_xscale("log"); ax.set_xlim(0.15, 4.5)
    ax.set_xticks([0.25, 0.5, 1, 2, 4], ["0.25", "0.5", "1", "2", "4"])
    ax.xaxis.set_minor_locator(NullLocator()); ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_yticks(y, d.index)
    ax.set_xlabel("Razón de momios de seguir en Q1\n(escala log, IC 95%; gris = no significativo)")
    save(fig, "f4_momios")


def modelos():
    t = pd.read_csv(TAB / "comparacion_modelos.csv")
    t = t[~t.Modelo.str.contains("estratificada")]
    nombres = {"Base: siempre la clase mayoritaria": "Base: clase mayoritaria", "Base: sólo índice de origen": "Base: solo índice origen"}
    t["lab"] = t.Modelo.replace(nombres)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    y = np.arange(len(t))
    c = [GRIS, GRIS, AZUL, AZUL2, AZUL2, AZUL2]
    ax.barh(y, t["AUC CV (media)"], xerr=t["AUC CV (desv.)"], color=c, capsize=4)
    for yy, (_, r) in zip(y, t.iterrows()):
        ax.text(r["AUC CV (media)"] + r["AUC CV (desv.)"] + 0.012, yy, f"{r['AUC CV (media)']:.2f} ({r['Tiempo de entrenamiento (s)']:.2f} s)", va="center", fontsize=14)
    ax.set_yticks(y, t.lab); ax.invert_yaxis(); ax.set_xlim(0.4, 1.0); ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8])
    ax.axvline(0.5, color=GRIS, ls=":")
    ax.set_xlabel("AUC en validación cruzada (0.5 = azar)\n(entre paréntesis: tiempo de entrenamiento)")
    save(fig, "f5_modelos")


def escenarios():
    e = pd.read_csv(TAB / "escenarios_roadmap.csv").dropna(subset=["Cambio vs continuidad (pts)"]).iloc[1:]
    lab = {"Mejora educativa (+1 nivel)": "+1 nivel educativo",
           "Mejora educativa sin mejora laboral (todos informales)": "+1 nivel, todos informales",
           "Mejora educativa con empleo formal": "+1 nivel y empleo formal",
           "Reducción de brecha territorial (Sur con perfil del Centro)": "Sur con perfil del Centro"}
    e["lab"] = e.Escenario.map(lab)
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    y = np.arange(len(e))
    v = e["Cambio vs continuidad (pts)"]
    ax.barh(y, v, xerr=[v - e["IC 95% inf"], e["IC 95% sup"] - v], color=AZUL, capsize=5)
    for yy, x in zip(y, v):
        ax.text(0.4, yy, f"{x:.0f} pts", va="center", ha="left", fontsize=15, fontweight="bold", color=AZUL)
    ax.set_xlim(min(e["IC 95% inf"]) - 1, 4.5)
    ax.set_yticks(y, e.lab); ax.invert_yaxis(); ax.axvline(0, color="black", lw=1)
    ax.set_xlabel("Cambio en % que sigue en Q1\nvs situación observada (pts, IC 95%)")
    save(fig, "f6_escenarios")


def estados():
    d = pd.read_csv(TAB / "contexto_vs_persistencia.csv")
    r = np.corrcoef(d.pobreza_pct, d.pct)[0, 1]
    fig, ax = plt.subplots(figsize=(5.4, 4.8))
    ax.scatter(d.pobreza_pct, d.pct, s=d.n_efectivo * 3, color=AZUL2, alpha=.75, ec=AZUL)
    for _, row in d.iterrows():
        if row.entidad in ("Guerrero", "Chiapas", "Oaxaca", "Veracruz", "Jalisco", "Hidalgo", "Ciudad de México", "Tamaulipas"):
            ax.annotate(row.entidad, (row.pobreza_pct, row.pct), fontsize=11, xytext=(4, 3), textcoords="offset points")
    b = np.polyfit(d.pobreza_pct, d.pct, 1)
    xx = np.linspace(d.pobreza_pct.min(), d.pobreza_pct.max(), 10)
    ax.plot(xx, np.polyval(b, xx), color=NARANJA, lw=2, ls="--")
    ax.set_xlabel("Pobreza estatal 2022 (% CONEVAL)")
    ax.set_ylabel("% que sigue en Q1 (EMOVI)")
    # r se reporta con los valores sin redondear del notebook 03 (0.56); aquí se calcula con la tabla redondeada.
    ax.set_title("r ≈ 0.56  ·  18 estados (n ≥ 40)", fontsize=15)
    save(fig, "f7_estados")


if __name__ == "__main__":
    for f in (matriz, grupos, desventajas, momios, modelos, escenarios, estados):
        f()
    print("Figuras en", OUT)
