# chatgpt
## demo
```python
import pandas as pd

data = {
    'region': ['Asia', 'Asia', 'Asia', 'North America', 'North America', 'Europe', 'Europe'],
    'az': ['a', 'a', 'b', 'c', 'd', 'e', 'f'],
    'cpu': [10, 8, 16, 16, 32, 8, 16],
    'name': ['machine10', 'machine1', 'machine2', 'machine3', 'machine4', 'machine5', 'machine6']
}

df = pd.DataFrame(data)

df_sorted = df.sort_values('cpu', ascending=False)

df_unique = df_sorted.drop_duplicates(subset=['region', 'az'], keep='first')

print(df_unique)
```