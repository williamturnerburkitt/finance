import argparse
import os
import logging
from datetime import datetime
import pandas as pd

from constants.columns import AMOUNT, COUNTERPARTY, OPERATION, EXPENSE_DATE, CURRENCY_DATE, YEAR, MONTH, DAY
from constants.drive import HOME, PRIVATE, HOUSEHOLD, YEAR_MONTH, INPUT


class Transactions:
    
    def __init__(
            self,
            household: str,
            date_of_interest: str,
            path: str = HOME + HOUSEHOLD
    ):
        self.household = household
        self.date_of_interest = date_of_interest
        self.path = path

    def read_input(self, sep: str) -> pd.DataFrame:
        df = pd.read_csv(f'{self.path}', index_col=False, sep=sep)
        logging.info(f'Read {df.count()} records from {self.path}.')
        return df
    
    @staticmethod
    def preprocess(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.lower()
        df[AMOUNT] = [amount.replace(',', '.') for amount in df.AMOUNT]
        df[OPERATION] = ['-' if '-' in amount else '+' for amount in df.AMOUNT]
        return df[[EXPENSE_DATE, COUNTERPARTY, AMOUNT, OPERATION]]
    
    def split_up_date(self, df: pd.DataFrame) -> pd.DataFrame:
        df[CURRENCY_DATE] = self.to_datetime_format(df, CURRENCY_DATE)
        df[YEAR] = [datum.year for datum in df[CURRENCY_DATE]]
        df[MONTH] = [datum.month for datum in df[CURRENCY_DATE]]
        df[DAY] = [datum.day for datum in df[CURRENCY_DATE]]
        return df.drop(CURRENCY_DATE, axis=1)

    def filter_on_month_of_interest(self, df: pd.DataFrame) -> pd.DataFrame:
        date_of_interest = datetime.strptime(self.date_of_interest, '%Y-%m')
        date_of_interest_month = date_of_interest.month
        
        return df[df['month'] == date_of_interest_month]
    
    def get_output_path(self, df: pd.DataFrame) -> str:
        latest_day = max(df['day'].values)
        month = df['month'].unique()[0]
        year = df['year'].unique()[0]
        latest_date = f'{year}-{month}-{latest_day}'
        return f'output/{self.household}/{latest_date}'

    @staticmethod
    def write_output(df: pd.DataFrame, output_path: str, file_name: str) -> None:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        df.to_excel(f'{output_path}/{file_name}')
        logging.info(f'Wrote {df.count()} records to {output_path}.')
    
    @staticmethod
    def to_datetime_format(df: pd.DataFrame, col: str, time_format: str = '%d/%m/%Y') -> list:
        return [datetime.strptime(value[0], time_format) for value in df[[col]].values.tolist()]


def main(
        path,
        household,
        year_month
) -> None:
    transactions = Transactions(path, household, year_month)

    df = transactions.read_input(sep=';')
    df = transactions.preprocess(df)
    df = transactions.split_up_date(df)
    df = transactions.filter_on_month_of_interest(df)
    output_path = transactions.get_output_path(df)
    transactions.write_output(df, output_path, f'{year_month}_output.xlsx')
    print(f"Wrote output with {len(df)} rows for {year_month} to {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to update transactions')
    parser.add_argument('--path')
    parser.add_argument('--household', help='lisa_william or william', default='lisa_william')
    parser.add_argument('--year-month', help='yyyy-mm; latest full month', default='latest_month')
    args = parser.parse_args()
    main(
        path=args.path,
        household=args.household,
        year_month=args.year_month
    )
    logging.info('Done')
