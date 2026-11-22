#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

def ouvrirUnFichier(nom):
    with open(nom, "r", encoding='utf-8') as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste

def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement

# Question 2
print("Question 2")
df_restaurants=ouvrirUnFichier("data/classement-restaurants-paris-2023-par-enseignes.csv")

# Question 3
print("Question 3")
nb_etablissements=list(df_restaurants["Nombre d'établissement"])

# Question 4
print("Question 4")
nb_etablissements_tries = ordreDecroissant(nb_etablissements)
rangs_restaurants=list(range(1, len(nb_etablissements_tries)+1))

# Question 5
print("Question 5")
plt.figure(figsize=(6,4))
plt.plot(rangs_restaurants, nb_etablissements_tries)
plt.title("Loi rang-taille des enseignes (échelle linéaire)")
plt.xlabel("Rang")
plt.ylabel("Nombre d'établissements")
plt.tight_layout()
plt.savefig("rang_taille_lineaire.png")
plt.close()

# Question 6
print("Question 6")
log_rangs = conversionLog(rangs_restaurants)
log_nb_etablissements = conversionLog(nb_etablissements_tries)

plt.figure(figsize=(6, 4))
plt.plot(log_rangs, log_nb_etablissements)
plt.title("Loi rang-taille des enseignes (échelle logarithmique)")
plt.xlabel("log(Rang)")
plt.ylabel("log(Nombre d'établissements)")
plt.tight_layout()
plt.savefig("rang_taille_log.png")
plt.close()

# Question 7
print("Question 7")
# Mettre ici votre réponse argumentée
#Oui, il est possible de faire des tests sur les rangs : par exemple des tests de corrélation
#de rangs (Spearman ou Kendall) pour comparer deux classements, ou des tests d'adéquation /
#d'ajustement (ex. régression en log-dog ou tests de loi de puissance) pour évaluer la relation
#entre le rang et la taille

# Question 9
print("Question 9")
df_monde = ouvrirUnFichier("data/Le-Monde-HS-Etats-du-monde-2007-2026.csv")

# Question 10
print("Question 10")
print("Question 10")
etats = list(df_monde["État"])
pop_2007 = list(df_monde["Pop 2007"])
pop_2026 = list(df_monde["Pop 2026"])
densite_2007 = list(df_monde["Densité 2007"])
densite_2026 = list(df_monde["Densité 2026"])

# Question 11
print("Question 11")
ordre_pop_2007 = ordrePopulation(pop_2007, etats)
ordre_pop_2026 = ordrePopulation(pop_2026, etats)
ordre_densite_2007 = ordrePopulation(densite_2007, etats)
ordre_densite_2026 = ordrePopulation(densite_2026, etats)

# Question 12
print("Question 12")
comparaison_2007 = classementPays(ordre_pop_2007, ordre_densite_2007)
comparaison_2007.sort()

comparaison_2026 = classementPays(ordre_pop_2026, ordre_densite_2026)
comparaison_2026.sort()

# Question 13
print("Question 13")
rangs_pop_2007 = []
rangs_densite_2007 = []
for ligne in comparaison_2007:
    rangs_pop_2007.append(ligne[0])
    rangs_densite_2007.append(ligne[1])

rangs_pop_2026 = []
rangs_densite_2026 = []
for ligne in comparaison_2026:
    rangs_pop_2026.append(ligne[0])
    rangs_densite_2026.append(ligne[1])

# Question 14
print("Question 14")
spearman_2007 = scipy.stats.spearmanr(rangs_pop_2007, rangs_densite_2007)
kendall_2007 = scipy.stats.kendalltau(rangs_pop_2007, rangs_densite_2007)
print("2007 - Spearman :", spearman_2007, "| Kendall :", kendall_2007)
print(f"Q14 (2007) | Spearman r = {spearman_2007[0]:.4f} (p = {spearman_2007[1]:.4e}) | Kendall tau = {kendall_2007[0]:.4f} (p = {kendall_2007[1]:.4e})")

