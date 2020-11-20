from eunjeon import Mecab
from bs4 import BeautifulSoup
import re
import konlpy
import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
tf.random.set_seed(777) #하이퍼파라미터 튜닝을 위해 실행시 마다 변수가 같은 초기값 가지게 하기

# 데이터 타입
ENCODER_INPUT  = 0
DECODER_INPUT  = 1
DECODER_OUTPUT = 2

# 태그 단어
PADDING = "<PADDING>"   # 패딩
START = "<START>"     # 시작
END = "<END>"       # 끝
OOV = "<OOV>"       # 없는 단어(Out of Vocabulary)

# 한 문장에서 단어 시퀀스의 최대 개수
sequence_length = 30

# 태그 인덱스
PADDING_INDEX = 0
START_INDEX = 1
END_INDEX = 2
OOV_INDEX = 3

def clean_korean_documents_simple_version(documents):
    #텍스트 정제 (HTML 태그 제거)
    for i, document in enumerate(documents):
        document = BeautifulSoup(document, 'html.parser').text 
        #print(document) #스토리가 진짜 너무 노잼
        documents[i] = document

    #텍스트 정제 (특수기호 제거)
    for i, document in enumerate(documents):
        document = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', document) #특수기호 제거, 정규 표현식
        #print(document) stale and uninspired
        documents[i] = document

    #텍스트 정제 (형태소 추출)
    for i, document in enumerate(documents):
        eunjeon = Mecab()
        clean_words = []
        for word in eunjeon.morphs(document): 
            clean_words.append(word)
        #print(clean_words) #['스토리', '진짜', '노잼']
        document = ' '.join(clean_words)
        #print(document) #스토리 진짜 노잼
        documents[i] = document

    return documents

# 문장을 인덱스로 변환
def convert_word_to_index(documents, word_to_index, document_usage): 
    documents_index = []

    # 모든 문장에 대해서 반복
    for document in documents:
        document_index = []

        # 디코더 입력일 경우 맨 앞에 START 태그 추가
        if document_usage == DECODER_INPUT:
            document_index.append(word_to_index[START])

        # 문장의 단어들을 띄어쓰기로 분리
        for word in document.split():
            if word_to_index.get(word) is not None:
                # 사전에 있는 단어면 해당 인덱스를 추가
                document_index.append(word_to_index[word])
            else:
                # 사전에 없는 단어면 OOV 인덱스를 추가
                document_index.append(word_to_index[OOV])

        # 최대 길이 검사
        if document_usage == DECODER_OUTPUT:
            # 디코더 목표일 경우 맨 뒤에 END 태그 추가
            if len(document_index) >= sequence_length:
                document_index = document_index[:sequence_length-1] + [word_to_index[END]]
            else:
                document_index += [word_to_index[END]]
        else:
            if len(document_index) > sequence_length:
                document_index = document_index[:sequence_length]

        # 최대 길이에 없는 공간은 패딩 인덱스로 채움
        document_index += [word_to_index[PADDING]] * (sequence_length - len(document_index))

        # 문장의 인덱스 배열을 추가
        documents_index.append(document_index)

    return np.asarray(documents_index)

# 인덱스를 문장으로 변환
def convert_index_to_word(indexs, index_to_word): 
    document = ''

    # 모든 문장에 대해서 반복
    for index in indexs:
        if index == END_INDEX:
            # 종료 인덱스면 중지
            break;
        if index_to_word.get(index) is not None:
            # 사전에 있는 인덱스면 해당 단어를 추가
            document += index_to_word[index]
        else:
            # 사전에 없는 인덱스면 OOV 단어를 추가
            document += index_to_word[OOV_INDEX]

        # 빈칸 추가
        document += ' '

    return document    

##########데이터 로드

# chatbot_data = pd.read_csv('C:/Users/user/Desktop/chat/chatbot/NLP/FoodACaffeData.csv')
chatbot_data = pd.read_csv('C:/Users/user/Desktop/chat/chatbot/NLP/FoodACaffeData.csv')

##########데이터 분석

##########데이터 전처리

def test (documents):
    #텍스트 정제 (형태소 추출)
    eunjeon = Mecab()
    testdata = eunjeon.pos(documents[0])

    return testdata



question = chatbot_data['question']
answer = chatbot_data['answer']

question = question.to_numpy()
answer = answer.to_numpy()



# question = question[:500] #데이터를 100개로 제한
# answer = answer[:500]

