# News_head Line project

## what the final looks like
  - next step is to write parse function for input
  - a log table of how many runs has been done in a particular date


```


import pandas as pd
    ...: import json
    ...:
    ...: def to_json1(df,orient='split'):
    ...:     return df.to_json(orient = orient, force_ascii = False)
    ...:
    ...: def to_json2(df,orient='records'):
    ...:     df_json = df.to_json(orient = orient, force_ascii = False)
    ...:     return json.loads(df_json)
    ...:
    ...: json1 = to_json1(df)
    ...: json2 = to_json2(df)
```
