import re
import pandas as pd
from pandas import DataFrame

# 데이터를 불러옴
df = pd.read_csv('chatbot.csv', sep = ',', encoding= 'utf-8')

review_column = ['shopid','menu_summary','nickname','rating','customer_comment','owner_comment']

# 이모티콘 제거
only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF" 
                           "]+", flags=re.UNICODE)

result=[]
for index, row in df.iterrows():
    customer = only_BMP_pattern.sub(r'', row['customer_comment'])
    answer = only_BMP_pattern.sub(r'', row['owner_comment'])
    imsi = [row['shopid'],row['menu_summary'],row['nickname'],row['rating'], customer, answer]
    result.append(imsi)

result = pd.DataFrame(result, columns=review_column)

# 심볼
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

result1=[]
for index, row in result.iterrows():
    customer = emoji_pattern.sub(r'', row['customer_comment'])
    # 나머지
    customer = re.sub('[❤️★♥️✨⭐♡♥☆⚽️⚾️❄❣️❤]', '', customer)
    answer = emoji_pattern.sub(r'', row['owner_comment'])
    # 나머지
    answer = re.sub('[❤️★♥️✨⭐♡♥☆⚽️⚾️❄❣️❤]', '', answer)
    imsi = [row['shopid'],row['menu_summary'],row['nickname'],row['rating'], customer, answer]
    result1.append(imsi)

result1 = pd.DataFrame(result1, columns=review_column)
result1.to_csv('test3.csv', mode='w', encoding='utf-8', index=False)

print('=======test2========')

