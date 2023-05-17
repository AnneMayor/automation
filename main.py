from util.generator import file_generator
import pandas as pd

def main():
    excel_file = pd.read_excel('files/your_file_name.xlsx', sheet_name='your_excel_sheet')
    excel_file.to_csv('files/your_file_name.csv', index=False)

    file_generator('files/your_file_name.csv')

if __name__ == '__main__':
    main()
