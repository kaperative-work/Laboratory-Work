import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

ROOT = Path(r"D:\SPP_7sem\MLM")
FIG = ROOT / "Screenshots" / "LR5"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams["axes.grid"] = True
plt.rcParams["figure.dpi"] = 120

RANDOM_STATE = 26
MAX_DEPTH = 3
MIN_SAMPLES_LEAF = 4

X, y = make_classification(
    n_samples=160,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    class_sep=0.9,
    flip_y=0.05,
    random_state=RANDOM_STATE,
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y,
)

print("Обучение:", X_train.shape[0], "тест:", X_test.shape[0], "признаков:", X_train.shape[1])
print("Классы на обучении:", np.bincount(y_train).tolist())
print("Классы на тесте:", np.bincount(y_test).tolist())

fig, ax = plt.subplots(figsize=(6.2, 4.4))
for label, color, name in ((0, "#4c78a8", "класс 0"), (1, "#f58518", "класс 1")):
    mask = y == label
    ax.scatter(X[mask, 0], X[mask, 1], c=color, s=28, label=name, edgecolors="white", linewidths=0.4)
ax.set_xlabel("Признак 1")
ax.set_ylabel("Признак 2")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "img.png")
plt.show()
