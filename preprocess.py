import pandas as pd
import re

file = pd.read_csv('./data/dataset.csv',encoding='utf-8-sig')
file['name'] =  [re.sub('[^A-Za-z0-9가-힣; ()]', '', str(s)) for s in file['name']]

file.to_csv('./data/dataset.csv',encoding='utf-8-sig',index=False)