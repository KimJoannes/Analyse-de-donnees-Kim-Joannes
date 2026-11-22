#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE/"data"
IMG = BASE/"img"
IMG2 = BASE / "img2"

CSV_OUT = BASE / "csv"
XLSX_OUT = BASE / "xlsx"

IMG.mkdir(parents=True, exist_ok=True)
IMG2.mkdir(parents=True, exist_ok=True)
CSV_OUT.mkdir(parents=True, exist_ok=True)
XLSX_OUT.mkdir(parents=True, exist_ok=True)

def sauvegarder_tableau(tableau, nom_base, colonnes):
    df_sortie=pd.DataFrame(tableau, columns=colonnes)

    df_sortie.to_csv(
        CSV_OUT / f"{nom_base}.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_sortie.to_excel(
        XLSX_OUT / f"{nom_base}.xlsx",
        index=False
    )

    return df_sortie

def listedesterritoires(territoiretest, exportationUSD, importationUSD):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    totalparterritoire = []
    for element in range(0,len(liste)):
        totalparterritoire.append([liste[element][0], exportationUSD[liste[element][1]:liste[element][2]].sum(), importationUSD[liste[element][1]:liste[element][2]].sum()])
    return totalparterritoire

def nettoyage(colonne):
    colonne2 = []
    for element in colonne:
        if element == 'Sans objet' or element =='-':
            colonne2.append(float(0))
        else:
            colonne2.append(float(element))
    return colonne2

def getliste(territoiretest):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    return liste

