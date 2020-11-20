import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import logging
import random

import torch
from transformers import AdamW
from torch.utils.data import dataloader

import torch.nn as nn
from torch.utils.data import Dataset # 데이터로더
from torch.nn import CrossEntropyLoss, MSELoss

from kobert_transformers import get_tokenizer

from transformers import BertPreTrainedModel
from kobert_transformers import get_kobert_model, get_distilkobert_model

from transformers.configuration_utils import PretrainedConfig
from transformers import BertModel, BertConfig, GPT2Config

logger = logging.getLogger(__name__)

#KoBERT
kobert_config = {
    'attention_probs_dropout_prob': 0.1,
    'hidden_act': 'gelu',
    'hidden_dropout_prob': 0.1,
    'hidden_size': 768,
    'initializer_range': 0.02,
    'intermediate_size': 3072,
    'max_position_embeddings': 512,
    'num_attention_heads': 12,
    'num_hidden_layers': 12,
    'type_vocab_size': 2,
    'vocab_size': 8002
}

def get_kobert_config():
    return BertConfig.from_dict(kobert_config)

class KoBERTforSequenceClassfication(BertPreTrainedModel):
    def __init__(self,
                num_labels = 201,
                hidden_size = 768,
                hidden_dropout_prob = 0.1,
               ):
        super().__init__(get_kobert_config())

        self.num_labels = num_labels
        self.kobert = get_kobert_model()
        self.dropout = nn.Dropout(hidden_dropout_prob)
        self.classifier = nn.Linear(hidden_size, num_labels)
        self.init_weights()

    def forward(
          self,
          input_ids=None,
          attention_mask=None,
          token_type_ids=None,
          position_ids=None,
          head_mask=None,
          inputs_embeds=None,
          labels=None,
  ):
        outputs = self.kobert(
        input_ids,
        attention_mask=attention_mask,
        token_type_ids=token_type_ids,
        position_ids=position_ids,
        head_mask=head_mask,
        inputs_embeds=inputs_embeds,
        )

        pooled_output = outputs[1]

        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)

        outputs = (logits,) + outputs[2:]  # add hidden states and attention if they are here

        if labels is not None:
            if self.num_labels == 1:
                #  We are doing regression
                loss_fct = MSELoss()
                loss = loss_fct(logits.view(-1), labels.view(-1))
            else:
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            outputs = (loss,) + outputs

        return outputs  # (loss), logits, (hidden_states), (attentions)

def kobert_input(tokenizer, str, device = None, max_seq_len = 512):
    index_of_words = tokenizer.encode(str)
    token_type_ids = [0] * len(index_of_words)
    attention_mask = [1] * len(index_of_words)

    # Padding Length
    padding_length = max_seq_len - len(index_of_words)

    # Zero Padding
    index_of_words += [0] * padding_length
    token_type_ids += [0] * padding_length
    attention_mask += [0] * padding_length

    data = {
        'input_ids': torch.tensor([index_of_words]).to(device),
        'token_type_ids': torch.tensor([token_type_ids]).to(device),
        'attention_mask': torch.tensor([attention_mask]).to(device),
    }
    return data

def load_answer():
    category_path = "/Users/kuku/Desktop/Yogiyo/SBA_ML_Final/chatbot/bert_c_most_update.txt"
    answer_path = "/Users/kuku/Desktop/Yogiyo/SBA_ML_Final/chatbot/bert_a_most_update.txt"

    c_f = open(category_path,'r',encoding='utf-8')
    a_f = open(answer_path,'r',encoding='utf-8')

    category_lines = c_f.readlines()
    answer_lines = a_f.readlines()

    category = {}
    answer = {}
    for line_num, line_data in enumerate(category_lines):
        data = line_data.split('\t')
        category[data[1][:-1]]=data[0]

    for line_num, line_data in enumerate(answer_lines):
        data = line_data.split('\t')
        keys = answer.keys()
        if(data[0] in keys):
            answer[data[0]] += [data[1][:-1]]
        else:
            answer[data[0]] =[data[1][:-1]]

    return category, answer

# #############################
# 로딩 init용
save_ckpt_path = "/Users/kuku/Desktop/Yogiyo/SBA_ML_Final/chatbot/kobert-wellnesee-text-classification.pth"

#답변과 카테고리 불러오기
category, answer = load_answer()

ctx = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(ctx)

# 저장한 Checkpoint 불러오기
checkpoint = torch.load(save_ckpt_path, map_location=device)

# device = torch.device('cpu') #load_state_dict (GPU 설정해주기)
model = KoBERTforSequenceClassfication()
model.load_state_dict(checkpoint['model_state_dict']) #모델 저장 & 불러오기
# model.to(device)

model.eval()

tokenizer = get_tokenizer()
# #############################

def process_kobert(text):
  
    data = kobert_input(tokenizer, text, device, 512)
    # print(data)

    output = model(**data)

    logit = output
    softmax_logit = nn.Softmax(logit).dim
    softmax_logit = softmax_logit[0].squeeze()

    max_index = torch.argmax(softmax_logit).item()
    max_index_value = softmax_logit[torch.argmax(softmax_logit)].item()

    answer_list = answer[category[str(max_index)]]
    
    full_intent = category[str(max_index)]
    print('전체 의도: ', full_intent)
    answer_len= len(answer_list)-1
    answer_index = random.randint(0,answer_len)
    print(f'Answer: {answer_list[answer_index]}, index: {max_index}, value: {max_index_value}')

    # full_intent에서 intent 파싱 (ex: 오늘메뉴추천요구 > 추천)
    intent = ''
    cat =''
    if '인사' in full_intent:
        intent = '인사'
        cat = '인사'
    elif '추천' in full_intent:
        intent = '추천'
        cat = full_intent[:full_intent.find('메뉴')]
    elif '주문' in full_intent:
        intent = '주문'
        cat = '주문'
    return intent, cat



if __name__ == "__main__":
    save_ckpt_path = "./chatbot/kobert-wellnesee-text-classification.pth"

    #답변과 카테고리 불러오기
    category, answer = load_answer()

    ctx = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(ctx)

    # 저장한 Checkpoint 불러오기
    checkpoint = torch.load(save_ckpt_path, map_location=device)

    # device = torch.device('cpu') #load_state_dict (GPU 설정해주기)
    model = KoBERTforSequenceClassfication()
    model.load_state_dict(checkpoint['model_state_dict']) #모델 저장 & 불러오기
    # model.to(device)

    model.eval()

    tokenizer = get_tokenizer()

    while 1:
        sent = input('\nQuestion: ')
        data = kobert_input(tokenizer, sent, device, 512)
        # print(data)

        output = model(**data)

        logit = output
        softmax_logit = nn.Softmax(logit).dim
        softmax_logit = softmax_logit[0].squeeze()

        max_index = torch.argmax(softmax_logit).item()
        max_index_value = softmax_logit[torch.argmax(softmax_logit)].item()

        answer_list = answer[category[str(max_index)]]
        print(category[str(max_index)])
        answer_len= len(answer_list)-1
        answer_index = random.randint(0,answer_len)
        print(f'Answer: {answer_list[answer_index]}, index: {max_index}, value: {max_index_value}')
        print('-'*50)
    # print('argmin:',softmax_logit[torch.argmin(softmax_logit)])