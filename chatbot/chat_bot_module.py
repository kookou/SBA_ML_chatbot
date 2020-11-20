from bs4 import BeautifulSoup
import re
import konlpy
import numpy as np
import pickle
import tensorflow as tf

# 데이터 타입
QUESTION_INPUT  = 0
ANSWER_INPUT  = 1
DECODER_TARGET = 2

# 태그 단어
PAD = "<PADDING>"   # 패딩
STA = "<START>"     # 시작
END = "<END>"       # 끝
OOV = "<OOV>"       # 없는 단어(Out of Vocabulary)

# 한 문장에서 단어 시퀀스의 최대 개수
max_sequences = 30

# 태그 인덱스
PAD_INDEX = 0
STA_INDEX = 1
END_INDEX = 2
OOV_INDEX = 3

def clean_korean_documents_simple(documents):
    #텍스트 정제 (HTML 태그 제거)
    for i, document in enumerate(documents):
        document = BeautifulSoup(document, 'html.parser').text 
        #print(document) #스토리가 진짜 너무 노잼
        documents[i] = document

    #텍스트 정제 (특수기호 제거)
    for i, document in enumerate(documents):
        document = re.sub(r'[.,!?"\':;~()]', '', document) #특수기호 제거, 정규 표현식
        #print(document) stale and uninspired
        documents[i] = document

    #텍스트 정제 (형태소 추출)
    for i, document in enumerate(documents):
        okt = konlpy.tag.Okt()
        clean_words = []
        for word in okt.morphs(document): 
            clean_words.append(word)
        #print(clean_words) #['스토리', '진짜', '노잼']
        document = ' '.join(clean_words)
        #print(document) #스토리 진짜 노잼
        documents[i] = document

    return documents

# 문장을 인덱스로 변환
def convert_text_to_index(sentences, vocabulary, type): 

    sentences_index = []

    # 모든 문장에 대해서 반복
    for sentence in sentences:
        sentence_index = []

        # 디코더 입력일 경우 맨 앞에 START 태그 추가
        if type == ANSWER_INPUT:
            sentence_index.extend([vocabulary[STA]])

        # 문장의 단어들을 띄어쓰기로 분리
        for word in sentence.split():
            if vocabulary.get(word) is not None:
                # 사전에 있는 단어면 해당 인덱스를 추가
                sentence_index.extend([vocabulary[word]])
            else:
                # 사전에 없는 단어면 OOV 인덱스를 추가
                sentence_index.extend([vocabulary[OOV]])

        # 최대 길이 검사
        if type == DECODER_TARGET:
            # 디코더 목표일 경우 맨 뒤에 END 태그 추가
            if len(sentence_index) >= max_sequences:
                sentence_index = sentence_index[:max_sequences-1] + [vocabulary[END]]
            else:
                sentence_index += [vocabulary[END]]
        else:
            if len(sentence_index) > max_sequences:
                sentence_index = sentence_index[:max_sequences]

        # 최대 길이에 없는 공간은 패딩 인덱스로 채움
        sentence_index += (max_sequences - len(sentence_index)) * [vocabulary[PAD]]

        # 문장의 인덱스 배열을 추가
        sentences_index.append(sentence_index)

    return np.asarray(sentences_index)

# 인덱스를 문장으로 변환
def convert_index_to_text(indexs, vocabulary): 

    sentence = ''

    # 모든 문장에 대해서 반복
    for index in indexs:
        if index == END_INDEX:
            # 종료 인덱스면 중지
            break;
        if vocabulary.get(index) is not None:
            # 사전에 있는 인덱스면 해당 단어를 추가
            sentence += vocabulary[index]
        else:
            # 사전에 없는 인덱스면 OOV 단어를 추가
            sentence.extend([vocabulary[OOV_INDEX]])

        # 빈칸 추가
        sentence += ' '

    return sentence

##########모델 로드

with open('model/chat_bot_model_word_to_index.pkl', 'rb') as f:
    word_to_index = pickle.load(f)

with open('model/chat_bot_model_index_to_word.pkl', 'rb') as f:
    index_to_word = pickle.load(f)

model = tf.saved_model.load('model/chat_bot_model/1')

