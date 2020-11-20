import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))

from util.file_helper import FileReader
import pdb
import json
import requests
import time
import pandas as pd

class YogiyoCrawler:

    def __init__(self):
        print(f'baseurl #### {baseurl}')
        self.reader = FileReader()

    def get_json(self, url):

        payload = {}
        headers = {
          'x-apikey': 'iphoneap',
          'x-apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2'
        }

        try:
            response = requests.request("GET", url, headers=headers, data = payload)
        except:
            print("ZZzzzz...")
            time.sleep(5)  # 너무 많은 request로 에러가 발생할 수 있으므로 잠시 쉰다
            return ['']  # 에러 발생 후 리스트를 리턴하여 해당번호는 패스하게 만듬
        try:
            json_data = response.json()
        except:
            print('유효하지 않은 json형식')
            return []
        # print(json_data)
        return json_data

    def get_json_store(self, start, end):
        json_list = []
        for index in range(start, end):
            index = str(index).zfill(6)
            url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{index}"
            ajson = self.get_json(url)
            if isinstance(ajson, dict):
                json_list.append(ajson)
            print(f'{index}번 크롤링 중')
        
        file_path = f"./data/json/store/yogiyo_store({start}~{end}).json"
        with open(file_path, 'w', encoding='UTF-8-sig') as file:
            json.dump(json_list, file, indent=4, ensure_ascii=False)
        print(f'yogiyo_store({start}~{end}).json 저장완료')

    def get_json_menu(self, start, end, list_data):
        json_list = []
        error_list = []
        for index in range(start, end):
            id = list_data[index]
            url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{id}/menu?add_photo_menu=android"
            ajson = self.get_json(url)


            print(f'{index}번 크롤링 중')
            pre_json = {"id": id, "menus": []}  # 전처리 데이터를 담을 json. 우선 id를 담는다.
            item_list = []
            id_set = set()  # 중복 아이템 관리 리스트
            for i in range(len(ajson)):
                try:
                    if isinstance(ajson[i], dict):
                        # 필요 데이터만 전처리
                        # print(ajson)
                        # print(len(ajson))
                        for item in ajson[i]["items"]:
                            if item["id"] not in id_set:
                                item_dict = dict()
                                item_dict["name"] = item["name"]
                                item_dict["price"] = item["price"]
                                item_dict["id"] = item["id"]
                                item_dict["review_count"] = item["review_count"]
                                # image 누락 아이템 예외 처리
                                try:
                                    item_dict["image"] = item["image"]
                                except:
                                    item_dict["image"] = "no_image"
                                item_list.append(item_dict)
                                # 중복 관리를 위해 리스트에 id 추가
                                id_set.add(item["id"])
                    pre_json["menus"] = item_list
                except:
                    error_list.append(id)
                    print(f'오류 데이터: id:{id}')
                    print(i)
            json_list.append(pre_json)

        # 파일 저장
        reader = self.reader
        reader.context = os.path.join(baseurl, './../../data/json/menu(seoul)')
        reader.fname = f'yogiyo_menu({start}~{end}).json'
        reader.new_file()
        reader.json_save(json_list)

        # 에러 로그 저장
        reader.fname = f'yogiyo_menu_error({start}~{end}).json'
        reader.new_file()
        reader.json_save(error_list)


    def get_json_review(self, start, end, list_data):
        json_list = []
        error_list = []
        for index in range(start, end):
            id = list_data[index]
            url = f"https://www.yogiyo.co.kr/api/v1/reviews/{id}"
            ajson = self.get_json(url)

            print(f'{index}번 크롤링 중')

            try:
                if isinstance(ajson[0], dict):
                    pre_json = {"id": id}
                    pre_json["reviews"] = ajson
                    json_list.append(pre_json)
            except:
                print(f'오류 데이터: id:{id}', ajson)
                error_list.append(id)


        # 파일 저장
        reader = self.reader
        reader.context = os.path.join(baseurl, 'data/json/review(seoul)')
        reader.fname = f'yogiyo_review({start}~{end}).json'
        reader.new_file()
        reader.json_save(json_list)

        # 에러 로그 저장
        reader.fname = f'yogiyo_review_error({start}~{end}).json'
        reader.new_file()
        reader.json_save(error_list)



    def load_json(self, file_path):

        # file_path = "./sample.json"
        with open(file_path, "r", encoding="UTF-8-SIG") as json_file:
            json_data = json.load(json_file)
            # print(json_data)

        return json_data

    def get_store_id_by_city(self, json_data, city):
        id_list = []
        for item in json_data:
            if city == item['city']:
                 id_list.append(item['id'])
        return id_list

    # 테스트 중
    def json_to_csv(self, json_data, start, end):
        reader = self.reader
        reader.context = os.path.join(baseurl, 'data/csv/store')
        reader.fname = f'yogiyo_store({start}~{end}).csv'
        reader.new_file()
        reader.json_to_csv(json_data)







