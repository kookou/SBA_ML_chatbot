import pandas as pd
import numpy as np
import matplotlib as mpl
from konlpy.tag import Kkma
from konlpy.utils import pprint

import csv
from konlpy.tag import Okt
from gensim.models import word2vec

#네이버 영화 코퍼스를 읽는다.
f = open('C:/Users/user/Desktop/chat/chatbot/NLP/ratings_train.txt', 'r', encoding='utf-8')
rdr = csv.reader(f, delimiter='\t')
rdw = list(rdr)
# print("Id=%s : Name=%s" % (r[0][0], r[0][1]))
# print("Id=%s : Name=%s" % (r[1][0], r[1][1]))
# print("Id=%s : Name=%s" % (r[2][0], r[2][1]))

f.close()
 

#트위터 형태소 분석기를 로드한다. Twiter가 KoNLPy v0.4.5 부터 Okt로 변경 되었다.
twitter = Okt()

 #텍스트를 한줄씩 처리합니다.
result = []
for line in rdw:
    #형태소 분석하기, 단어 기본형 사용
    malist = twitter.pos( line[1], norm=True, stem=True)
    r = []
    for word in malist:
        #Josa”, “Eomi”, “'Punctuation” 는 제외하고 처리
        if not word[1] in ["Josa","Eomi","Punctuation"]:
            r.append(word[0])
    #형태소 사이에 공백 " "  을 넣습니다. 그리고 양쪽 공백을 지웁니다.
    rl = (" ".join(r)).strip()
    result.append(rl)
    #print(rl)

#형태소들을 별도의 파일로 저장 합니다.
with open("NaverMovie.nlp",'w', encoding='utf-8') as fp:
    fp.write("\n".join(result))

#Word2Vec 모델 만들기
wData = word2vec.LineSentence("NaverMovie.nlp")
wModel =word2vec.Word2Vec(wData, size=200, window=10, hs=1, min_count=2, sg=1)
wModel.save("NaverMovie.model")
print("Word2Vec Modeling finished")




# kkma = Kkma()
# pprint(kkma.nouns(u'명사만을 추출하여 워드클라우드를 그려봅니다'))

# rain_data_order = ['판교에 오늘 피자 주문해줘']
# train_data_reserve = ['오늘 날짜에 호텔 예약 해줄레']
# train_data_info = ['모래 날짜의 판교 여행 정보 알려줘']

# get_data_list = train_data_info[0]

# dict_entity = {
#     'date' : ['오늘','내일','모래'],
#     'loc' : ['판교','야탑'],
#     'menu' : ['피자','햄버거'],
#     'hotel' : ['호텔','여관','민박'],
#     'travel' : ['여행','관광','카페']
# }

# length = 1
# for key in list(dict_entity.keys()):
#     length = length * len(dict_entity[key])
# print("Augmentation length is {0}".format(length))


# mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
# morpphed_text = mecab.pos(get_data_list)
# print(morpphed_text)