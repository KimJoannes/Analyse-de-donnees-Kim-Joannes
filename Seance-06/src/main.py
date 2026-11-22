#coding:utf8

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats

def ouvrirUnFichier(nom):
    with open(nom, "r", encoding = "utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

def analyser_paire(df, col_x, col_y):
    sub = df[[col_x, col_y]].copy()
    sub[col_x] = pd.to_numeric(sub[col_x], errors="coerce")
    sub[col_y] = pd.to_numeric(sub[col_y], errors="coerce")
    sub = sub.dropna()
    x = sub[col_x]
    y = sub[col_y]
    reg_xy = scipy.stats.linregress(x, y)
    reg_yx = scipy.stats.linregress(y, x)
    corr = x.corr(y)
    return x, y, reg_xy, reg_yx, corr

def tracer_regression(x, y, reg, titre, xlabel, ylabel, fichier_sortie):
    plt.figure(figsize=(6, 4.5))
    plt.scatter(x, y, alpha=0.65, s=22, label="Territoires")
    x_vals = np.linspace(x.min(), x.max(), 200)
    y_vals = reg.intercept + reg.slope * x_vals
    plt.plot(
        x_vals,
        y_vals,
        color="red",
        linewidth=2,
        label=f"y = {reg.slope:.4f}x + {reg.intercept:.2e} (r={reg.rvalue:.3f})",
    )
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(fichier_sortie, dpi=130)
    plt.close()
    
# Question 1
print("Question 1")

# "Année" : Année, ici 2024
# "Code-ISO" : code ISO du territoire
# "Total-export-alimentaire-USD" : total des exportations concernant les produits alimentaires
# "Total-import-alimentaire-USD" : total des importations concernant les produits alimentaires
# "Total-export-autres-USD" : total des exportations concernant les produits non alimentaires
# "Total-import-autres-USD" : total des importations concernant les produits non alimentaires
# "Total-export-USD" : total des exportations
# "Total-import-USD" : total des importations

chemin_2024=Path("data/Produits-alimentaires-vs-autres-2024.csv")
if not chemin_2024.exists() and Path("data/Produits-alimentaires-vs-autres.csv").exists():
    chemin_2024 = Path("data/Produits-alimentaires-vs-autres.csv")
df = ouvrirUnFichier(chemin_2024)
annee = df["Année"]
code_iso = df["Code-ISO"]
export_alim = df["Total-export-alimentaire-USD"]
import_alim = df["Total-import-alimentaire-USD"]
export_autres = df["Total-export-autres-USD"]
import_autres = df["Total-import-autres-USD"]
export_total = df["Total-export-USD"]
import_total = df["Total-import-USD"]

# Question 2
print("Question 2")
# Calcul de la régression linéaire pour la méthode des moindres carrées 1
# Calcul de la droite de régression 1
# Calcul de la régression linéaire pour la méthode des moindres carrées 2
# Calcul de la droite de régression 2
# Calcul de la régression linéaire pour la méthode des moindres carrées 3
# Calcul de la droite de régression 3

print("Question 2")
x1, y1, reg1_xy, reg1_yx, corr1 = analyser_paire(
    df, "Total-import-alimentaire-USD", "Total-export-alimentaire-USD"
)
x2, y2, reg2_xy, reg2_yx, corr2 = analyser_paire(
    df, "Total-import-autres-USD", "Total-export-autres-USD"
)
x3, y3, reg3_xy, reg3_yx, corr3 = analyser_paire(
    df, "Total-import-USD", "Total-export-USD"
)

for nom, r_xy, r_yx in [
    ("Alimentaire", reg1_xy, reg1_yx),
    ("Autres", reg2_xy, reg2_yx),
    ("Total", reg3_xy, reg3_yx),
]:
    print(
        f"[{nom}] x->y: pente={r_xy.slope:.4f}, ord={r_xy.intercept:.2f} | "
        f"y->x (inversé): pente={r_yx.slope:.4f}, ord={r_yx.intercept:.2f}"
    )

# Question 3
print("Question 3")
# Calcul du coefficient de corrélation 1
# Calcul du coefficient de corrélation 2
# Calcul du coefficient de corrélation 3
print(f"Corrélation Alimentaire : {corr1:.4f}")
print(f"Corrélation Autres      : {corr2:.4f}")
print(f"Corrélation Total       : {corr3:.4f}")

# Question 4
print("Question 4")
# Calcul du graphique 1
# Calcul du graphique 2
# Calcul du graphique 3
print("Question 4")
dossier_out = Path("outputs")
dossier_out.mkdir(parents=True, exist_ok=True)

tracer_regression(
    x1, y1, reg1_xy,
    "Produits alimentaires (2024)",
    "Total-import-alimentaire-USD", "Total-export-alimentaire-USD",
    dossier_out / "regression_alimentaire_2024.png",
)
tracer_regression(
    x2, y2, reg2_xy,
    "Produits non alimentaires (2024)",
    "Total-import-autres-USD", "Total-export-autres-USD",
    dossier_out / "regression_autres_2024.png",
)
tracer_regression(
    x3, y3, reg3_xy,
    "Commerce total (2024)",
    "Total-import-USD", "Total-export-USD",
    dossier_out / "regression_total_2024.png",
)

#Bonus : généralisation de 1995 à 2024
print("\n===BONUS:1995 à 2024===")
resultats_annees=[]
for an in range(1995,2025):
    fichier_an=Path(f"data/Produits-alimentaires-vs-autres-{an}.csv")
    if fichier_an.exists():
        df_an = ouvrirUnFichier(fichier_an)
        _, _, r_a, _, c_a = analyser_paire(
            df_an, "Total-import-alimentaire-USD", "Total-export-alimentaire-USD"
        )
        _, _, r_o, _, c_o = analyser_paire(
            df_an, "Total-import-autres-USD", "Total-export-autres-USD"
        )
        _, _, r_t, _, c_t = analyser_paire(
            df_an, "Total-import-USD", "Total-export-USD"
        )
        resultats_annees.append({
            "Annee": an,
            "pente_alim": r_a.slope,
            "corr_alim": c_a,
            "r2_alim": r_a.rvalue ** 2,
            "pente_autres": r_o.slope,
            "corr_autres": c_o,
            "pente_total": r_t.slope,
            "corr_total": c_t,
        })

df_synthese = pd.DataFrame(resultats_annees)
df_synthese.to_csv(dossier_out / "synthese_regressions_1995_2024.csv", index=False)

if not df_synthese.empty:
    plt.figure(figsize=(7, 4.2))
    plt.plot(df_synthese["Annee"], df_synthese["pente_alim"], marker="o", markersize=4, label="Pente Alimentaire")
    plt.plot(df_synthese["Annee"], df_synthese["corr_alim"], marker="s", markersize=4, label="Corrélation r Alimentaire")
    plt.title("Évolution 1995–2024 : pente et corrélation (Alimentaire)")
    plt.xlabel("Année")
    plt.ylabel("Valeur")
    plt.legend()
    plt.tight_layout()
    plt.savefig(dossier_out / "evolution_alimentaire_1995_2024.png", dpi=130)
    plt.close()
    print(df_synthese[["Annee", "pente_alim", "corr_alim", "r2_alim"]].to_string(index=False))