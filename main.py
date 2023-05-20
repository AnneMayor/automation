"""Automation Main Module"""

import pandas as pd
from util.generator import file_generator


def main():
    """execute automated file generation program"""

    excel_file = pd.read_excel('files/your_file_name.xlsx', sheet_name='your_file_sheet')
    excel_file.to_csv('files/your_file_name.csv', index=False)

    file_generator('files/your_file_name.csv')

if __name__ == '__main__':
    main()
