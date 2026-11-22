#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats
import numpy as np
from scipy import stats

# C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
# Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
# Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

# Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

# Question 1 : Théorie de l'échantillonnage (intervalles de fluctuation)
# L'échantillonnage se base sur la répétitivité.
print("Question 1")
df_ech = ouvrirUnFichier("data/Echantillonnage-100-Echantillons.csv")

moyennes_arrondies = {col: round(float(df_ech[col].mean())) for col in df_ech.columns}
total_moyennes = sum(moyennes_arrondies.values())
freq_ech = {col: round(val / total_moyennes, 2) for col, val in moyennes_arrondies.items()}

pop_mere = {"Pour": 852, "Contre": 911, "Sans opinion": 422}
total_pop = sum(pop_mere.values())
freq_pop = {col: round(val / total_pop, 2) for col, val in pop_mere.items()}

print("1. Moyennes arrondies (100 échantillons) :", moyennes_arrondies)
print("   Fréquences échantillons (arr. 2 déc.)  :", freq_ech)
print("   Fréquences population mère (arr. 2 déc.):", freq_pop)
zc = 1.96
for col in df_ech.columns:
    p_obs = moyennes_arrondies[col] / total_moyennes
    marge = zc * np.sqrt((p_obs * (1 - p_obs)) / total_moyennes)
    print(f"   IF 95% [{col}] : [{p_obs - marge:.4f}, {p_obs + marge:.4f}]")
print("Résultat sur le calcul d'un intervalle de fluctuation")

# Question 2 : Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Question 2")
premier_echantillon= list(df_ech.iloc[0])
somme_ligne = sum(premier_echantillon)
print("\n2. Premier échantillon (liste):", premier_echantillon, "|Somme:", somme_ligne)
for col, effectif in zip(df_ech.columns, premier_echantillon):
    freq_i=effectif/somme_ligne
    marge_i=zc * np.sqrt((freq_i*(1-freq_i))/somme_ligne)
    print(f"IC 95% [{col}] (f={freq_i:.4f}) : [{freq_i - marge_i:.4f}, {freq_i + marge_i:.4f}]")
print("Résultat sur le calcul d'un intervalle de confiance")

# Question 3 : Théorie de la décision (tests d'hypothèse)
# La décision se base sur la notion de risques alpha et bêta.
# Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Question 3")
test1 = ouvrirUnFichier("data/Loi-normale-Test-1.csv")["Test"]
test2 = ouvrirUnFichier("data/Loi-normale-Test-2.csv")["Test"]

stat1, p1 = stats.shapiro(test1)
stat2, p2 = stats.shapiro(test2)
print(f"\n3. Shapiro Test 1 : W={stat1:.4f}, p-value={p1:.4e}")
print(f"   Shapiro Test 2 : W={stat2:.4f}, p-value={p2:.4e}")
print("Théorie de la décision")

# Question bonus
print("Question bonus")
print("Résumé Test 2:", test2.describe())
print("Effectifs par valeur Test 2:\n", test2.value_counts().sort_index())
#Loi-normal-Test-2.csv suit une loi de Zipf (distribution discrète en loi de puissance, vue en Séance 3)
#Les données sont des entiers positifs (1 à 14) fortement concentrés sur la valeur 1 (1 792 occurrences sur 2 000), avec une chute rapide des effectifs et une longue traîne à droite (très loin de la symétrie en cloche de la loi normale)
#Cela explique la statistique W très faible (environ 0.2609) et la p-value extrêmement petite (environ 7.05*$\approx 7.05 \times 10^{-67}<0.05)