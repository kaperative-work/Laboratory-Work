binary_prefixes = ("doornumber_bin", "fuel_diesel", "turbo", "engine_rear")
scale_cols = []
for col in df_ohe.columns:
    if col == "car_ID" or col == "price":
        continue
    if not pd.api.types.is_numeric_dtype(df_ohe[col]):
        continue
    if col in binary_prefixes or df_ohe[col].dropna().isin([0, 1]).all():
        continue
    scale_cols.append(col)

train_size = int(len(df_ohe) * 0.8)
train = df_ohe.iloc[:train_size]
print("Обучающих строк:", train_size, "проверочных:", len(df_ohe) - train_size)

df_minmax = df_ohe.copy()
df_std = df_ohe.copy()
for col in scale_cols:
    series = df_ohe[col].astype(float)
    train_series = train[col].astype(float)
    xmin = train_series.min()
    xmax = train_series.max()
    if xmax == xmin:
        df_minmax[col] = 0.0
    else:
        df_minmax[col] = (series - xmin) / (xmax - xmin)
    mu = train_series.mean()
    sigma = train_series.std(ddof=0)
    if sigma == 0:
        df_std[col] = 0.0
    else:
        df_std[col] = (series - mu) / sigma

print("Min-max, минимум и максимум обучающей части:")
print(df_minmax.iloc[:train_size][scale_cols[:6]].agg(["min", "max"]).T)
train_z = df_std.iloc[:train_size][scale_cols[:6]]
print("\nZ-score, среднее и СКО обучающей части:")
print(pd.DataFrame({"mean": train_z.mean(), "std": train_z.std(ddof=0)}))
