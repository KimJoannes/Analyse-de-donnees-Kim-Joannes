#coding:utf8

import numpy as np
import pandas as pd
import scipy
import scipy.stats as stats
import matplotlib.pyplot as plt

#https://docs.scipy.org/doc/scipy/reference/stats.html

dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)

# Question 1
print("Question 1")
import os
os.makedirs('img',exist_ok=True)
def plot_discret(x,y,titre,nom_fichier):
    """Trace un diagramme en bâtons pour une loi discrète et l'enregistre dans img/."""
    plt.figure(figsize=(6,4))
    plt.stem(x,y,basefmt=" ")
    plt.title(titre)
    plt.xlabel("k (valeurs possibles)")
    plt.ylabel("Probabilité P (X=k)")
    plt.savefig(f"img/C:\KimJoannes-Forriez-2026-2027-Analyse-de-donnees\Seance-03\src.png",dpi=300)
    plt.close()

def plot_continu(x,y,titre, nom_fichier):
    """Trace une courbe de densité pour une loi continue et l'enregistrer dans img/."""
    plt.figure(figsize=(6,4))
    plt.plot(x,y,lw=2,color='royalblue')
    plt.title(titre)
    plt.xlabel("x")
    plt.ylabel("Densité de probabilité f(x)")
    plt.savefig(f"img/C:\KimJoannes-Forriez-2026-2027-Analyse-de-donnees\Seance-03\src",dpi=300)
    plt.close()
    
#1 variables discrètes
#A.Loi de Dirac (fonction personnalisée: probabilité de 1 en un point unique, 0 ailleurs)
x_dirac=np.arange(0, 7)
y_dirac=np.where(x_dirac == 3, 1.0, 0.0)
plot_discret(x_dirac, y_dirac, "Loi de Dirax (a=3)","loi_dirac")

#B.Loi uniforme discète (via scipy.stats.randint)
low,high = 1,7
x_uni_d=np.arange(low,high)
y_uni_d=stats.randint.pmf(x_uni_d,low,high)
plot_discret(x_uni_d,y_uni_d,"Loi uniforme discètre (1 à 6)","loi_uniforme_discrete")

#C.Loi binomiale(via scipy.stats.binom)
n_binom,p_binom=10,0.5
x_binom=np.arange(0, n_binom+1)
y_binom=stats.binom.pmf(x_binom,n_binom,p_binom)
plot_discret(x_binom,y_binom,"Loi binomiale (n=10, p=0.5)", "loi_binomiale")

#D.Loi de Poisson (discrète) (via scpipy.stats.poisson)
mu_poisson=3.0
x_poisson=np.arange(0,13)
y_poisson=stats.poisson.pmf(x_poisson,mu_poisson)
plot_discret(x_poisson,y_poisson,"Loi de Poisson(mu=3)","loi_poisson")

#E.Loi de Zipf-Mandelbrot (fonction personnalisée)
def zipf_mandelbrot_pmf(k,s,q,n_max):
    k=np.asarray(k,dtype=float)
    poids=1.0/((k+q)**s)
    constante_norm=np.sum(1.0/((np.arange(1, n_max+1,dtype=float)+q)**s))
    return poids/constante_norm
x_zm=np.arange(1,21)
y_zm=zipf_mandelbrot_pmf(x_zm,s=1.5,q=2.0,n_max=50)
plot_discret(x_zm,y_zm,"Loi de Zipf-Mandelbrot(s=1.5,q=2.0)","loi_zipf_manderlbrot")

# 2. VARIABLES CONTINUES

# Loi normale N (mu=0,sigma=1)
x_norm = np.linspace(-4, 4, 300)
y_norm = stats.norm.pdf(x_norm, loc=0, scale=1)
plot_continu(x_norm, y_norm, "Loi normale (mu=0, sigma=1)", "loi_normale")