# import numpy as np
# a = np.array(list)
# print(np.median(a))
# print(max(list))
# print('아이디:', restaurants[0]["id"])
# print('상호:', restaurants[0]["name"])
# print('주소:', restaurants[0]["address"])
# print('거리:', restaurants[0]["distance"])
# print('위도:', restaurants[0]["lng"])
# print('경도:', restaurants[0]["lat"])
# print('대표 메뉴:', restaurants[0]["representative_menus"])
# print('카테고리:', restaurants[0]["categories"])
# print('배달비:', restaurants[0]["delivery_fee"])
# print('최소 주문액:', restaurants[0]["min_order_amount"])
# print('영업 시간:', restaurants[0]["open_time_description"])
# print('리뷰 평점:', restaurants[0]["review_avg"])

# list = []
# # for i, item in enumerate(restaurants):
# for i in range(5):
#     list.append(restaurants[i]["id"])
#
# print(list)
#
# json_list = []



if __name__ == '__main__':
    yogiyo = YogiyoCrawler()

    # 매장 크롤링
    # start = 361000
    # end = 362000
    # for i in range(9):
    #     yogiyo.get_json_store(start, end)
    #     start += 1000
    #     end += 1000
    # yogiyo.get_json_store(0, 1000)


    # -------------------------
    # 메뉴 크롤링
    # file_path = f'./../../data/yogiyo_store_id_list(seoul).json'
    # json_data = yogiyo.load_json(file_path)
    #
    # file_path = r'./../../data/csv/gangnam_seocho.csv'
    # df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig')
    #
    # # 강남 서초만
    # shop_list = df['id'].drop_duplicates().tolist()
    # print(len(shop_list))
    # start = 0
    # end = 1000
    # # for i in range(5):
    # #     yogiyo.get_json_menu(start, end, shop_list)
    # #     start += 1000
    # #     end += 1000
    # yogiyo.get_json_menu(5000, 5965, shop_list)

    # -------------------------
    # 리뷰 크롤링
    # file_path = f'./data/yogiyo_store_id_list(seoul).json'
    # json_data = yogiyo.load_json(file_path)
    # start = 0
    # end = 1000
    # for i in range(42):
    #     yogiyo.get_json_review(start, end, json_data)
    #     start += 1000
    #     end += 1000
    # yogiyo.get_json_review(42000, 42612, json_data)

    #---------------------------
    # json을 csv로(매장)
    # start = 0
    # end = 1000
    # for i in range(849):
    #     input_file_path = f'./data/json/store/yogiyo_store({start}~{end}).json'
    #     try:
    #         yogiyo.json_to_csv(input_file_path, start, end)
    #     except:
    #         pass
    #     start += 1000
    #     end += 1000
    # yogiyo.json_to_csv(f'./../../data/json/store/yogiyo_store({0}~{1000}).json', 0, 1000)

    #---------------------------
    # csv 병합
    # input_path = './data/csv/store'
    # output_file = './data/csv/store/yogiyo_store(total).csv'
    # reader = FileReader()
    # reader.merge_csv(input_path, output_file, '*.csv')




    # ---------------------------
    # 서울의 매장 id만 취합

    # start = 0
    # end = 1000
    # total_list = []
    # for i in range(498):
    #     file_path = f'./data/json/yogiyo_store({start}~{end}).json'
    #     json_data = yogiyo.load_json(file_path)
    #     id_list = yogiyo.get_store_id_by_city(json_data, '서울')
    #     # print(id_list)
    #     total_list += id_list
    #     start += 1000
    #     end += 1000
    #
    # print(len(total_list))
    # file_path = "./yogiyo_store_id_list(seoul).json"
    # with open(file_path, 'w', encoding='UTF-8-sig') as file:
    #     json.dump(total_list, file, indent=4, ensure_ascii=False)















