import numpy as np
from bs4 import BeautifulSoup
import re
import pandas as pd
import konlpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle
from sklearn.naive_bayes import MultinomialNB
from eunjeon import Mecab
# from dataCreate import dataCreate

mecab = Mecab()
kkma = konlpy.tag.Kkma()

##########데이터 로드
chatbot_data = pd.read_csv('C:/Users/user/Desktop/chat/chatbot/NLP/running.csv')
data = list(chatbot_data['data'])
label = list(chatbot_data['label'])
print(data)

x_data = np.array(
    data
    # #추천
    # '근처 피자 추천해줘',
    # '우리 동네 초밥집 추천해줘',
    # '짬뽕 맛있는곳 어디야',
    # '돈까스 먹고싶다',
    # '햄버거 맛있는곳 알려줘',
    # '괜찮은 일식집 알려줘',
    # '보쌈집 추천해줘',
    # '오늘 뭐 먹을까',
    # '오늘 뭐 먹지',
    # '점심 뭐 먹을까',
    # '점심 뭐 먹지',
    # '저녁에 뭐 먹을까',
    # '저녁에 뭐 먹지',
    # '아침으로 먹을만 한거 추천해줘',
    # '내일 점심에 뭐 먹을까',

    # #주문
    # '판교에 치킨 주문해줘',
    # '피자 세트로 할래',
    # '이걸로 시켜줘',
    # '초밥 시켜줘',
    # '아이스아메리카노 시켜줘',
    # '그걸로 주문해줘',
    # '지금 주문해줘',
    # '피자치킨 세트 주문해',
    # '치킨 시켜줘',

  
)

# y_data = np.array([0,0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
y_data = np.array(label)

labels = ['추천', '주문', '인사', '언제']

##########데이터 분석

##########데이터 전처리

# 텍스트 정제 (HTML 태그 제거)
for i, text in enumerate(x_data):
    text = BeautifulSoup(text, 'html.parser').text 
    #print(text) #스토리가 진짜 너무 노잼
    x_data[i] = text
print(x_data) 

# 텍스트 정제 (특수기호 제거)
for i, text in enumerate(x_data):
    text = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', text) #특수기호 제거, 정규 표현식
    #print(document) stale and uninspired
    x_data[i] = text

#텍스트 정제 (어간 추출)
for i, text in enumerate(x_data):
    # okt = konlpy.tag.Okt()
    clean_words = mecab.nouns(text) 
    print(clean_words) #['스토리', '진짜', '노잼']
    text = ' '.join(clean_words)
    print(text) #스토리 진짜 노잼
    x_data[i] = text
print(x_data) 

#단어 카운트 (가중치 부여)
transformer = TfidfVectorizer()
transformer.fit(x_data)
#print(transformer.get_feature_names()) #['계약', '기간', '등록', '무료', '배송', '백화점', '보고', '상황', '선물', '소식', '신제품', '오늘', '인기', '일정', '제품', '진행', '쿠폰', '파격', '프로젝트', '한정', '할인', '확인', '회의']
#print(vectorizer.vocabulary_) #{'신제품': 10, '소식': 9, '쿠폰': 16, '선물': 8, '무료': 3, '배송': 4, '백화점': 5, '파격': 17, '오늘': 11, '할인': 20, '인기': 12, '제품': 14, '기간': 1, '한정': 19, '일정': 13, '확인': 21, '프로젝트': 18, '진행': 15, '상황': 7, '보고': 6, '계약': 0, '회의': 22, '등록': 2}
x_data = transformer.transform(x_data)
print(x_data.shape) #(10, 23)
#print(x_data)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=777, stratify=y_data)

# with open('model/user_intent_classification_model_transformer.pkl', 'wb') as f:
#     pickle.dump(transformer, f)

##########모델 생성

model = MultinomialNB(alpha=1.0)

##########모델 학습

model.fit(x_train, y_train)

##########모델 검증

