# -----------------------------------------------
# Recyclavenir - ESG Scoring Prototype
# Auteur : Dr Edouard_V
# Date : Mars 2026
# -----------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# --- CONFIGURATION ---
DATA_PATH = "../data/recyclavenir_esg_data.csv"
OUTPUT_DIR = "../output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- LECTURE DES DONNÉES ---
df = pd.read_csv(DATA_PATH)

# Conversion sécurisée des valeurs numériques
for col in ["2023", "2024", "2025"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- CALCUL DES SCORES MOYENS PAR PILIER ---
scores = df.groupby("Piliers")[["2023", "2024", "2025"]].mean()

# Pondérations ESG
weights = {"Env": 0.5, "Soc": 0.3, "Gov": 0.2}

# Score global par année
global_scores = {}
for year in ["2023", "2024", "2025"]:
    global_scores[year] = sum(scores.loc[pillar, year] * weights[pillar] for pillar in weights)

# --- EXPORT DES SCORES ---
summary = pd.DataFrame(scores)
summary.loc["Global"] = [global_scores["2023"], global_scores["2024"], global_scores["2025"]]
summary.to_csv(os.path.join(OUTPUT_DIR, "esg_scores_summary.csv"))

# --- VISUALISATION RADAR 2025 ---
labels = list(scores.index)
values = list(scores["2025"])
values += values[:1]  # fermer le graphe
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_title("Profil ESG Recyclavenir - Année 2025", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "esg_radar_2025.png"))
plt.show()
