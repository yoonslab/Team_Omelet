import pandas as pd
import pandas_datareader.data as web

from datetime import datetime
import sys
import io

class getStockAttributes:

    def get_stock_list():
        ks_df = pd.read_html('C:/workspace/Team_Omlet/data/상장법인목록_코스피.xls', header=0)[0]
        kq_df = pd.read_html('C:/workspace/Team_Omlet/data/상장법인목록_코스닥.xls', header=0)[0]

        stock_list = [ks_df, kq_df]

        ks_df['market'] = 'KS'
        kq_df['market'] = 'KQ'

        for list in stock_list:
            list.종목코드 = list.종목코드.map('{:06d}'.format)
            list = list[['회사명', '종목코드', '업종']]

        df = pd.concat(stock_list)
        df = df.rename(columns={'회사명': 'company', '종목코드': 'code', '업종': 'division'})

        stock_list = df[['code', 'market', 'company', 'division']]
        stock_list = stock_list.reset_index(drop=True)

        return stock_list

    def get_url(company, stock_list):
        code = stock_list.query("company=='{}'".format(company))['code'].to_string(index = False)
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code = code)
        print("요청 URL = {}".format(url))

        return url

    def get_stock_price(stock_name, end_date, stock_list):
        url = getStockAttributes.get_url(stock_name, stock_list)
        df = pd.DataFrame()
        for page in range(1, 2):
            pg_url = '{url}&page={page}'.format(url = url, page = page)
            df = df.append(pd.read_html(pg_url, header = 0)[0], ignore_index= True)
            index = pd.read_html(pg_url, header = 0)[0]

        stock_df = df.dropna()

        return stock_df

# 상위 5개 데이터 확인하기
stock_list = getStockAttributes.get_stock_list()

df = getStockAttributes.get_stock_price('신라젠', '2019-03-08', stock_list)

print(df.head())
print(df.tail())
