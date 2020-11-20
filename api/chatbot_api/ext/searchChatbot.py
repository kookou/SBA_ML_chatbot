import numpy as np
from bs4 import BeautifulSoup
import re
import pandas as pd
import konlpy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle
from sklearn.naive_bayes import MultinomialNB
# from eunjeon import Mecab
# from dataCreate import dataCreate

# mecab = Mecab()
# kkma = konlpy.tag.Kkma()
# Okt = konlpy.tag.Okt()
komoran = konlpy.tag.Komoran()

##########데이터 로드
chatbot_data = pd.read_csv('/Users/kuku/Desktop/Yogiyo/SBA_ML_Final/data/NLP_data/running.csv')
data = list(chatbot_data['data'])
label = list(chatbot_data['label'])

x_data = np.array(data)
y_data = np.array(label)

labels = ['추천', '주문', '인사', '언제']




##########데이터 전처리

# 텍스트 정제 (HTML 태그 제거)
for i, text in enumerate(x_data):
    text = BeautifulSoup(text, 'html.parser').text 
    #print(text) #스토리가 진짜 너무 노잼
    x_data[i] = text
# print(x_data) 

# 텍스트 정제 (특수기호 제거)
for i, text in enumerate(x_data):
    text = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', text) #특수기호 제거, 정규 표현식
    #print(document) stale and uninspired
    x_data[i] = text

#텍스트 정제 (어간 추출)
for i, text in enumerate(x_data):
    # okt = konlpy.tag.Okt()
    clean_words = komoran.nouns(text) 
    # print(clean_words) #['스토리', '진짜', '노잼']
    text = ' '.join(clean_words)
    # print(text) #스토리 진짜 노잼
    x_data[i] = text
# print(x_data) 

#단어 카운트 (가중치 부여)
transformer = TfidfVectorizer()
transformer.fit(x_data)
#print(transformer.get_feature_names()) #['계약', '기간', '등록', '무료', '배송', '백화점', '보고', '상황', '선물', '소식', '신제품', '오늘', '인기', '일정', '제품', '진행', '쿠폰', '파격', '프로젝트', '한정', '할인', '확인', '회의']
#print(vectorizer.vocabulary_) #{'신제품': 10, '소식': 9, '쿠폰': 16, '선물': 8, '무료': 3, '배송': 4, '백화점': 5, '파격': 17, '오늘': 11, '할인': 20, '인기': 12, '제품': 14, '기간': 1, '한정': 19, '일정': 13, '확인': 21, '프로젝트': 18, '진행': 15, '상황': 7, '보고': 6, '계약': 0, '회의': 22, '등록': 2}
x_data = transformer.transform(x_data)
# print(x_data.shape) #(10, 23)
#print(x_data)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=777, stratify=y_data)

# with open('model/user_intent_classification_model_transformer.pkl', 'wb') as f:
#     pickle.dump(transformer, f)

##########모델 생성

model = MultinomialNB(alpha=1.0)

##########모델 학습

model.fit(x_train, y_train)
print('============= chatbot 모델 학습 완료 ==============')

##########모델 예측

def process_nb(text):
    
    dict_entity = {
    'active' : ['추천','가격','얼마','메뉴','찾아'],
    'order' : ['주문','배달','시켜'],
    'menu' : ['피자','햄버거','짜장면','짬뽕','치킨','돈까스','초밥','일식','양식','스파게티','밥','보쌈','한식','프렌차이즈','김밥','떡볶이','족발','분식','디저트','야식','한식','중식','커피','삼계탕','찌개','냉면','찜닭'],
    'loc' : ['근처','동네','강남','집','회사','신사','논현','압구정','청담','삼성','대치','역삼','도곡','개포','일원','수서','세곡'],
    'date' : ['오늘','내일','모래','점심','저녁','아침']
    }

    get_data_list = [text][0]


    morpphed_text = komoran.pos(get_data_list)
    print('5',morpphed_text) # [('근처', 'NNG'), ('피자', 'NNG'), ('추천', 'NNG'), ('해', 'XSV+EC'), ('줘', 'VX+EC')]

    tagged_text = ''
    for pos_tags in morpphed_text:
        if (pos_tags[1] in ['NNG','MAG', 'NNP','SL'] and len(pos_tags[0]) > 1): #Check only Noun
            feature_value = pos_tags[0]
            print('7',feature_value)
            tagged_text = tagged_text + pos_tags[0] + ' '

    print('6',tagged_text) #(근처 피자 추천)

    word = tagged_text.split(' ')
    word = word[0]
    print('검색어',word)

    x_data = np.array([ text ])

    for i, text in enumerate(x_data):
        text = BeautifulSoup(text, 'html.parser').text 
        x_data[i] = text
    print('1',x_data) 

    #텍스트 정제 (어간 추출)
    for i, text in enumerate(x_data):
        # okt = konlpy.tag.Okt()
        clean_words = komoran.nouns(text) 
        print('clean_words',clean_words) 
        text = ' '.join(clean_words)
        print('text',text) 
        x_data[i] = text
    print('2',x_data) 
    
    x_data = transformer.transform(x_data)
    print(x_data) #(10, 23)
    y_predict = model.predict(x_data)
    text = labels[y_predict[0]]
    # print('3',y_predict) #[0]
    # print('4',labels[y_predict[0]]) #ham
    
    if text == '추천':
        return text, word

    elif text == '인사':
         return text, word

    elif text == '주문':
        return text, word

    elif text == '언제':
        return text, word

    elif x_data =='':
        text = 'none'
        return text

    print("장난하냐", text)
##########모델 저장

# joblib.dump(model,'chatbot_model.h5')
# print("저장 되었나")
