"""File Generator Module"""

import csv
import re
import math
import pandas as pd

from exception.common_exception import UnknownTypeException


CSV_FILE_PATTERN = r'.csv$'
NAME_FILTER = r'\((.*?)\)'
WORD_FILTER = r'주식회사'
TECH_SUPPORT_FILTER = r'기술지원'
COMMENT_FILTER = r'msp|ta계약'
SALES_INCENTIVE_FILTER = r'omm'
SALES_FIRM = '매출 거래처명'
SALES_ISSUED_DATE = '매출 세금계산서 발행일자'
PURCHASES_ISSUED_DATE = '매입 세금계산서 발행일자'
PURCHASE_FIRM = '매입 거래처명'
PRICE_SALES = '매출금액(KRW)'
PRICE_PURCHASES = '원가금액(KRW)'
COST_RATIO = '원가율'

def file_generator(origin_file):
    """generate new file according to origin file type"""

    if re.search(CSV_FILE_PATTERN, origin_file):
        csv_file = csv_generator(origin_file)
        excel_generator(csv_file)

    else:
        raise UnknownTypeException('Unknown file type')

def csv_generator(origin_file):
    """generate csv file from excel"""

    raw_data = read_csv(origin_file)
    update_file(raw_data, origin_file)
    return origin_file

def read_csv(origin_file):
    """read csv file data"""

    new_data = []
    with open(origin_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)

        header = next(reader)

        header[0] = SALES_ISSUED_DATE
        header[2] = SALES_FIRM
        header[3] = PRICE_SALES
        header[5] = PURCHASES_ISSUED_DATE
        header[7] = PURCHASE_FIRM
        header[8] = PRICE_PURCHASES

        new_data.append(header)

        for row in reader:
            new_data.append(filter_data(row))

    filtered_new_data = list(filter(lambda x: len(x) > 0, new_data))

    return filtered_new_data

def filter_data(row):
    """filter data following conditions"""

    if all(not x for x in row):
        return []

    if re.findall(COMMENT_FILTER, row[4].lower()):
        row[4] = 'MSP'
        return row

    if row[0] == '' and re.findall(TECH_SUPPORT_FILTER, row[6].lower()):
        row[4] = 'MSP'
        return row

    if re.findall(SALES_INCENTIVE_FILTER, row[6].lower()):
        row[4] = '판매장려금'
        return row

    return row

def update_file(data, origin_file):
    """update file data"""

    with open(origin_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def excel_generator(origin_csv_file):
    """generate excel file from csv file"""

    new_csv_file = pd.read_csv(origin_csv_file)
    new_csv_file = new_csv_file.drop(new_csv_file.columns[[1,6]], axis=1)

    new_csv_file[COST_RATIO] = (new_csv_file[PRICE_PURCHASES] / new_csv_file[PRICE_SALES]) * 100
    new_csv_file[COST_RATIO] = new_csv_file[COST_RATIO].fillna(0)
    new_csv_file[COST_RATIO] = new_csv_file[COST_RATIO].astype('float64')

    new_csv_file[COST_RATIO] = new_csv_file[COST_RATIO].apply(math.floor)

    new_csv_file.to_excel('outputs/your_file_name_final.xlsx', index=False, header=True)
