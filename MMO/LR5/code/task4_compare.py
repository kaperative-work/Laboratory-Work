import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier

own_train = predict(X_train, my_tree)
own_test = predict(X_test, my_tree)
acc_own_train = accuracy_metric(y_train, own_train)
acc_own_test = accuracy_metric(y_test, own_test)

library_tree = DecisionTreeClassifier(
    criterion="gini",
    max_depth=MAX_DEPTH,
    min_samples_leaf=MIN_SAMPLES_LEAF,
    random_state=RANDOM_STATE,
)
library_tree.fit(X_train, y_train)
lib_train = library_tree.predict(X_train)
lib_test = library_tree.predict(X_test)
acc_lib_train = accuracy_metric(y_train, lib_train)
acc_lib_test = accuracy_metric(y_test, lib_test)

mismatch_train = int(np.sum(own_train != lib_train))
mismatch_test = int(np.sum(own_test != lib_test))
print("Своё дерево, обучение/тест:", round(acc_own_train, 6), round(acc_own_test, 6))
print("sklearn, обучение/тест:", round(acc_lib_train, 6), round(acc_lib_test, 6))
print("Расхождений на обучении:", mismatch_train, "на тесте:", mismatch_test)
print("Глубина sklearn:", library_tree.get_depth(), "листьев:", library_tree.get_n_leaves())

x_min = min(X[:, 0].min(), X_train[:, 0].min()) - 0.4
x_max = max(X[:, 0].max(), X_train[:, 0].max()) + 0.4
y_min = min(X[:, 1].min(), X_train[:, 1].min()) - 0.4
y_max = max(X[:, 1].max(), X_train[:, 1].max()) + 0.4
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250), np.linspace(y_min, y_max, 250))
grid = np.c_[xx.ravel(), yy.ravel()]
own_grid = predict(grid, my_tree).reshape(xx.shape)
lib_grid = library_tree.predict(grid).reshape(xx.shape)
print("Клеток сетки с разным классом:", int(np.sum(own_grid != lib_grid)))

fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2), sharex=True, sharey=True)
for ax, field, title in (
    (axes[0], own_grid, "Своё дерево"),
    (axes[1], lib_grid, "sklearn"),
):
    ax.contourf(xx, yy, field, levels=[-0.1, 0.5, 1.1], colors=["#d6e3f0", "#f8d7b5"], alpha=0.95)
    for label, color in ((0, "#4c78a8"), (1, "#f58518")):
        mask = y_test == label
        ax.scatter(X_test[mask, 0], X_test[mask, 1], c=color, s=26, edgecolors="white", linewidths=0.4)
    ax.set_title(title)
    ax.set_xlabel("Признак 1")
axes[0].set_ylabel("Признак 2")
fig.tight_layout()
fig.savefig(FIG / "img_1.png")
plt.show()

fig, ax = plt.subplots(figsize=(6.2, 4.2))
labels_bar = ["Обучение", "Тест"]
x_pos = np.arange(len(labels_bar))
width = 0.34
ax.bar(x_pos - width / 2, [acc_own_train, acc_own_test], width, label="Своё дерево", color="#4c78a8")
ax.bar(x_pos + width / 2, [acc_lib_train, acc_lib_test], width, label="sklearn", color="#f58518")
ax.set_xticks(x_pos, labels_bar)
ax.set_ylim(0, 1.05)
ax.set_ylabel("Доля верных ответов")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "img_2.png")
plt.show()