# print(question[:3]) #['12시 땡!', '1지망 학교 떨어졌어']
# print(answer[:3]) #['하루가 또 가네요.', '위로해 드립니다.']

# test = test(answer)
# 형태소분석 수행
question = clean_korean_documents_simple_version(question)
answer = clean_korean_documents_simple_version(answer)
print(question[:3]) #['12시 땡', '1 지망 학교 떨어졌어']
print(answer[:3]) #['하루 가 또 가네요', '위로 해 드립니다']
# print(test[:1])

# 질문과 대답 문장들을 하나로 합침
documents = []
documents.extend(question)
documents.extend(answer)
# 단어들의 배열 생성
words = []
for document in documents:
    for word in document.split():
        words.append(word)
# 길이가 0인 단어는 삭제
words = [word for word in words if len(word) > 0]
# 중복된 단어 삭제
words = list(set(words))
# 제일 앞에 태그 단어 삽입
words = [PADDING, START, END, OOV] + words
print(words[:10]) #['<PADDING>', '<START>', '<END>', '<OOV>', '으로', '아세요', '다음', '모두', '정말', '그런거니']
max_vocabulary = len(words)
# 단어와 인덱스의 딕셔너리 생성
word_to_index = {word: index for index, word in enumerate(words)} #단어 -> 인덱스, 문장을 인덱스로 변환하여 모델 입력으로 사용
index_to_word = {index: word for index, word in enumerate(words)} #인덱스 -> 단어, 모델의 예측 결과인 인덱스를 문장으로 변환시 사용

# 인코더 입력 인덱스 변환
x_encoder = convert_word_to_index(question, word_to_index, ENCODER_INPUT)
print(x_encoder[:3]) 

# 디코더 입력 인덱스 변환 (START ~)
x_decoder = convert_word_to_index(answer, word_to_index, DECODER_INPUT)
print(x_decoder[:3]) 

# 디코더 목표 인덱스 변환 (~ END)
y_decoder = convert_word_to_index(answer, word_to_index, DECODER_OUTPUT)
print(y_decoder[:3]) 

#원핫 인코딩
y_decoder = tf.keras.utils.to_categorical(y_decoder, max_vocabulary)

##########모델 생성

encoder_input = tf.keras.layers.Input(shape=(None,)) #입력 문장의 인덱스 시퀀스를 입력으로 받음
net = tf.keras.layers.Embedding(input_dim=max_vocabulary, output_dim=100)(encoder_input)
net, state_h, state_c = tf.keras.layers.LSTM(units=128, return_sequences=True, return_state=True)(net)
#net, state_h, state_c = tf.keras.layers.LSTM(units=128, return_sequences=True, return_state=True, dropout=0.1, recurrent_dropout=0.5)(net)

decoder_input = tf.keras.layers.Input(shape=(None,)) #목표 문장의 인덱스 시퀀스를 입력으로 받음
net = tf.keras.layers.Embedding(input_dim=max_vocabulary, output_dim=100)(decoder_input)
net, state_h, state_c = tf.keras.layers.LSTM(units=128, return_sequences=True, return_state=True)(net, initial_state=[state_h, state_c]) #initial_state를 인코더의 상태로 초기화
#net, state_h, state_c = tf.keras.layers.LSTM(units=128, return_sequences=True, return_state=True, dropout=0.1, recurrent_dropout=0.5)(net, initial_state=[state_h, state_c]) #initial_state를 인코더의 상태로 초기화
net = tf.keras.layers.Dense(units=max_vocabulary, activation='softmax')(net) #단어의 개수만큼 노드의 개수를 설정해 원핫 형식으로 각 단어 인덱스를 출력
model = tf.keras.models.Model([encoder_input, decoder_input], net)

model.summary()


#인코더
encoder_input = model.input[0]
net = model.layers[2](encoder_input)
net, state_h, state_c = model.layers[4](net)
encoder_model = tf.keras.models.Model(encoder_input, [state_h, state_c])

encoder_model.summary()

#디코더
decoder_input = tf.keras.layers.Input(shape=(None,))
state_h_input = tf.keras.layers.Input(shape=(128,))
state_c_input = tf.keras.layers.Input(shape=(128,))   
net = model.layers[-4](decoder_input)
net, state_h, state_c = model.layers[-2](net, initial_state=[state_h_input, state_c_input])
net = model.layers[-1](net)
decoder_model = tf.keras.models.Model([decoder_input, state_h_input, state_c_input], [net, state_h, state_c])

