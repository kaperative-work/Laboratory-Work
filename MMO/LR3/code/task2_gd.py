import matplotlib.pyplot as plt
import numpy as np

def mse(X, y, w):
    r = X @ w - y
    return float(np.mean(r * r))


def grad_mse(X, y, w):
    n = X.shape[0]
    r = X @ w - y
    return (2.0 / n) * (X.T @ r)


def gradient_descent(X, y, eta, eps=1e-8, max_iter=10000, lam=0.0):
    """Полный градиентный спуск. lam > 0 — проксимальный шаг для штрафа L1."""
    w = np.zeros(X.shape[1], dtype=float)
    history = []
    for _ in range(max_iter):
        w_new = w - eta * grad_mse(X, y, w)
        if lam > 0.0:
            thr = eta * lam
            w_new[1:] = np.sign(w_new[1:]) * np.maximum(np.abs(w_new[1:]) - thr, 0.0)
        history.append(mse(X, y, w_new))
        if history[-1] > 1e12:
            w = w_new
            break
        weight_dist = np.linalg.norm(w_new - w, ord=2)
        w = w_new
        if weight_dist < eps:
            break
    return w, np.asarray(history, dtype=float)


w_ols, *_ = np.linalg.lstsq(Xb, y, rcond=None)
normal_eq_w = np.linalg.inv(Xb.T @ Xb) @ Xb.T @ y
print("МНК, веса:", np.round(w_ols, 6))
print("Нормальное уравнение, веса:", np.round(normal_eq_w, 6))
print("||w_мнк - w_норм||:", f"{np.linalg.norm(w_ols - normal_eq_w):.3e}")
print("МНК, MSE:", round(mse(Xb, y, w_ols), 6))

etas = [0.001, 0.01, 0.1, 0.3, 1.0]
curves = {}
print()
print("Спуск на стандартизированных признаках, ε = 1e-8")
for eta in etas:
    w, hist = gradient_descent(Xb, y, eta=eta, eps=1e-8, max_iter=10000)
    curves[eta] = hist
    print(
        f"eta={eta:<5}  итераций={len(hist):<4}  "
        f"MSE={hist[-1]:.6g}  ||w-w_мнк||={np.linalg.norm(w - w_ols):.3e}"
    )

fig, ax = plt.subplots(figsize=(8, 4.2))
for eta in (0.001, 0.01, 0.1, 0.3):
    ax.plot(np.arange(1, len(curves[eta]) + 1), curves[eta], label=f"η = {eta}")
ax.set_xlabel("Итерация")
ax.set_ylabel("Среднеквадратичная ошибка")
ax.set_title("Полный градиентный спуск при разной скорости обучения")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "img_1.png", bbox_inches="tight")
plt.show()

print()
print("При eta = 1.0 ошибка расходится. Первые значения MSE:", np.round(curves[1.0][:6], 1))
print("Последнее MSE при eta = 1.0:", f"{curves[1.0][-1]:.4e}", "за", len(curves[1.0]), "шагов")

print()
print("Те же формулы на исходном масштабе, без стандартизации")
for eta in (1e-6, 1e-4, 0.01):
    _, hist = gradient_descent(Xb_raw, y, eta=eta, eps=1e-4, max_iter=500)
    print(f"eta={eta:<8}  итераций={len(hist):<4}  MSE: {hist[0]:.4g} -> {hist[-1]:.4g}")

_, hist_slow = gradient_descent(Xb_raw, y, eta=1e-4, eps=1e-12, max_iter=500)
_, hist_scaled = gradient_descent(Xb, y, eta=0.1, eps=1e-8, max_iter=500)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
axes[0].plot(hist_slow, color="darkorange")
axes[0].set_title("Без стандартизации, η = 0,0001")
axes[0].set_xlabel("Итерация")
axes[0].set_ylabel("MSE")
axes[1].plot(hist_scaled, color="steelblue")
axes[1].set_title("После стандартизации, η = 0,1")
axes[1].set_xlabel("Итерация")
axes[1].set_ylabel("MSE")
fig.tight_layout()
fig.savefig(FIG / "img_2.png", bbox_inches="tight")
plt.show()
