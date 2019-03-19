#!/usr/bin/env python3
"""
개별종목별 연도별, 분기별 재무재표 다운로드 --> to.xlsx
Output filename: ./input/[stock_name]_[period].xlsx
"""
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def stock_list():
    df = pd.read_excel('./input/상장법인목록.xlsx', dtype='str')

    return df

def finance_stats(company, stock_list):

    code = stock_list.query("company=='{}'".format(company))['code'].to_string(index = False)

    URL = "https://finance.naver.com/item/main.nhn?code={code}".format(code=code)

    get_url = requests.get(URL)
    html = get_url.text

    soup = BeautifulSoup(html, 'html.parser')

    finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]

    th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
    annual_date = th_data[3:7]
    quarter_date = th_data[7:13]

    finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]
    finance_data = [item.get_text().strip() for item in finance_html.select('td')]
    finance_data = np.array(finance_data)

    finance_data.resize(len(finance_index), 10)

    finance_date = annual_date + quarter_date

    finance = pd.DataFrame(data=finance_data[0:,0:], index=finance_index, columns=finance_date)

    annual_finance = finance.iloc[:, :4]
    quarter_finance = finance.iloc[:, 4:]

    return annual_finance, quarter_finance

def main():
    df = stock_list()
    company_list = df['company'][82]

    annual, quarter = finance_stats(company_list, df) #삼성에스디에스
    print(annual)
    print(quarter)

    file_name = './input/{}_annual.xlsx'.format(company_list)
    annual = annual.astype('str')
    annual.to_excel(file_name, index=False)
    print('성공적으로 생성되었습니다. \nfile_name : {}'.format(file_name))

    file_name = './input/{}_quarter.xlsx'.format(company_list)
    quarter = quarter.astype('str')
    quarter.to_excel(file_name, index=False)
    print('성공적으로 생성되었습니다. \nfile_name : {}'.format(file_name))


if __name__ == "__main__":
    main()