decoder_model.summary()


##########모델 학습 및 검증

#내장 루프
def on_epoch_end(epoch, logs):
    x_encoder = [
        '아이스아메리카노 하나요'
    ]

    x_encoder = clean_korean_documents_simple_version(x_encoder)
    x_encoder = convert_word_to_index(x_encoder, word_to_index, ENCODER_INPUT)
    print(x_encoder) #
    print(len(x_encoder[0])) #

    x_decoder = [
        '테이크아웃하실 건가요?'
    ]

    x_decoder = clean_korean_documents_simple_version(x_decoder)
    x_decoder = convert_word_to_index(x_decoder, word_to_index, DECODER_INPUT)
    print(x_decoder) #
    print(len(x_decoder[0])) #

    y_predict = model([x_encoder, x_decoder]).numpy()
    #print(y_predict.shape) #(1, 30, 454)
    indexs = y_predict.argmax(axis=2)
    #print(indexs) #[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]

    # 인덱스를 문장으로 변환
    text = convert_index_to_word(indexs[0], index_to_word)
    print()
    print('짬뽕 하나 주세요 ->', text) #<PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> <PADDING> 

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) #optimizer='rmsprop' 더 좋은 성능
#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.compile(loss=tf.keras.losses.CategoricalCrossentropy(), optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), metrics=[tf.keras.metrics.Accuracy()])

model.fit([x_encoder, x_decoder], y_decoder, epochs=100, validation_split=0.3, callbacks=[tf.keras.callbacks.LambdaCallback(on_epoch_end=on_epoch_end)])

##########모델 예측

print('인공지능 챗봇')
print('인공지능 챗봇과 대화를 합니다.')

x_encoder = [
    '짬뽕 하나 주세요'
]

x_encoder = clean_korean_documents_simple_version(x_encoder)
x_encoder = convert_word_to_index(x_encoder, word_to_index, ENCODER_INPUT)
#print(x_encoder) #[[209 201 271  70 219 113   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0]]
#print(len(x_encoder[0])) #30

# 입력을 인코더에 넣어 마지막 상태 구함
state_h, state_c = encoder_model(x_encoder)
#print(state_h.shape) #(1, 128)
#print(state_c.shape) #(1, 128)

# 인덱스 초기화
indexs = []

# 목표 시퀀스 초기화
x_decoder = np.zeros((1, 1))
# 목표 시퀀스의 첫 번째에 <START> 태그 추가
x_decoder[0, 0] = START_INDEX
#print(x_decoder) #[[1.]]

# 디코더로 현재 타임 스텝 출력 구함
# 처음에는 인코더 상태를, 다음부터 이전 디코더 상태로 초기화
# 디코더의 이전 상태를 다음 디코더 예측에 사용
y_predict, state_h, state_c = decoder_model([x_decoder, state_h, state_c])
#print(y_predict.shape) #(1, 1, 454)
#print(state_h.shape) #(1, 128)
#print(state_c.shape) #(1, 128)
# 결과의 원핫인코딩 형식을 인덱스로 변환
#print(y_predict[0, 0, :].shape) #(454,)
index = y_predict[0, 0, :].numpy().argmax()
#print(index) #0
indexs.append(index)

# 디코더 타임 스텝 반복
while index != END_INDEX:
    # 목표 시퀀스를 바로 이전의 출력으로 설정
    x_decoder = np.zeros((1, 1))
    x_decoder[0, 0] = index
    #print(x_decoder) #[[0.]]

    # 디코더로 현재 타임 스텝 출력 구함
    # 처음에는 인코더 상태를, 다음부터 이전 디코더 상태로 초기화
    # 디코더의 이전 상태를 다음 디코더 예측에 사용
    y_predict, state_h, state_c = decoder_model([x_decoder, state_h, state_c])
    #print(y_predict.shape) #(1, 1, 454)
    #print(state_h.shape) #(1, 128)
    #print(state_c.shape) #(1, 128)
    # 결과의 원핫인코딩 형식을 인덱스로 변환
    #print(y_predict[0, 0, :].shape) #(454,)
    index = y_predict[0, 0, :].numpy().argmax() 
    #print(index) #0
    indexs.append(index)

    # 종료 검사
    if len(indexs) >= sequence_length:
        break

# 인덱스를 문장으로 변환
#print(indexs) #[194, 257, 379, 2] 
text = convert_index_to_word(indexs, index_to_word)
print(text) #저 도 요 


