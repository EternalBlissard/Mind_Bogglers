import pandas as pd
df = pd.read_csv("templates\\RatingsUpdated.csv")
print(df.loc[0])
df_new = df.loc[184926:]
df_new.to_csv("templates\\Ratings2.csv", index=False)
