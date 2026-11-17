from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(r"D:\MLM")
DATA = ROOT / "data" / "LR4" / "Bankloan.csv"
FIG = ROOT / "Screenshots" / "LR4"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams["axes.grid"] = True
plt.rcParams["figure.dpi"] = 120

df_raw = pd.read_csv(DATA)
print("Файл:", DATA.name)
print("Строк:", df_raw.shape[0], "столбцов:", df_raw.shape[1])
print("Столбцы:", list(df_raw.columns))
print()
df_raw.info()
print()
print(df_raw.describe().T.round(3).to_string())
print()
print("Пропуски по столбцам:")
print(df_raw.isna().sum().to_string())
print("Всего пропусков:", int(df_raw.isna().sum().sum()))
print()
print("Уровни образования ed:", df_raw["ed"].value_counts().sort_index().to_dict())

known = df_raw["default"].notna()
labeled = df_raw.loc[known, "default"].astype(int)
print("Строк с известным default:", int(known.sum()))
print("Строк без метки:", int((~known).sum()))
print(labeled.value_counts().sort_index().to_string())
print("Доля класса 1:", round(float(labeled.mean()), 4))

fig, ax = plt.subplots(figsize=(6.2, 3.6))
counts = labeled.value_counts().sort_index()
ax.bar(["нет просрочки (0)", "просрочка (1)"], counts.values, color=["steelblue", "darkorange"])
for i, value in enumerate(counts.values):
    ax.text(i, value + 8, str(int(value)), ha="center")
ax.set_ylabel("Число заёмщиков")
ax.set_title("Целевой признак default среди размеченных строк")
fig.tight_layout()
fig.savefig(FIG / "img.png", bbox_inches="tight")
plt.show()

missing = df_raw.isna().sum()
fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.bar(missing.index.astype(str), missing.values, color="slategray")
ax.set_ylabel("Число пропусков")
ax.set_title("Пропуски по столбцам")
ax.tick_params(axis="x", rotation=30)
fig.tight_layout()
fig.savefig(FIG / "img_1.png", bbox_inches="tight")
plt.show()