print(model.signatures.keys()) #KeysView(_SignatureMap({'serving_default': <tensorflow.python.saved_model.load._WrapperFunction object at 0x13d11b910>, 'encoder': <tensorflow.python.saved_model.load._WrapperFunction object at 0x13c960d10>, 'decoder': <tensorflow.python.saved_model.load._WrapperFunction object at 0x13d268fd0>}))
print(model.signatures['serving_default'].structured_input_signature) #((), {'input1': TensorSpec(shape=(None, None), dtype=tf.float32, name='input1'), 'input2': TensorSpec(shape=(None, None), dtype=tf.float32, name='input2')})
print(model.signatures['serving_default'].structured_outputs) #{'output_0': TensorSpec(shape=(None, None, 454), dtype=tf.float32, name='output_0')}
print(model.signatures['encoder'].structured_input_signature) #((), {'input': TensorSpec(shape=(None, None), dtype=tf.float32, name='input')})
print(model.signatures['encoder'].structured_outputs) #{'output_0': TensorSpec(shape=(None, None, 128), dtype=tf.float32, name='output_0'), 'output_1': TensorSpec(shape=(None, 128), dtype=tf.float32, name='output_1'), 'output_2': TensorSpec(shape=(None, 128), dtype=tf.float32, name='output_2')}
print(model.signatures['decoder'].structured_input_signature) #((), {'input1': TensorSpec(shape=(None, None), dtype=tf.float32, name='input1'), 'input2': TensorSpec(shape=(None, 128), dtype=tf.float32, name='input2'), 'input3': TensorSpec(shape=(None, 128), dtype=tf.float32, name='input3')})
print(model.signatures['decoder'].structured_outputs) #{'output_0': TensorSpec(shape=(None, None, 454), dtype=tf.float32, name='output_0'), 'output_1': TensorSpec(shape=(None, 128), dtype=tf.float32, name='output_1'), 'output_2': TensorSpec(shape=(None, 128), dtype=tf.float32, name='output_2')}

##########모델 예측

# 텍스트 생성
def chat(sentence):
    sentences = []
    sentences.append(sentence)
    sentences = clean_korean_documents_simple(sentences)
    question_seq = convert_text_to_index(sentences, word_to_index, QUESTION_INPUT)
    #print(question_seq) #[[209 201 271  70 219 113   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0]]
    #print(len(question_seq[0])) #30

    # 입력을 인코더에 넣어 마지막 상태 구함
    d = model.signatures['encoder'](input=tf.constant(question_seq, dtype=tf.float32))
    encoder_outputs, state_h, state_c = d['output_0'], d['output_1'], d['output_2']
    #print(encoder_outputs.shape) #(1, 30, 128)
    #print(state_h.shape) #(1, 128)
    #print(state_c.shape) #(1, 128)

    # 목표 시퀀스 초기화
    answer_seq = np.zeros((1, 1))
    # 목표 시퀀스의 첫 번째에 <START> 태그 추가
    answer_seq[0, 0] = STA_INDEX
    #print(answer_seq) #[[1.]]

    # 인덱스 초기화
    indexs = []

    # 디코더 타임 스텝 반복
    while 1:
        # 디코더로 현재 타임 스텝 출력 구함
        # 처음에는 인코더 상태를, 다음부터 이전 디코더 상태로 초기화
        # 디코더의 이전 상태를 다음 디코더 예측에 사용
        d = model.signatures['decoder'](input1=tf.constant(answer_seq, dtype=tf.float32), input2=tf.constant(state_h, dtype=tf.float32), input3=tf.constant(state_c, dtype=tf.float32))
        decoder_outputs, state_h, state_c = d['output_0'], d['output_1'], d['output_2']
        #print(decoder_outputs.shape) #(1, 1, 329)
        #print(state_h.shape) #(1, 128)
        #print(state_c.shape) #(1, 128)

        # 결과의 원핫인코딩 형식을 인덱스로 변환
        #print(decoder_outputs[0, 0, :].shape) #(329,)        
        index = np.argmax(decoder_outputs[0, 0, :])
        #print(index) #0        
        indexs.append(index)

        # 종료 검사
        if index == END_INDEX or len(indexs) >= max_sequences:
            break

        # 목표 시퀀스를 바로 이전의 출력으로 설정
        answer_seq = np.zeros((1, 1))
        answer_seq[0, 0] = index
        #print(answer_seq) #[[0.]]

    # 인덱스를 문장으로 변환
    #print(indexs) #[194, 257, 379, 2] 
    sentence = convert_index_to_text(indexs, index_to_word)
    #print(sentence)

    return sentence

if __name__ == '__main__':
    print('인공지능 챗봇')
    print('인공지능 챗봇과 대화를 합니다.')

    while True:
        text = input('나: ')
        if text == 'quit':
            break

        print('챗봇:', chat(text))