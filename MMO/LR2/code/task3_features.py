df_feat = df_clean.copy()
company = df_feat["CarName"].str.split().str[0].str.lower()
fixes = {
    "maxda": "mazda",
    "porcshce": "porsche",
    "toyouta": "toyota",
    "vokswagen": "volkswagen",
    "vw": "volkswagen",
}
df_feat["company"] = company.replace(fixes)
df_feat["power_to_weight"] = df_feat["horsepower"] / df_feat["curbweight"]
df_feat["avg_mpg"] = (df_feat["citympg"] + df_feat["highwaympg"]) / 2
df_feat[["CarName", "company", "power_to_weight", "avg_mpg"]].head()

df_enc = df_feat.copy()
df_enc["doornumber_bin"] = (df_enc["doornumber"] == "four").astype(int)
df_enc["fuel_diesel"] = (df_enc["fueltype"] == "diesel").astype(int)
df_enc["turbo"] = (df_enc["aspiration"] == "turbo").astype(int)
df_enc["engine_rear"] = (df_enc["enginelocation"] == "rear").astype(int)

cyl_map = {
    "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "eight": 8, "twelve": 12,
}
df_enc["cylinders"] = df_enc["cylindernumber"].map(cyl_map)

ohe_cols = ["carbody", "drivewheel", "enginetype", "fuelsystem", "company"]
df_ohe = pd.get_dummies(df_enc, columns=ohe_cols, drop_first=True, dtype=int)
df_ohe = df_ohe.drop(columns=["CarName", "doornumber", "fueltype", "aspiration", "enginelocation", "cylindernumber"])
print("Размер после кодирования:", df_ohe.shape)
df_ohe.head()
