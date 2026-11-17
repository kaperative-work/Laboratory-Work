from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

features = ["age", "ed", "employ", "address", "income", "debtinc", "creddebt", "othdebt"]
target = "default"
X = df[features]
y = df[target]
print("Целевая переменная:", target, "— 1, если заёмщик допустил просрочку")
print("Признаки:", features)
print("Матрица признаков:", X.shape, "—", X.shape[0], "объектов и", X.shape[1], "признаков")
print("Образование ed оставлено числом: уровни 1–5 упорядочены, отдельных строковых категорий нет.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=True, random_state=26, stratify=y
)
print("Обучение:", X_train.shape[0], "тест:", X_test.shape[0])
print(
    "Доля класса 1, обучение:", round(float(y_train.mean()), 4),
    "тест:", round(float(y_test.mean()), 4),
)
print("База большинства на тесте, accuracy:", round(float(1 - y_test.mean()), 4))

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
print("Средние стандартизированного обучения:", np.round(X_train_s.mean(axis=0), 6))
print("СКО стандартизированного обучения:", np.round(X_train_s.std(axis=0), 6))
print("Среднее и СКО взяты только с обучения и применены к тесту.")
print("Дерево получит те же признаки без стандартизации: порог в узле не зависит от масштаба столбца.")