# Question 4
print("Question 4")
# Source des données : https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
with open("./data/Produits-alimentaires-2024.csv", "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

# Question 5
print("Question 5")
print(contenu)
df=pd.DataFrame(contenu)
print("Contenu du DataFrame")
print(df)

# Question 6
print("Question 6")
nombre_lignes = len(contenu)
print("Nombre de lignes :", nombre_lignes)
nombre_colonnes = len(contenu.columns)
print("Nombre de colonnes :", nombre_colonnes)

# Question 7
print("Question 7")
print(contenu.head(1))

# Question 8
print("Question 8")
print("Types statistiques des colonnes:")
print(contenu.dtypes)

# Contenu des colonnes
# "year" : année
# "origin_id" : territoire de référence
# "dest_id" : territoire partenaire
# "Dist_VO (km)" : distance intercentroïde entre les deux territoires
# "hs92_Section_id" : code Section du produit
# "hs92_HS02_id" : code 2-digit du produit
# "hs92_HS04_id" : code 4-digit du produit
# "hs92_HS06_id" : code 6-digit du produit
# "export_val" : valeur des exportations du territoire de référence vers le territoire partenaire en dollars courants
# "import_val" : valeur des importations du territoire partenaire vers le territoire de référence en dollars courants
# "export_ton" : valeur des exportations du territoire de référence vers le territoire partenaire en tonnes
# "import_ton" : valeur des importations du territoire partenaire vers le territoire de référence en tonnes

# Question 9
print("Question 9")
export_ton = contenu["export_ton"]
import_ton=contenu["import_ton"]
territoires=contenu["origin_id"]

# Question 10
print("Question 10")
totaux_tonnes = []
for code, debut, fin in getliste(territoires):
    total_export = 0.0
    total_import = 0.0
    for valeur in export_ton.iloc[debut:fin]:
        if str(valeur).strip() != "-" and str(valeur).strip() != "Sans objet" and not pd.isna(valeur):
            total_export += float(valeur)
    for valeur in import_ton.iloc[debut:fin]:
        if str(valeur).strip() != "-" and str(valeur).strip() != "Sans objet" and not pd.isna(valeur):
            total_import += float(valeur)
    totaux_tonnes.append([code, total_export, total_import])

print(pd.DataFrame(totaux_tonnes, columns=["origin_id", "export_ton_total", "import_ton_total"]))
sauvegarder_tableau(totaux_tonnes, "totaux_tonnes_par_territoire",
                    ["origin_id", "export_ton_total", "import_ton_total"])
somme_exports_tonnes = sum(ligne[1] for ligne in totaux_tonnes)
somme_imports_tonnes = sum(ligne[2] for ligne in totaux_tonnes)
print("Total général exportations (tonnes) :", somme_exports_tonnes)
print("Total général importations (tonnes) :", somme_imports_tonnes)
print("Totaux identiques :", np.isclose(somme_exports_tonnes, somme_imports_tonnes))

# Question 11
print("Question 11")
# Appliquer la fonction listedesterritoires(...) sur vos colonnes ici
colonnes_usd = contenu[["origin_id", "export_val", "import_val"]]
totalparterritoire = listedesterritoires(
    colonnes_usd["origin_id"], colonnes_usd["export_val"], colonnes_usd["import_val"]
)
sauvegarder_tableau(totalparterritoire, "totaux_usd_par_territoire",
                    ["origin_id", "export_val_total", "import_val_total"])

for code, exportations, importations in totalparterritoire:
    if exportations == 0 and importations == 0:
        continue
    plt.figure(figsize=(6, 6))
    plt.pie([exportations, importations],
            labels=["Exportations", "Importations"],
            autopct="%1.1f%%", startangle=90)
    plt.title(f"Exportations et importations en USD - {code.upper()}")
    plt.tight_layout()
    plt.savefig(IMG / f"echanges_usd_{code}.png", dpi=150)
    plt.close()

# Questions 12 et 14
print("Questions 12 et 14")
# Application la fonction nettoyage(...) sur vos colonnes ici
distances_nettoyees = nettoyage(contenu["Dist_VO (km)"])
export_val_nettoyees = nettoyage(contenu["export_val"])
import_val_nettoyees = nettoyage(contenu["import_val"])
export_ton_nettoyees = nettoyage(contenu["export_ton"])
import_ton_nettoyees = nettoyage(contenu["import_ton"])

# Appliquer la fonction :
# liste = getliste(...)
liste = getliste(contenu["origin_id"])
# Mettre le code nouveau DataFrame ici et appeler la liste donnees2
donnees2titre = ["distance", "export_val_2", "import_val_2", "export_ton_2", "import_ton_2"]
donnees2 = pd.DataFrame({
    donnees2titre[0]: distances_nettoyees,
    donnees2titre[1]: export_val_nettoyees,
    donnees2titre[2]: import_val_nettoyees,
    donnees2titre[3]: export_ton_nettoyees,
    donnees2titre[4]: import_ton_nettoyees
})
# Compléter la boucle à partir des différents éléments précédents. Le nom des listes est celle proposée dans les commentaires.
# parametres = []
# quartiles = []
# deciles = []
# for element in range(0,len(donnees2.columns)):
#     parametres2 = []
#     distanceinterquartile = []
#     distanceinterdecile = []
#     for element2 in range(0,len(liste)):
#         codeiso = liste[element2][0]
#         data2 = donnees2.iloc[liste[element2][1]:liste[element2][2],element]

#         moyenne = 
#         mediane = 
#         mode = 
#         ecarttype = 
#         ecartabsolumoyen = 
#         etendue = 
#         parametres2.append([codeiso, moyenne, mediane, mode, ecarttype, ecartabsolumoyen, etendue])

#         quartile = 
#         distanceinterquartile.append([codeiso, (quartile[0.75] - quartile[0.25]).round(decimals=2)])
#         decile = 
#         distanceinterdecile.append([codeiso, (decile[0.9] - decile[0.1]).round(decimals=2)])
#     parametres.append(parametres2)
#     quartiles.append(distanceinterquartile)
#     deciles.append(distanceinterdecile)
parametres = []
quartiles = []
deciles = []
for element in range(len(donnees2.columns)):
    parametres2 = []
    distanceinterquartile = []
    distanceinterdecile = []
    for element2 in range(len(liste)):
        codeiso = liste[element2][0]
        data2 = donnees2.iloc[liste[element2][1]:liste[element2][2], element]
        moyenne = round(data2.mean(), 2)
        mediane = round(data2.median(), 2)
        modes = data2.mode()
        mode = round(modes.iloc[0], 2) if not modes.empty else np.nan
        ecarttype = round(data2.std(), 2)
        ecartabsolumoyen = round(abs(data2 - data2.mean()).mean(), 2)
        etendue = round(data2.max() - data2.min(), 2)
        parametres2.append([codeiso, moyenne, mediane, mode, ecarttype,
                            ecartabsolumoyen, etendue])

        quartile = data2.quantile([0.25, 0.75])
        distanceinterquartile.append([
            codeiso, round(quartile.loc[0.75] - quartile.loc[0.25], 2)
        ])
        decile = data2.quantile([0.1, 0.9])
        distanceinterdecile.append([
            codeiso, round(decile.loc[0.9] - decile.loc[0.1], 2)
        ])
    parametres.append(parametres2)
    quartiles.append(distanceinterquartile)
    deciles.append(distanceinterdecile)
noms_stats = ["moyenne", "mediane", "mode", "ecart_type", "ecart_absolu_moyen", "etendue"]
for i, nom_variable in enumerate(donnees2.columns):
    tableau = []
    for ligne in parametres[i]:
        tableau.append([ligne[0]] + ligne[1:])
    sauvegarder_tableau(tableau, f"statistiques_{nom_variable}",
                        ["origin_id"] + noms_stats)

# Question 13
print("Question 13")
print(pd.DataFrame(parametres[0],
                   columns=["origin_id"] + noms_stats).round(2))

# Question 14
# print("Question 14")
for i, nom_variable in enumerate(donnees2.columns):
    sauvegarder_tableau(quartiles[i], f"distance_interquartile_{nom_variable}",
                        ["origin_id", "distance_interquartile"])
    sauvegarder_tableau(deciles[i], f"distance_interdecile_{nom_variable}",
                        ["origin_id", "distance_interdecile"])

# Question 15
print("Question 15")
for nom_variable in donnees2.columns:
    plt.figure(figsize=(8, 5))
    plt.boxplot(donnees2[nom_variable].dropna(), vert=True)
    plt.ylabel(nom_variable)
    plt.title(f"Boîte à moustaches - {nom_variable}")
    plt.tight_layout()
    plt.savefig(IMG / f"boite_moustaches_{nom_variable}.png", dpi=150)
    plt.close()

# Question 16
print("Question 16")
# Source des données : BDCOM, https://www.apur.org/fr/open-data-cartes/open-data/base-donnees-commerces-parisiens
with open("./data/restaurants-paris-2023.csv", "r", encoding="utf-8") as fichier:
    contenu2 = pd.read_csv(fichier)
correspondance_surf = {
    1: "]0, 300] m²",
    2: "]300, 1000] m²",
    3: "]1000, +infini[ m²"
}
contenu2["categorie_surface"] = contenu2["surf"].map(correspondance_surf)
effectifs_surface = contenu2["surf"].value_counts().reindex([1, 2, 3], fill_value=0)
tableau_surface = [
    [1, correspondance_surf[1], int(effectifs_surface.loc[1])],
    [2, correspondance_surf[2], int(effectifs_surface.loc[2])],
    [3, correspondance_surf[3], int(effectifs_surface.loc[3])]
]
print(pd.DataFrame(tableau_surface,
                   columns=["code", "tranche_surface", "effectif"]))
sauvegarder_tableau(tableau_surface, "effectifs_par_tranche_surface",
                    ["code", "tranche_surface", "effectif"])
# Question bonus
print("Question bonus")
fichier_pays = DATA / "country_names.xls"
if fichier_pays.exists():
    try:
        pays = pd.read_excel(fichier_pays)  # nécessite le paquet xlrd pour .xls
        print("Colonnes du fichier country_names.xls :", pays.columns.tolist())
        # Repérage automatique des colonnes ISO et nom ; à ajuster si nécessaire
        # selon les intitulés exacts présents dans le classeur fourni.
        colonnes = {str(c).lower(): c for c in pays.columns}
        col_iso = next((v for k, v in colonnes.items()
                        if "iso" in k or k in ("id", "code")), None)
        col_nom = next((v for k, v in colonnes.items()
                        if "name" in k or "nom" in k or "country" in k), None)
        if col_iso is not None and col_nom is not None:
            noms_pays = dict(zip(pays[col_iso].astype(str).str.lower(),
                                 pays[col_nom].astype(str)))
            for code, exportations, importations in totalparterritoire:
                if exportations == 0 and importations == 0:
                    continue
                nom = noms_pays.get(str(code).lower(), str(code).upper())
                plt.figure(figsize=(6, 6))
                plt.pie([exportations, importations],
                        labels=["Exportations", "Importations"],
                        autopct="%1.1f%%", startangle=90)
                plt.title(f"Exportations et importations en USD - {nom}")
                plt.tight_layout()
                plt.savefig(IMG2 / f"echanges_usd_{code}.png", dpi=150)
                plt.close()
        else:
            print("Colonnes ISO/nom non identifiées : graphiques bonus non générés.")
    except ImportError:
        print("Bonus ignoré : installer xlrd avec 'pip install xlrd' pour lire country_names.xls.")
    except Exception as erreur:
        print("Bonus non exécuté :", erreur)
else:
    print("Fichier country_names.xls absent.")

print("Analyse terminée. Résultats : dossiers img, csv et xlsx.")
