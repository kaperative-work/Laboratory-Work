missing = df.isna().sum()
missing_share = missing / len(df)
print(pd.DataFrame({"пропусков": missing, "доля": missing_share.round(3)}))
print("Пропущенных ячеек:", int(missing.sum()))
print("Столбцы, где пусто больше 70%:", missing_share[missing_share > 0.7].index.tolist())

fig, ax = plt.subplots(figsize=(10, 4))
ax.imshow(df.isna().astype(int).values, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)
ax.set_title("Тепловая карта пропусков")
ax.set_xlabel("Столбец")
ax.set_ylabel("Строка")
ax.set_xticks(range(df.shape[1]))
ax.set_xticklabels(df.columns, rotation=90, fontsize=8)
plt.tight_layout()
plt.show()

numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != "car_ID"]
stats = df[numeric_cols].describe().T
stats["median"] = df[numeric_cols].median()
stats["IQR"] = stats["75%"] - stats["25%"]
stats

plot_cols = ["price", "horsepower", "enginesize", "curbweight", "citympg", "highwaympg"]

fig, axes = plt.subplots(2, 3, figsize=(12, 7))
for ax, col in zip(axes.ravel(), plot_cols):
    ax.hist(df[col], bins=20, color="steelblue", edgecolor="white")
    ax.set_title(col)
plt.suptitle("Распределения до обработки")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 3, figsize=(12, 7))
for ax, col in zip(axes.ravel(), plot_cols):
    ax.boxplot(df[col], orientation="vertical")
    ax.set_title(col)
plt.suptitle("BoxPlot до устранения выбросов")
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df["horsepower"], df["price"], alpha=0.7, color="teal")
ax.set_xlabel("horsepower")
ax.set_ylabel("price")
ax.set_title("Связь мощности и цены")
plt.tight_layout()
plt.show()

body_counts = df["carbody"].value_counts()
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(body_counts.index, body_counts.values, color="steelblue")
ax.set_title("Число автомобилей по типу кузова")
ax.set_ylabel("Количество")
plt.tight_layout()
plt.show()

df_clean = df.copy()
empty_cols = df_clean.columns[df_clean.isna().mean() > 0.7]
df_clean = df_clean.drop(columns=empty_cols)
print("Удалены столбцы с пропуском больше 70%:", empty_cols.tolist())

for col in df_clean.columns:
    if df_clean[col].isna().any():
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        else:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode().iloc[0])

def replace_outliers(series):
    values = series.astype(float).copy()
    replaced = 0
    for _ in range(10):
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            break
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        mask = (values < low) | (values > high)
        count = int(mask.sum())
        if count == 0:
            break
        values = values.mask(mask, values.median())
        replaced += count
    return values, replaced

for col in numeric_cols:
    cleaned, replaced = replace_outliers(df_clean[col])
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    print(f"{col}: Q1={q1:.3f}, Q3={q3:.3f}, IQR={iqr:.3f}, заменено медианой {replaced}")
    df_clean[col] = cleaned

print("Строк:", len(df_clean))
print("Пропущенных ячеек после обработки:", int(df_clean.isna().sum().sum()))

fig, ax = plt.subplots(figsize=(10, 3))
ax.imshow(df_clean.isna().astype(int).values, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)
ax.set_title("Тепловая карта пропусков после обработки")
ax.set_xticks(range(df_clean.shape[1]))
ax.set_xticklabels(df_clean.columns, rotation=90, fontsize=8)
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 3, figsize=(12, 7))
for ax, col in zip(axes.ravel(), plot_cols):
    ax.boxplot(df_clean[col], orientation="vertical")
    ax.set_title(col)
plt.suptitle("BoxPlot после замены выбросов медианой")
plt.tight_layout()
plt.show()

left = 0
for col in numeric_cols:
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        continue
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    left += int(((df_clean[col] < low) | (df_clean[col] > high)).sum())
print("Выбросов по правилу 1.5·IQR после обработки:", left)

corr = df_clean[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))
ax.set_xticklabels(numeric_cols, rotation=90, fontsize=8)
ax.set_yticklabels(numeric_cols, fontsize=8)
ax.set_title("Тепловая карта корреляций")
fig.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
