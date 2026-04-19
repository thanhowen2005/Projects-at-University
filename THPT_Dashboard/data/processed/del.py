import pandas as pd

df = pd.read_csv("data/processed/thpt2020.csv")

df['sbd'] = (
    df['sbd']
    .astype(str)
    .str.strip()
    .str.replace('.0', '', regex=False)
    .str[-7:]   # 👈 lấy 7 số cuối
)

df.to_csv("data/processed/thpt2020.csv", index=False)

print("✅ Clean xong SBD")