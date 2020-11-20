from eunjeon import Mecab
import re
import konlpy
import numpy as np
import pandas as pd
import pickle
import tensorflow as tf


mecab = Mecab()

train_data_order = ['판교에 오늘 피자 주문해줘']
train_data_reserve = ['오늘 날짜에 호텔 예약 해줄레']
train_data_info = ['모래 날짜의 판교 여행 정보 알려줘']

get_data_list = train_data_info[0]

dict_entity = {
    'date' : ['오늘','내일','모래'],
    'loc' : ['판교','야탑'],
    'menu' : ['피자','햄버거'],
    'hotel' : ['호텔','여관','민박'],
    'travel' : ['여행','관광','카페']
}

length = 1
for key in list(dict_entity.keys()):
    length = length * len(dict_entity[key])
print("Augmentation length is {0}".format(length))

morpphed_text = mecab.pos(get_data_list)
print(morpphed_text)