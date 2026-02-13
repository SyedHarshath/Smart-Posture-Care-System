import pandas as pd
df_good = pd.read_csv("posture_data_new_good.csv")
df_bad = pd.read_csv("posture_data_new_bad.csv")
df_all = pd.concat([df_good, df_bad], ignore_index=True)
df_all.to_csv("posture_new_data.csv", index=False)
