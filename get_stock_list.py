#!/usr/bin/env python3
"""
한국거래소 홈페이지에서 코스피, 코스닥 상장종목 목록 다운로드 --> to.xlsx
Output filename: ./input/상장법인목록.xlsx
"""
import pandas as pd
import pandas_datareader.data as web

from datetime import datetime

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def get_stock_list():
    ks_df = pd.read_html('./data/상장법인목록_코스피.xls', header=0)[0]
    kq_df = pd.read_html('./data/상장법인목록_코스닥.xls', header=0)[0]

    stock_list = [ks_df, kq_df]

    ks_df['market'] = 'KS'
    kq_df['market'] = 'KQ'

    for list in stock_list:
        list.종목코드 = list.종목코드.map('{:06d}'.format)
        list = list[['회사명', '종목코드', '업종']]

    df = pd.concat(stock_list)
    df = df.rename(columns={'회사명':'company', '종목코드':'code', '업종':'division'})

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

    for page in enum:
        pg_url = '{url}&page={page}'.format(url = url, page = page)
        df = df.append(pd.read_html(pg_url, header = 0)[0], ignore_index= True)
        index = pd.read_html(pg_url, header = 0)[0]

    stock_df = df.dropna()

    return stock_df

def main():
    #if len(sys.argv) < 2:
    #    print('Usage: ./all_tickers.py <True/False>')
    #    return
    #top_n = sys.argv[1]
    df = get_stock_list()
    file_name = './input/상장법인목록.xlsx'
    df = df.astype('str')
    df.to_excel(file_name, index=False)
    print('성공적으로 생성되었습니다. \nfile_name : {}'.format(file_name))

if __name__ == "__main__":
    main()
