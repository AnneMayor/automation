import exception.CommonException as commonException

import csv
import re
import enum
import pandas as pd
import math

csv_file_pattern = r'.csv$'
name_filter = r'\((.*?)\)'
word_filter = r'주식회사'
tech_support_filter = r'기술지원'
comment_filter = r'msp|ta계약'
sales_incentive_filter = r'omm'
sales_firm = '매출 거래처명'
sales_issued_date = '매출 세금계산서 발행일자'
purchases_issued_date = '매입 세금계산서 발행일자'
purchase_firm = '매입 거래처명'
price_sales = '매출금액(KRW)'
price_purchases = '원가금액(KRW)'
cost_ratio = '원가율'


class Status(enum.Enum):
    SUCCESS = 0
    FAIL = 1
    UNKNOWN = -1

def default():
    raise commonException.UnknownTypeException("Unknown file type")

def file_generator(origin_file):
    if(re.search(csv_file_pattern, origin_file)):
        new_file = csv_generator(origin_file)
        excel_generator(new_file)

    else:
        default()

def csv_generator(origin_file):
    data = read_csv(origin_file)
    write_data(data, origin_file)
    return origin_file

def read_csv(origin_file):
    new_data = []
    with open(origin_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)

        header = next(reader)

        header[0] = sales_issued_date
        header[2] = sales_firm
        header[3] = price_sales
        header[5] = purchases_issued_date
        header[7] = purchase_firm
        header[8] = price_purchases

        new_data.append(header)
        
        for row in reader:
            new_data.append(extract_data(row))

    filtered_new_data = list(filter(lambda x: len(x) > 0, new_data))
    
    return filtered_new_data

def extract_data(row):
    if(all(not x for x in row)):
        return []
    
    if(re.findall(comment_filter, row[4].lower())):
        row[4] = 'MSP'
        return row

    if(row[0] == '' and re.findall(tech_support_filter, row[6].lower())):
        row[4] = 'MSP'
        return row
    
    if(re.findall(sales_incentive_filter, row[6].lower())):
        row[4] = '판매장려금'
        return row
    
    return row

def write_data(data, origin_file):
    with open(origin_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def excel_generator(new_file):
    new_csv_file = pd.read_csv(new_file)
    new_csv_file = new_csv_file.drop(new_csv_file.columns[[1,6]], axis=1)

    new_csv_file[cost_ratio] = (new_csv_file[price_purchases] / new_csv_file[price_sales]) * 100
    new_csv_file[cost_ratio] = new_csv_file[cost_ratio].fillna(0)
    new_csv_file[cost_ratio] = new_csv_file[cost_ratio].astype('float64')
    
    new_csv_file[cost_ratio] = new_csv_file[cost_ratio].apply(math.floor)

    new_csv_file.to_excel('your_file_name_final.xlsx', index=False, header=True)
