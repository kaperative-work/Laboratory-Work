from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def scores_of(model, sample):
    if isinstance(model, SVC):
        return model.decision_function(sample)
    return model.predict_proba(sample)[:, 1]


def evaluate(name, model, train_x, test_x):
    model.fit(train_x, y_train)
    pred_train = model.predict(train_x)
    pred_test = model.predict(test_x)
    score = scores_of(model, test_x)
    row = {
        "model": name,
        "acc_train": accuracy_score(y_train, pred_train),
        "acc_test": accuracy_score(y_test, pred_test),
        "precision": precision_score(y_test, pred_test, zero_division=0),
        "recall": recall_score(y_test, pred_test, zero_division=0),
        "f1": f1_score(y_test, pred_test, zero_division=0),
        "roc_auc": roc_auc_score(y_test, score),
    }
    return model, pred_test, score, row


specs = [
    (
        "Логистическая регрессия",
        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=26),
        X_train_s,
        X_test_s,
    ),
    (
        "SVM, ядро RBF",
        SVC(kernel="rbf", class_weight="balanced", random_state=26),
        X_train_s,
        X_test_s,
    ),
    (
        "CART",
        DecisionTreeClassifier(max_depth=4, min_samples_leaf=15, class_weight="balanced", random_state=26),
        X_train,
        X_test,
    ),
]

models = {}
preds = {}
score_map = {}
rows = []
for name, model, train_x, test_x in specs:
    model, pred, score, row = evaluate(name, model, train_x, test_x)
    models[name] = model
    preds[name] = pred
    score_map[name] = score
    rows.append(row)

deep = DecisionTreeClassifier(max_depth=None, min_samples_leaf=1, random_state=26)
_, _, _, deep_row = evaluate("CART без ограничения глубины", deep, X_train, X_test)
rows.append(deep_row)

table = pd.DataFrame(rows)
print(table.round(4).to_string(index=False))
print()
for name in models:
    matrix = confusion_matrix(y_test, preds[name])
    tn, fp, fn, tp = matrix.ravel()
    print(f"{name}: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.6))
for ax, name in zip(axes, models):
    ConfusionMatrixDisplay(confusion_matrix(y_test, preds[name]), display_labels=["0", "1"]).plot(
        ax=ax, colorbar=False
    )
    ax.set_title(name)
fig.tight_layout()
fig.savefig(FIG / "img_4.png", bbox_inches="tight")
plt.show()

metric_keys = ["precision", "recall", "f1", "roc_auc"]
metric_labels = ["Точность", "Полнота", "F1", "ROC-AUC"]
fig, ax = plt.subplots(figsize=(8.2, 4.2))
positions = np.arange(len(metric_keys))
width = 0.25
for i, name in enumerate(models):
    values = [next(row[key] for row in rows if row["model"] == name) for key in metric_keys]
    ax.bar(positions + (i - 1) * width, values, width, label=name)
ax.set_xticks(positions, metric_labels)
ax.set_ylim(0, 1)
ax.set_ylabel("Значение на тесте")
ax.set_title("Качество трёх моделей на тестовой выборке")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "img_5.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(6.4, 4.6))
for name in models:
    fpr, tpr, _ = roc_curve(y_test, score_map[name])
    auc = next(row["roc_auc"] for row in rows if row["model"] == name)
    ax.plot(fpr, tpr, label=f"{name}, AUC = {auc:.3f}")
ax.plot([0, 1], [0, 1], ls="--", color="gray", label="случайный классификатор")
ax.set_xlabel("Доля ложных срабатываний")
ax.set_ylabel("Полнота")
ax.set_title("ROC-кривые на тестовой выборке")
ax.legend()
fig.tight_layout()
fig.savefig(FIG / "img_6.png", bbox_inches="tight")
plt.show()

tree = models["CART"]
importance = pd.Series(tree.feature_importances_, index=features).sort_values()
coef = pd.Series(models["Логистическая регрессия"].coef_.ravel(), index=features).sort_values()
print()
print("Важность признаков CART:")
print(importance.round(4).to_string())
print("Коэффициенты логистической регрессии:")
print(coef.round(4).to_string())

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].barh(importance.index.astype(str), importance.values, color="steelblue")
axes[0].set_title("Важность признаков CART")
axes[0].set_xlabel("Вклад в уменьшение неоднородности")
axes[1].barh(coef.index.astype(str), coef.values, color="darkorange")
axes[1].axvline(0, color="black", lw=0.8)
axes[1].set_title("Коэффициенты логистической регрессии")
axes[1].set_xlabel("Вес стандартизированного признака")
fig.tight_layout()
fig.savefig(FIG / "img_7.png", bbox_inches="tight")
plt.show()
