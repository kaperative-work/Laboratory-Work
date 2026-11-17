import matplotlib.pyplot as plt
import numpy as np

def stochastic_gradient_descent(X, y, eta, max_epochs=100, seed=26, record_every=10):
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    w = np.zeros(X.shape[1], dtype=float)
    epoch_mse = []
    step_epoch = []
    step_mse = []
    seen = 0
    for _epoch in range(max_epochs):
        for _step in range(n):
            train_ind = int(rng.integers(0, n))
            x_i = X[train_ind:train_ind + 1]
            y_i = y[train_ind:train_ind + 1]
            y_pred = x_i @ w
            grad = (2.0 / y_i.shape[0]) * (x_i.T @ (y_pred - y_i))
            w = w - eta * np.ravel(grad)
            seen += 1
            if seen % record_every == 0:
                step_epoch.append(seen / n)
                step_mse.append(mse(X, y, w))
        epoch_mse.append(mse(X, y, w))
    return w, np.asarray(epoch_mse), np.asarray(step_epoch), np.asarray(step_mse)


epochs = 100
w_gd, hist_gd = gradient_descent(Xb, y, eta=0.1, eps=0.0, max_iter=epochs)
w_sgd, hist_sgd, step_epoch, step_mse = stochastic_gradient_descent(
    Xb, y, eta=0.001, max_epochs=epochs, seed=26
)

print("После", epochs, "эпох")
print("Полный спуск, η = 0,1:   MSE =", round(float(hist_gd[-1]), 6), " веса", np.round(w_gd, 4))
print("Стохастический, η = 0,001: MSE =", round(float(hist_sgd[-1]), 6), " веса", np.round(w_sgd, 4))
print("MSE метода наименьших квадратов:", round(mse(Xb, y, w_ols), 6))
print("Первая эпоха: полный", round(float(hist_gd[0]), 2), ", стохастический", round(float(hist_sgd[0]), 2))
print("Последние 8 значений MSE стохастического спуска:", np.round(hist_sgd[-8:], 3))

# Останов полного спуска по порогу, отдельно от графика фиксированной длины
w_stop, hist_stop = gradient_descent(Xb, y, eta=0.1, eps=1e-8, max_iter=10000)
print("Полный спуск с остановом ||Δw||_2 < 1e-8: итераций =", len(hist_stop), ", MSE =", round(float(hist_stop[-1]), 6))
rises = int(np.sum(np.diff(step_mse) > 1.0))
print("Число записанных шагов, где MSE выросла больше чем на 1:", rises)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
xs = np.arange(1, epochs + 1)
axes[0].plot(step_epoch, step_mse, color="darkorange", lw=0.8, label="стохастический, η = 0,001")
axes[0].plot(xs, hist_gd, color="steelblue", lw=2, label="полный, η = 0,1")
axes[0].set_xlabel("Эпоха")
axes[0].set_ylabel("Среднеквадратичная ошибка")
axes[0].set_title("Вся траектория")
axes[0].legend()
axes[1].plot(step_epoch, step_mse, color="darkorange", lw=0.8, label="стохастический, η = 0,001")
axes[1].plot(xs, hist_gd, color="steelblue", lw=2, label="полный, η = 0,1")
axes[1].set_xlim(20, 100)
axes[1].set_ylim(135.5, 160)
axes[1].set_xlabel("Эпоха")
axes[1].set_ylabel("Среднеквадратичная ошибка")
axes[1].set_title("Окрестность минимума")
axes[1].legend()
fig.suptitle("Полный и стохастический градиентный спуск")
fig.tight_layout()
fig.savefig(FIG / "img_3.png", bbox_inches="tight")
plt.show()
