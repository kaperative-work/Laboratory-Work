from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

candidates = [
    Path("../data/LR2/CarPrice_Assignment.csv"),
    Path("data/LR2/CarPrice_Assignment.csv"),
]
DATA_PATH = next(path for path in candidates if path.exists())
df = pd.read_csv(DATA_PATH)
print("Файл:", DATA_PATH)
print("Строк:", df.shape[0], "столбцов:", df.shape[1])
df.head()

df.info()
df.describe().T
