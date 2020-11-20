import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))

import csv
import json
import glob

import pandas as pd
from pandas import DataFrame

CSV_COLUMNS = ['shop_id', 'shop_name', 'shop_addr', 'shop_img', 'cat', 'shop_lat', 'shop_lng', 'shop_rev_avg',
               'shop_rev_cnt', 'open_time']  # shop 컬럼 커스텀 지정
mycolums = ['storeid', 'comment', 'rating', 'menu_summary', 'rating_quantity', 'rating_taste', 'rating_delivery',
            'time', 'nickname', 'customerid']  # review 컬럼 커스텀 지정
menu_column = ['food_id', 'food_name', 'price', 'food_img', 'food_rev_cnt', 'shop_id']  # food  컬럼 커스텀 지정


class YogiyoModel:
    def __init__(self, filename):
        self.filename = filename
        self.writer = None

    def hook_process(self):
        yogiyo = YogiyoModel()
        self.yogiyo.convert()
        # self.yogiyo.get_seoul_data()
        # self.yogiyo.merge()

    def _process(self, item):  # 컬럼명으로 된 변수들에 조건에 맞는 값을 저장
        if item['city'] == '서울':
            shop_id = item['id']
            shop_name = item['name']
            shop_addr = item['address']
            cat = item['categories']
            shop_lat = item['lat']
            shop_lng = item['lng']
            open_time = item['open_time_description']
            shop_rev_avg = item['review_avg']
            shop_rev_cnt = item['review_count']
            shop_img = item['logo_url']
        else:
            shop_id = ''
            shop_name = ''
            shop_addr = ''
            shop_img = ''
            cat = ''
            shop_lat = ''
            shop_lng = ''
            shop_rev_avg = ''
            shop_rev_cnt = ''
            open_time = ''
        return [shop_id, shop_name, shop_addr, shop_img, cat, shop_lat, shop_lng, shop_rev_avg, shop_rev_cnt,
                open_time]

    def convert(self):  # json을 읽어와서 process()에서 지정한 컬럼만 csv파일로 만듬
        with open(self.filename, 'rb') as json_file:
            data = json.load(json_file)
            with open(self.filename + '.csv', 'wt', newline='', encoding="UTF-8-SIG") as csv_file:
                self.writer = csv.writer(csv_file, delimiter=',')
                self.writer.writerow(CSV_COLUMNS)
                for item in data:
                    row = self._process(item)
                    self.writer.writerow(row)
            print('----finished----')

    def review_csv(self):
        # CSV_COLUMNS=[storeid, comment, rating, menu_summary, rating_quantity, rating_taste, rating_delivery, time, nickname,customerid]
        with open(self.filename, 'rb') as json_file:
            data = json.load(json_file)
            result = []
            for item in data:
                if item['id'] != '':
                    id = item['id']
                    reviews = item['reviews']
                    for idx in reviews:
                        comment = idx['comment']
                        comment = comment.replace('\n', ' ')  # '\n' 을 공백으로 전처리
                        imsi = [item['id'], comment, idx['rating'], idx['menu_summary'], idx['rating_quantity'],
                                idx['rating_taste'], idx['rating_delivery'], idx['time'], idx['nickname'], idx['id']]
                        result.append(imsi)
                else:
                    id = ''  # 아이디 없는 경우 예외처리

        result = pd.DataFrame(result, columns=mycolums)
        outputname = f'{self.filename}.csv'
        result.to_csv(outputname, mode='w', encoding='utf-8', index=False)

        print('------------ finished --------')

    def menu_csv(self):
        with open(self.filename, 'rb') as json_file:
            data = json.load(json_file)
            result = []
            for item in data:
                id = item['id']
                menus = item['menus']
                # ['food_id', 'food_name', 'price', 'food_img', 'food_rev_cnt', 'shop_id']
                for idx in menus:
                    imsi = [idx['id'], idx['name'], idx['price'], idx['image'], idx['review_count'], id]
                    result.append(imsi)

        result = pd.DataFrame(result, columns=menu_column)
        outputname = f'{self.filename}.csv'
        result.to_csv(outputname, mode='w', encoding='utf-8', index=False)

        print('------------ finished --------')

    def merge(self):  # 여러 개의 csv파일을 한 번에 처리해서 병합
        data = []
        for file in allFile_list:
            df = pd.read_csv(file)
            data.append(df)
            dataCombine = pd.concat(data, axis=0, ignore_index=True)

        output_file = r'C:\Users\USER\data\csv\store.csv'
        dataCombine.to_csv(output_file, index=False)

        print(f'---------------csv created ---------------')

    def preprocessing(self):
        filename = '.\csv\seoul.csv'
        myframe = pd.read_csv(self.filename, sep=',', encoding='utf-8')

        myframe = myframe.dropna(axis=0)

        csvfilename = 'seoul_store_info.csv'
        myframe.to_csv(csvfilename, mode='w', encoding='utf-8', index=False)
        print(f'--------{csvfilename} done -------------')


if __name__ == '__main__':

    input_path = r'./../../data/json/store/'
    # allFile_list = glob.glob(os.path.join(input_path, 'yogiyo_menu_gs(*'))

    print(allFile_list)

    for file in allFile_list:
        YogiyoModel(f'{file}').menu_csv()
    # filename = '.\csv\seoul.csv'


    # allFile_list = glob.glob(os.path.join(input_path, 'yogiyo_*' + '.csv'))
    # print(allFile_list)
    #
    # for file in allFile_list:
    #     YogiyoModel(f'{file}').merge()
    # # filename = '.\csv\seoul.csv'
