import matplotlib.pyplot as plt
import numpy as np

lambdas = np.logspace(-3, 3, 20)
weights = []
mses = []
iters = []
for lam in lambdas:
    w, hist = gradient_descent(Xb, y, eta=0.05, eps=1e-8, max_iter=10000, lam=float(lam))
    weights.append(w)
    mses.append(hist[-1])
    iters.append(len(hist))

W = np.vstack(weights)
print("Коэффициенты λ:")
print(np.array2string(lambdas, precision=4, separator=", "))
print()
print("λ          MSE        w0       w1       w2       w3    ненулевых признаков")
for lam, row, err in zip(lambdas, W, mses):
    nnz = int(np.sum(np.abs(row[1:]) > 1e-6))
    print(f"{lam:10.4g}  {err:9.3f}  {row[0]:7.3f}  {row[1]:7.3f}  {row[2]:7.3f}  {row[3]:7.3f}  {nnz}")

fig, ax = plt.subplots(figsize=(8, 4.4))
labels = ["w0 свободный член", "w1", "w2", "w3"]
for j, label in enumerate(labels):
    ax.plot(lambdas, W[:, j], marker="o", ms=3.5, label=label)
ax.set_xscale("log")
ax.set_xlabel("Коэффициент L1-регуляризации λ")
ax.set_ylabel("Вес")
ax.set_title("Веса линейной модели при росте λ")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "img_4.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(lambdas, mses, marker="o", ms=3.5, color="steelblue")
ax.set_xscale("log")
ax.set_xlabel("Коэффициент L1-регуляризации λ")
ax.set_ylabel("MSE")
ax.set_title("Ошибка на обучении при росте λ")
fig.tight_layout()
fig.savefig(FIG / "img_5.png", bbox_inches="tight")
plt.show()