spearman_2026 = scipy.stats.spearmanr(rangs_pop_2026, rangs_densite_2026)
kendall_2026 = scipy.stats.kendalltau(rangs_pop_2026, rangs_densite_2026)
print("2026 - Spearman :", spearman_2026, "| Kendall :", kendall_2026)
print(f"Q14 (2026) | Spearman r = {spearman_2026[0]:.4f} (p = {spearman_2026[1]:.4e}) | Kendall tau = {kendall_2026[0]:.4f} (p = {kendall_2026[1]:.4e})")

spearman_2026 = scipy.stats.spearmanr(rangs_pop_2026, rangs_densite_2026)
kendall_2026 = scipy.stats.kendalltau(rangs_pop_2026, rangs_densite_2026)
print("2026 - Spearman :", spearman_2026, "| Kendall :", kendall_2026)

print("\n=== RÉCAPITULATIF SÉANCE 5 ===")
print(f"Q2-Q4 | Nombre d'enseignes (2023) : {len(nb_etablissements_tries)} | Top 5 : {nb_etablissements_tries[:5]}")
print("Q5-Q6 | Graphiques enregistrés : rang_taille_lineaire.png et rang_taille_log.png")
print("Q7    | Tests sur les rangs : possible (corrélations de rangs Spearman/Kendall ou ajustement log-log / loi de puissance)")
print(f"Q9-Q11| États traités (2007 / 2026) : {len(ordre_pop_2007)} / {len(ordre_pop_2026)} | Top 3 pop 2026 : {ordre_pop_2026[:3]}")
print(f"Q12-Q13| Lignes comparées 2007 / 2026 : {len(comparaison_2007)} / {len(comparaison_2026)}")
print(f"Q14 (2007) | Spearman r = {spearman_2007[0]:.4f} (p = {spearman_2007[1]:.4e}) | Kendall tau = {kendall_2007[0]:.4f} (p = {kendall_2007[1]:.4e})")
print(f"Q14 (2026) | Spearman r = {spearman_2026[0]:.4f} (p = {spearman_2026[1]:.4e}) | Kendall tau = {kendall_2026[0]:.4f} (p = {kendall_2026[1]:.4e})")

#Bonus : Créer des fonctions locales permettant de calcuer rapidement une analyse de rangs
    #Pour les restaurants, données du fichier restaurants-paris-2017 : comparaison addresses postales entre la liste des restaurants en 2017 et celle en 2023
# 1-FONCTIONS LOCALES BONUS : ANALYSE DE RANGS
def calculerRangs(valeurs):
    """Retourne les rangs (1 = plus grande valeur) associés à une liste de valeurs."""
    tries = sorted(((val, idx) for idx, val in enumerate(valeurs)), key=lambda x: x[0], reverse=True)
    rangs = [0] * len(valeurs)
    for rang, (_, idx_orig) in enumerate(tries, start=1):
        rangs[idx_orig] = rang
    return rangs


def comparerRangs(valeurs_a, valeurs_b):
    """Calcule rangs, corrélation de Spearman et concordance de Kendall entre deux séries."""
    rangs_a = calculerRangs(valeurs_a)
    rangs_b = calculerRangs(valeurs_b)
    spearman = scipy.stats.spearmanr(rangs_a, rangs_b)
    kendall = scipy.stats.kendalltau(rangs_a, rangs_b)
    return {
        "rangs_a": rangs_a,
        "rangs_b": rangs_b,
        "spearman_r": float(spearman[0]),
        "spearman_p": float(spearman[1]),
        "kendall_tau": float(kendall[0]),
        "kendall_p": float(kendall[1]),
    }

#2-Comparaison 2017 vs 2023
print("\n=== BONUS : 2017 vs 2023 ===")
df_2017 = ouvrirUnFichier("data/classement-restaurants-paris-2017-par-enseignes.csv")
df_communes = pd.merge(
    df_2017,
    df_restaurants,
    on="Enseigne",
    suffixes=("_2017", "_2023")
)
res_bonus = comparerRangs(
    list(df_communes["Nombre d'établissement_2017"]),
    list(df_communes["Nombre d'établissement_2023"])
)
print(
    f"Enseignes communes : {len(df_communes)} | "
    f"Spearman r = {res_bonus['spearman_r']:.4f} (p = {res_bonus['spearman_p']:.4e}) | "
    f"Kendall tau = {res_bonus['kendall_tau']:.4f} (p = {res_bonus['kendall_p']:.4e})"
)
