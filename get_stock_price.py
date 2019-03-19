#!/usr/bin/env python3
"""
주가 [날짜, 종가, 시가, 고가, 저가, 거래량] --> to.xlsx
Output filename: ./input/[stock_name].xlsx
"""
import pandas as pd
import pandas_datareader.data as web

from datetime import datetime

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def stock_list():
    df = pd.read_excel('./input/상장법인목록.xlsx', dtype='str')

    return df

def get_url(company, stock_list):
    code = stock_list.query("company=='{}'".format(company))['code'].to_string(index = False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code = code)
    print("요청 URL = {}".format(url))

    return url

def get_stock_price(stock_name, stock_list):
    url = get_url(stock_name, stock_list)
    df = pd.DataFrame()

    for page in range(1, 100): #range ==> 날짜별 주가 for-loop
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    df = df[['날짜', '종가', '시가', '고가', '저가', '거래량']]
    df = df.rename(columns={'날짜':'date', '종가':'close', '시가':'open',
                            '고가':'high', '저가':'low', '거래량':'volume'})
    stock_df = df.dropna()

    return stock_df

def main():
    df = stock_list()
    company_list = df['company'][82]

    sp = get_stock_price(company_list, df)
    print(sp)

    file_name = './input/{}.xlsx'.format(company_list)
    sp = sp.astype('str')
    sp.to_excel(file_name, index=False)
    print('성공적으로 생성되었습니다. \nfile_name : {}'.format(file_name))

if __name__ == "__main__":
    main()
