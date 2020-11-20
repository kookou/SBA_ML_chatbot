import pandas as pd

# https://www.bigdatahub.co.kr/product/view.do?pid=1002328


for y in range(1, 9):
    filename = 'Calldata_200%s.csv'%(y)
    myframe = pd.read_csv(filename, sep = ',', encoding= 'utf-8')

    # 통화 데이터에서 음식점 통화 데이터만 추출
    result = []
    mycolumns = ('일자(YYYYMMDD)', '연령', '성별','발신지(시도)','발신지(시군구)','업종')
    for index, row in myframe.iterrows():

        if row['발신지(시도)'] == '경기':
            imsi = [row['일자(YYYYMMDD)'], row['연령'], row['성별'],row['발신지(시도)'],row['발신지(시군구)'],row['중분류']]

            if row['대분류'] == '음식점':
                imsi = [row['일자(YYYYMMDD)'], row['연령'], row['성별'],row['발신지(시도)'],row['발신지(시군구)'],row['중분류']]
                result.append(imsi)
    print('--------ing-------------')
    result = pd.DataFrame(result, columns=mycolumns)

    # remove irrelvant row
    idx = result[(result['업종'] == '술집') | (result['업종'] == '음식점') | (result['업종'] == '뷔페')].index
    result = result.drop(idx)
    print(result.head())

    filename1 = './orderdata/order_kyungki_200%s.csv'%(y)
    result.to_csv(filename1, mode= 'w', encoding='utf-8',index=False)




print('finished')
