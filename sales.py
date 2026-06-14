import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'MS Gothic'

# CSVを読み込む
df = pd.read_csv("sales.csv")

# 各月の合計を計算して新しい列に追加
df["合計"] = df[["商品A", "商品B", "商品C"]].sum(axis=1)

# 各月の合計を表示
for i, row in df.iterrows():
    print(f'{row["月"]}の合計: {row["合計"]}')

# グラフを表示
df.plot(x="月", y=["商品A", "商品B", "商品C"], kind="bar")
plt.title("月別売上グラフ")
plt.ylabel("売上")
plt.show()