# print(model.score(x_train, y_train)) #1.0

# print(model.score(x_test, y_test)) #1.0

# with open('model/user_intent_classification_model.pkl', 'wb') as f:
#     pickle.dump(model, f)

##########모델 예측


def chat(text):

    dict_entity = {
    'active' : ['추천','가격','얼마','메뉴','찾아'],
    'order' : ['주문','배달','시켜'],
    'menu' : ['피자','햄버거','짜장면','짬뽕','치킨','돈까스','초밥','일식','양식','스파게티','밥','보쌈','한식','프렌차이즈','김밥','떡볶이','족발','분식','디저트','야식','한식','중식','커피','삼계탕','찌개','냉면','찜닭'],
    'loc' : ['근처','동네','강남','집','회사','신사','논현','압구정','청담','삼성','대치','역삼','도곡','개포','일원','수서','세곡'],
    'date' : ['오늘','내일','모래','점심','저녁','아침']
    }

    get_data_list = [text][0]


    morpphed_text = kkma.pos(get_data_list)
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
        clean_words = mecab.nouns(text) 
        print('clean_words',clean_words) 
        text = ' '.join(clean_words)
        print('text',text) 
        x_data[i] = text
    print('2',x_data) 
    
    x_data = transformer.transform(x_data)
    # print(x_data.shape) #(10, 23)
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

    else:
        response = 'none'
    return response

    
#     if text == '추천':
#         response = word + ' 추천해 드릴께요'

#     elif text == '인사':
#         response = 'aa 님 안녕하세요'

#     elif text == '주문':
#         response = word+ ' 주문해 드릴께요'

#     elif text == '언제':
#         response = word+ '이런 메뉴는 어떠세요?'

#     else:
#         response = '무슨 말인지 이해 못했습니다'
#     return response

# print('챗봇')
# print('챗봇과 대화를 합니다.')
# print('안녕하세요')

# while True:
#     text = input('나: ')
#     if text == 'quit':
#         break

#     print('챗봇:', chat(text))



# x_data = np.array([
#     '동네 중국집 알려줘'
# ])

# #텍스트 정제 (HTML 태그 제거)
# for i, text in enumerate(x_data):
#     text = BeautifulSoup(text, 'html.parser').text 
#     #print(text) #스토리가 진짜 너무 노잼
#     x_data[i] = text
# print(x_data) 

# #텍스트 정제 (어간 추출)
# for i, text in enumerate(x_data):
#     okt = konlpy.tag.Okt()
#     clean_words = okt.nouns(text) 
#     print(clean_words) #['스토리', '진짜', '노잼']
#     text = ' '.join(clean_words)
#     print(text) #스토리 진짜 노잼
#     x_data[i] = text
# print(x_data) 

#단어 카운트 (가중치 부여)
#transformer = TfidfVectorizer()
#transformer.fit(x_data)
#print(transformer.get_feature_names()) #['계약', '기간', '등록', '무료', '배송', '백화점', '보고', '상황', '선물', '소식', '신제품', '오늘', '인기', '일정', '제품', '진행', '쿠폰', '파격', '프로젝트', '한정', '할인', '확인', '회의']
#print(vectorizer.vocabulary_) #{'신제품': 10, '소식': 9, '쿠폰': 16, '선물': 8, '무료': 3, '배송': 4, '백화점': 5, '파격': 17, '오늘': 11, '할인': 20, '인기': 12, '제품': 14, '기간': 1, '한정': 19, '일정': 13, '확인': 21, '프로젝트': 18, '진행': 15, '상황': 7, '보고': 6, '계약': 0, '회의': 22, '등록': 2}
# x_data = transformer.transform(x_data)
# print(x_data.shape) #(10, 23)
# print(x_data)

#print(x_data.toarray())

# print(x_data)
# y_predict = model.predict(x_data)
# print(y_predict) #[0]
# print(labels[y_predict[0]]) #ham



# if __name__ == '__main__':
#     chat()