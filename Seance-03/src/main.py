#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Lecture du fichier CSV
df = pd.read_csv("./data/resultats-elections-presidentielles-2022-1er-tour.csv")

# Étape 5 : sélection des colonnes quantitatives
num = df.select_dtypes(include=[np.number])

res = pd.DataFrame({
    "moyenne": num.mean(),
    "médiane": num.median(),
    "mode": num.mode().iloc[0],
    "écart-type": num.std(),
    "écart abs. moy.": num.apply(lambda s: np.mean(np.abs(s - s.mean()))),
    "étendue": num.max() - num.min()
}).round(2)

# Étape 6 : affichage
print("\n--- Paramètres statistiques arrondis à deux décimales ---\n")
print(res)

# Etape 7 :
q = num.quantile([.10,.25,.75,.90])
res = (q.loc[.75]-q.loc[.25]).to_frame("IQR (Q3-Q1)")
res["IDR (P90-P10)"] = q.loc[.90]-q.loc[.10]
print(res.round(2))

# Etape 8 :
os.makedirs("img", exist_ok=True)
for c in num: plt.boxplot(num[c].dropna(), showmeans=True); plt.title(c); plt.savefig(f"img/{c}.png"); plt.close()
print("Graphiques enregistrés dans 'img/'")

# Etape 9 :
df = pd.read_csv("data/island-index.csv")

# Etape 10 :
df = pd.read_csv("data/island-index.csv", low_memory=False)
col = [c for c in df.columns if "Surface" in c and "km" in c][0]
df[col] = pd.to_numeric(df[col], errors="coerce")

bins = [0,10,25,50,100,2500,5000,10000,float("inf")]
labels = ["]0,10]","]10,25]","]25,50]","]50,100]","]100,2500]","]2500,5000]","]5000,10000]","]10000,+∞["]

print(df.assign(cat=pd.cut(df[col], bins=bins, labels=labels))
        ["cat"].value_counts().reindex(labels, fill_value=0))




