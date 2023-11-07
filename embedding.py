import pandas as pd
import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import pickle

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def embedding(model,tokenizer,name_list):
    tmp_ix = 0
    batch = 500
    embeddings = []
    while tmp_ix < len(name_list):
        encoded_input = tokenizer(name_list[tmp_ix:min(tmp_ix+500,len(name_list))], padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(input_ids = encoded_input.input_ids.cuda(), attention_mask = encoded_input.attention_mask.cuda())

        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'].cuda())
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        tmp_ix += batch
        embeddings.extend(sentence_embeddings)
        print(tmp_ix)
    return embeddings

def df_to_dataset(data):
    dataset = []
    name_for_embeddings = []
    dataset_hscode = data['hscode'].to_list()
    dataset_eng = data['english'].to_list()
    dataset_kor = data['korean'].to_list()
    for i in range(len(dataset_hscode)):
        code = str(dataset_hscode[i])
        if len(code) == 9:
            code = '0' + code
        name_for_embeddings.append(str(dataset_eng[i]))
        dataset.append([code,str(dataset_eng[i]),str(dataset_kor[i])])
    return dataset, name_for_embeddings

def dataset_to_pickle(dataset, name_for_embeddings, model, tokenizer):
    embedding_list = embedding(model,tokenizer,name_for_embeddings)
    emb_dict = dict()
    for i in tqdm(range(len(embedding_list))):
        emb_dict[i] = [dataset[i][0],dataset[i][1],dataset[i][2],embedding_list[i].cpu().numpy().tolist()]
    with open('./data/test_emb.pickle','wb') as f:
        pickle.dump(emb_dict,f)
    f.close()


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2').cuda()

    data = pd.read_csv('./data/test.csv',encoding='utf-8-sig')
    dataset, name_for_embeddings = df_to_dataset(data)
    dataset_to_pickle(dataset,name_for_embeddings,model,tokenizer)

