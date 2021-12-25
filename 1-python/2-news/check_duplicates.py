import jsonlines
import pandas as pd
import json
import os
def to_json2(df,orient='records'):
    df_json = df.to_json(orient = orient, force_ascii = False)
    return json.loads(df_json)

df = pd.read_json('news.json',lines=True)
n0 = df.shape[0]
df.drop_duplicates(inplace=True)
n1 = df.shape[0]
print('Remove %s duplicate records...'%(n1-n0))
data = to_json2(df)
os.remove('news.json')
with jsonlines.open('news.json', 'w') as writer:
    writer.write_all(data)
