import os
import logging
from datetime import datetime
import pandas as pd


class Transactions:
    
    def __init__(self, account: str, date_of_interest: str):
        self.account = account
        self.date_of_interest = date_of_interest
        self.input_path = f'input/{self.account}/{self.date_of_interest}'

    @staticmethod
    def read_input(input_path: str, file_name: str, sep: str) -> pd.DataFrame:
        df = pd.read_csv(f'{input_path}/{file_name}', index_col=False, sep=sep)
        logging.info(f'Read {df.count()} records from {input_path}.')
        return df
    
    @staticmethod
    def preprocess(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.lower()
        df['bedrag'] = [amount.replace(',', '.') for amount in df.bedrag]
        df['operatie'] = ['-' if '-' in amount else '+' for amount in df.bedrag]
        return df[['valutadatum', 'naam tegenpartij bevat', 'bedrag', 'operatie']]
    
    def split_up_date(self, df: pd.DataFrame) -> pd.DataFrame:
        df['valutadatum'] = self.to_datetime_format(df, 'valutadatum')
        df['year'] = [datum.year for datum in df['valutadatum']]
        df['month'] = [datum.month for datum in df['valutadatum']]
        df['day'] = [datum.day for datum in df['valutadatum']]
        return df.drop('valutadatum', axis=1)

    def filter_on_month_of_interest(self, df: pd.DataFrame) -> pd.DataFrame:
        date_of_interest = datetime.strptime(self.date_of_interest, '%Y-%m')
        date_of_interest_month = date_of_interest.month
        
        return df[df['month'] == date_of_interest_month]
    
    def get_output_path(self, df: pd.DataFrame) -> str:
        latest_day = max(df['day'].values)
        month = df['month'].unique()[0]
        year = df['year'].unique()[0]
        latest_date = f'{year}-{month}-{latest_day}'
        return f'output/{self.account}/{latest_date}'

    @staticmethod
    def write_output(df: pd.DataFrame, output_path: str, file_name: str) -> None:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        df.to_excel(f'{output_path}/{file_name}')
        logging.info(f'Wrote {df.count()} records to {output_path}.')
    
    @staticmethod
    def to_datetime_format(df: pd.DataFrame, col: str, time_format: str = '%d/%m/%Y') -> list:
        return [datetime.strptime(value[0], time_format) for value in df[[col]].values.tolist()]


def main(account, date_of_interest):
    transactions = Transactions(account, date_of_interest)

    df = transactions.read_input(transactions.input_path, "input.csv", ";")
    df = transactions.preprocess(df)
    df = transactions.split_up_date(df)
    df = transactions.filter_on_month_of_interest(df)
    output_path = transactions.get_output_path(df)
    transactions.write_output(df, output_path, f"{date_of_interest}_output.xlsx")


if __name__ == "__main__":
    main(
        account="lisa_william",
        date_of_interest="2022-11"
        )
