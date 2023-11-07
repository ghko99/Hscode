import pandas as pd
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('./data/dataset.csv',encoding='utf-8-sig')
hscode_dict = dict()

for i in range(1,98):
    hscode_dict[str(i)] = []


for i in range(len(dataset)):
    hscode = str(dataset.iloc[i]['hscode'])
    name = dataset.iloc[i]['name']
    if len(hscode) == 9:
        hscode_dict[hscode[0]].append(name)
    else:
        hscode_dict[hscode[:2]].append(name)

train_dict = dict()
test_dict = dict()
val_dict = dict()
for key, value in hscode_dict.items():
    if len(value) == 0:
        continue
    train, test = train_test_split(value, test_size=0.2, random_state=42)
    
    if len(test) == 1:
        validation = []
    else:
        test, validation =  train_test_split(test,test_size=0.5,random_state=42)

    train_dict[key] = train
    test_dict[key] = test
    val_dict[key] = validation

train_dataset = []
test_dataset = []
valid_dataset = []
for key ,value in train_dict.items():
    trainset = []
    validset = []
    testset = []
    for val in value:
        trainset.append([str(val),int(key)])
    for val in test_dict[key]:
        testset.append([str(val),int(key)])
    for val in val_dict[key]:
        validset.append([str(val),int(key)])
    train_dataset.extend(trainset)
    test_dataset.extend(testset)
    valid_dataset.extend(validset)


df = pd.DataFrame(train_dataset, columns = ['name', 'label'])
df.to_csv('./data/trainset.csv',encoding='utf-8-sig',index=False)
df = pd.DataFrame(test_dataset, columns = ['name', 'label'])
df.to_csv('./data/testset.csv',encoding='utf-8-sig',index=False)
df = pd.DataFrame(valid_dataset, columns = ['name', 'label'])
df.to_csv('./data/validset.csv',encoding='utf-8-sig',index=False)