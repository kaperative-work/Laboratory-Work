from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_regression

FIG = Path(r"D:\MLM\Screenshots\LR3")
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams["axes.grid"] = True
plt.rcParams["figure.dpi"] = 120

X0, y, coef_true = make_regression(
    n_samples=300,
    n_features=3,
    n_informative=3,
    noise=12.0,
    bias=5.0,
    coef=True,
    random_state=26,
)
scales = np.array([1.0, 40.0, 0.05])
X_raw = X0 * scales

mu = X_raw.mean(axis=0)
sigma = X_raw.std(axis=0)
X = (X_raw - mu) / sigma

print("Объектов:", X_raw.shape[0], "признаков:", X_raw.shape[1])
print("Истинные коэффициенты make_regression:", np.round(coef_true, 4))
print("Множители масштаба:", scales)
print("Средние до стандартизации:", np.round(mu, 4))
print("СКО до стандартизации:", np.round(sigma, 4))
print("Средние после стандартизации:", np.round(X.mean(0), 6))
print("СКО после стандартизации:", np.round(X.std(0), 6))
print("Среднее y:", round(float(y.mean()), 6))


def design(features):
    return np.column_stack([np.ones(len(features)), features])


Xb = design(X)
Xb_raw = design(X_raw)

fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))
names = ["признак 1", "признак 2", "признак 3"]
for j, ax in enumerate(axes):
    ax.scatter(X[:, j], y, s=12, alpha=0.7, color="steelblue")
    ax.set_xlabel(names[j] + " после стандартизации")
    ax.set_ylabel("y")
fig.suptitle("Целевая величина и три признака")
fig.tight_layout()
fig.savefig(FIG / "img.png", bbox_inches="tight")
plt.show()
