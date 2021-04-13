import pandas as pd
fileName='alpha_c.csv'
df = pd.read_csv('./pdf/' + fileName)
print(len(df))
df.drop_duplicates(subset =fileName,keep = "first", inplace = True)
df.to_csv('new.csv')
print(len(df))
