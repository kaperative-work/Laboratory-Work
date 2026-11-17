df = df_raw.dropna(subset=["default"]).copy()
df["default"] = df["default"].astype(int)
print("После удаления строк без метки:", df.shape[0], "строк, столбцов:", df.shape[1])
print("Пропусков в признаках:", int(df.drop(columns="default").isna().sum().sum()))

skewed = ["income", "debtinc", "creddebt", "othdebt"]
print()
print("Хвосты по правилу 1,5·IQR и доля просрочки в них:")
for col in ["age", "employ", "address", *skewed]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    mask = (df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)
    rate = float(df.loc[mask, "default"].mean()) if mask.any() else float("nan")
    print(f"{col:10}  объектов={int(mask.sum()):3}  доля default в хвосте={rate:.3f}")

fig, axes = plt.subplots(2, 4, figsize=(12, 5.6))
for ax, col in zip(axes[0], skewed):
    ax.boxplot(df[col].to_numpy(), tick_labels=[col])
    ax.set_title("до логарифма")
for col in skewed:
    df[col] = np.log1p(df[col])
for ax, col in zip(axes[1], skewed):
    ax.boxplot(df[col].to_numpy(), tick_labels=[col])
    ax.set_title("после log1p")
fig.suptitle("Денежные признаки до и после смягчения логарифмом")
fig.tight_layout()
fig.savefig(FIG / "img_2.png", bbox_inches="tight")
plt.show()

print()
print("Корреляция Пирсона с default после логарифма:")
corr = df.corr(numeric_only=True)["default"].drop("default").sort_values()
print(corr.round(3).to_string())

fig, ax = plt.subplots(figsize=(6.6, 4.2))
colors = ["darkorange" if value > 0 else "steelblue" for value in corr.values]
ax.barh(corr.index.astype(str), corr.values, color=colors)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Корреляция с default")
ax.set_title("Связь признаков с просрочкой")
fig.tight_layout()
fig.savefig(FIG / "img_3.png", bbox_inches="tight")
plt.show()
