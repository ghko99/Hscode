from transformers import AutoTokenizer, AutoModel
from sentence_transformers import util
import torch
import torch.nn.functional as F
import pickle
import json
import numpy as np
import time

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def hscode_recommend(model,tokenizer, input):
    
    with open('./data/emb.pickle' , 'rb') as f:
        hscode = pickle.load(f) # [hscode, english, korean ,embedding]
    f.close()
    
    encoded_input = tokenizer(input , padding=True,truncation=True,return_tensors='pt')

    with torch.no_grad():
        output = model(input_ids = encoded_input.input_ids.cuda(), attention_mask = encoded_input.attention_mask.cuda())

    input_embedding = mean_pooling(output,encoded_input['attention_mask'].cuda())
    input_embedding = F.normalize(input_embedding, p=2,dim=1)

    embeddings = []
    names = []
    for values in hscode.values():
        embeddings.append(values[3])
        names.append(values[0])

    names = np.array(names)
    embeddings = torch.tensor(embeddings).cuda()

    cos_sim = util.cos_sim(input_embedding[0], embeddings)
    sorted_idx = torch.argsort(cos_sim,descending=True)
    recommend = names[sorted_idx.tolist()[0][:]]
    result = np.unique(recommend, return_index=True)[1]
    result = np.sort(result)
    return recommend[result][:10]
    

if __name__ == '__main__':

    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2').cuda()
    
    with open('./data/hscode.pickle','r') as f:
        hscode_dict = json.load(f)
    f.close()

    while True:
        user_input = input('user input: ')
        if user_input == 'exit':
            break
        prev = time.time()
        recommended = hscode_recommend(model,tokenizer,user_input)
        for name in recommended:
            print('hscode: ', name)
            names = hscode_dict[name]
            print('korean: ', names[0])
            print('english: ', names[1])
            print('-'*100)
    
