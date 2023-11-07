import pickle
import numpy as np
import torch
from tqdm import tqdm
from sentence_transformers import util

def get_accuracy():
    with open('./data/train_emb.pickle' , 'rb') as f:
        train = pickle.load(f) # [hscode, english, korean ,embedding]
    f.close()
    with open('./data/test_emb.pickle' , 'rb') as f:
        test = pickle.load(f) # [hscode, english, korean ,embedding]
    f.close()


    train_embeddings = []
    train_hscodes = []

    for values in train.values():
        train_embeddings.append(values[3])
        train_hscodes.append(values[0][:])
    
    train_hscodes = np.array(train_hscodes)
    train_embeddings = torch.tensor(train_embeddings).cuda()

    cor = 0
    for values in tqdm(test.values()):
        cos_sim = util.cos_sim(torch.tensor(values[3]).cuda(), train_embeddings)
        sorted_idx = torch.argsort(cos_sim,descending=True)
        recommend = train_hscodes[sorted_idx.tolist()[0][:]]
        result = np.unique(recommend, return_index=True)[1]
        result = np.sort(result)
        top_10 = recommend[result][:10]
        if values[0] in top_10:
            cor += 1
    print('accuracy: ', cor, '/', len(test), ' = ' , cor/(len(test)))

get_accuracy()