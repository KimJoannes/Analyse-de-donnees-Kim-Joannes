#coding:utf8

import numpy as np
import pandas as pd
import scipy
import scipy.stats

def ouvrirUnFichier(nom):
    with open(nom, "r", encoding = "utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

def tableauDeContingence(nom, donnees):
    indexValeurs = {}
    for element in range(0,len(nom)):
        indexValeurs.update({element: nom[element]})
    return pd.DataFrame(donnees).rename(index = indexValeurs)

def sommeDesColonnes(tableau):
    colonne = list(tableau.head(0))
    sommeColonne = []
    for element in colonne:
        sommeColonne.append(tableau[element].sum())
    return sommeColonne

def sommeDesLignes(tableau):
    colonne = list(tableau.head(0))
    sommeLigne = []
    for element1 in range(0,len(tableau)):
        ligne = []
        for element2 in range(0,len(colonne)):
            ligne.append(tableau.iloc[element1, element2])
        sommeLigne.append(np.sum(list(ligne)))
    return sommeLigne

data = pd.DataFrame(ouvrirUnFichier("./data/arrondissements-enseignes.csv"))
# print(data)

# Création du tableau de contingence
# Contrairement à l'usage, vous ne devez pas créer de tableau croisé dynamique, puisque le fichier est déjà un tableau de contingence
nomdescolonnes = list(data.head(0))
# print(nomdescolonnes)
dictionnaire = {}
for element in range(1, len(nomdescolonnes)):
    dictionnaire[nomdescolonnes[element]] = data[nomdescolonnes[element]]
contingence = tableauDeContingence = tableauDeContingence(data[nomdescolonnes[0]], dictionnaire)
# print(tableauDeContingence)

# Question 1
print("Question 1")
marges_lignes = sommeDesLignes(contingence)
marges_colonnes = sommeDesColonnes(contingence)
total_lignes = sum(marges_lignes)
total_colonnes = sum(marges_colonnes)
print("Marges des lignes :", marges_lignes)
print("Total marges lignes :", total_lignes)
print("Total marges colonnes :", total_colonnes)

# Question 2
print("Question 2")
print("Question 2")
totaux_identiques = total_lignes == total_colonnes
print("Total marges lignes == Total marges colonnes :", totaux_identiques)

# Question 3
print("Question 3")
# Faire le test du chi2 avec les outils Scipy.stats
chi2_stat, p_val, dof, ex = scipy.stats.chi2_contingency(contingence.values)
print(f"Chi2 = {chi2_stat:.4f} | ddl = {dof} | p-value = {p_val:.4e}")
print("Liaison significative (p < 0.05) :", p_val < 0.05)

# Question 4
print("Question 4")
print("Question 4")
effectif_total = total_lignes
phi2 = chi2_stat / effectif_total
print(f"Phi^2 de Pearson = {phi2:.6f}")

# Question bonus
print("Question bonus")
print("Question bonus")
echantillons = ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv")
f_stat, p_anova = scipy.stats.f_oneway(
    echantillons["Pour"],
    echantillons["Contre"],
    echantillons["Sans opinion"],
)
print(f"ANOVA (Pour / Contre / Sans opinion) : F = {f_stat:.4f} | p-value = {p_anova:.4e}")

# AFC (Analyse Factorielle des Correspondances) sur le tableau de contingence
X = contingence.astype(float).values
N = X.sum()
P = X / N
r = P.sum(axis=1, keepdims=True)
c = P.sum(axis=0, keepdims=True)
S = (P - r @ c) / np.sqrt(r @ c)
_, s_vals, _ = np.linalg.svd(S, full_matrices=False)
valeurs_propres = np.sort(s_vals ** 2)[::-1]
valeurs_propres = valeurs_propres[valeurs_propres < 0.999999]
inertie_totale = valeurs_propres.sum()
part_inertie = (valeurs_propres / inertie_totale) * 100
print(f"AFC inertie totale (= phi^2) : {inertie_totale:.6f}")
print("Top 5 valeurs propres AFC :", np.round(valeurs_propres[:5], 6))
print("Top 5 % inertie expliquée :", np.round(part_inertie[:5], 2))