# Loi log-normale (s=0.5, scale=1)
x_lognorm = np.linspace(0.01, 4, 300)
y_lognorm = stats.lognorm.pdf(x_lognorm, s=0.5,scale=1)
plot_continu(x_lognorm, y_lognorm, "Loi log-normale(s=0.5)", "loi_log_normale")

#Loi uniforme continue sur [0,1]->loc=0, scale=1(borne sup = loc+scale)
x_uni_c = np.linspace(-0.5, 1.5, 300)
y_uni_c = stats.uniform.pdf(x_uni_c, loc=0, scale=1)
plot_continu(x_uni_c, y_uni_c, "Loi uniforme continue[0,1]", "loi_uniforme_continue")

#Loi du Chi-deux (df=4 degrés de liberté)
x_chi2 = np.linspace(0, 16, 300)
y_chi2 = stats.chi2.pdf(x_chi2, df=4)
plot_continu(x_chi2, y_chi2, "Loi du Chi-deux (df=4)", "loi_chi2")

#Loi de Pareto(b=2.5, scale=1)
x_pareto = np.linspace(1, 6, 300)
y_pareto = stats.pareto.pdf(x_pareto, b=2.5,scale=1)
plot_continu(x_pareto, y_pareto, "Loi de Pareto(b=2.5,x_m=1)", "loi_pareto")

print("Terminé ! Toutes les images ont été enregistrées dans le dossier 'img'.")

# Question 2
print("Question 2")
import numpy as np
import scipy.stats as stats


# --- LOIS DISCRÈTES ---

def stats_dirac(a=3.0):
    """Moyenne et écart type d'une loi de Dirac centrée en a."""
    moyenne = float(a)
    ecart_type = 0.0
    return moyenne, ecart_type


def stats_uniforme_discrete(low=1, high=7):
    """Moyenne et écart type d'une loi uniforme discrète sur {low, ..., high-1}."""
    moyenne, variance = stats.randint.stats(low, high, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_binomiale(n=10, p=0.5):
    """Moyenne et écart type d'une loi binomiale Bin(n, p)."""
    moyenne, variance = stats.binom.stats(n, p, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_poisson(mu=3.0):
    """Moyenne et écart type d'une loi de Poisson P(mu)."""
    moyenne, variance = stats.poisson.stats(mu, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_zipf_mandelbrot(s=1.5, q=2.0, n_max=50):
    """Moyenne et écart type d'une loi de Zipf-Mandelbrot tronquée sur 1..n_max."""
    k = np.arange(1, n_max + 1, dtype=float)
    poids = 1.0 / ((k + q) ** s)
    pmf = poids / np.sum(poids)
    moyenne = float(np.sum(k * pmf))
    variance = float(np.sum(((k - moyenne) ** 2) * pmf))
    return moyenne, float(np.sqrt(variance))


# --- LOIS CONTINUES ---

def stats_normale(loc=0.0, scale=1.0):
    """Moyenne et écart type d'une loi normale N(loc, scale^2)."""
    moyenne, variance = stats.norm.stats(loc=loc, scale=scale, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_log_normale(s=0.5, scale=1.0):
    """Moyenne et écart type d'une loi log-normale."""
    moyenne, variance = stats.lognorm.stats(s, scale=scale, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_uniforme_continue(loc=0.0, scale=1.0):
    """Moyenne et écart type d'une loi uniforme continue sur [loc, loc + scale]."""
    moyenne, variance = stats.uniform.stats(loc=loc, scale=scale, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_chi2(df=4):
    """Moyenne et écart type d'une loi du chi-deux à df degrés de liberté."""
    moyenne, variance = stats.chi2.stats(df, moments="mv")
    return float(moyenne), float(np.sqrt(variance))


def stats_pareto(b=2.5, scale=1.0):
    """Moyenne et écart type d'une loi de Pareto (b > 2 pour variance finie)."""
    moyenne, variance = stats.pareto.stats(b, scale=scale, moments="mv")
    return float(moyenne), float(np.sqrt(variance))

print("Terminé ! Toutes les images ont été enregistrées dans le dossier 'img'.")