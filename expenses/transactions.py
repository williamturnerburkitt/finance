import argparse
import io
import os
import logging
import csv
import typing

import arrow
from pathlib import Path

from constants.columns import AMOUNT, COUNTERPARTY, OPERATION, EXPENSE_DATE, CURRENCY_DATE, YEAR, MONTH, DAY, \
    LATEST_MONTH
from constants.drive import HOME, FAMILY, YEAR_MONTH, FILE_NAME


class Transactions:

    def __init__(self, household: str, year_month: str):
        self.household = household
        self.year_month = year_month
        self.path = f'{HOME}/{self.household}'

    def read_input(self, file_name: str, delimiter: str = ';') -> None:
        with open(f'../{self.path}/{self.year_month}/{file_name}') as transactions:

            self.ignore_useless_data(transactions)
            csv_reader = csv.DictReader(transactions, delimiter=delimiter)
            for row in csv_reader:
                print(row)
        logging.info(f'Read records from {self.path}.')
        return None
    
    @staticmethod
    def preprocess(df):
        df.columns = df.columns.str.lower()
        df[AMOUNT] = [amount.replace(',', '.') for amount in df.AMOUNT]
        df[OPERATION] = ['-' if '-' in amount else '+' for amount in df.AMOUNT]
        return df[[EXPENSE_DATE, COUNTERPARTY, AMOUNT, OPERATION]]
    
    def split_up_date(self, df):
        df[CURRENCY_DATE] = self.to_datetime_format(df, CURRENCY_DATE)
        df[YEAR] = [datum.year for datum in df[CURRENCY_DATE]]
        df[MONTH] = [datum.month for datum in df[CURRENCY_DATE]]
        df[DAY] = [datum.day for datum in df[CURRENCY_DATE]]
        return df.drop(CURRENCY_DATE, axis=1)

    def filter_on_month_of_interest(self, df):
        # date_of_interest = datetime.strptime(self.date_of_interest, '%Y-%m')
        # date_of_interest_month = date_of_interest.month

        return None
        # return df[df['month'] == date_of_interest_month]
    
    def get_output_path(self, df) -> str:
        latest_day = max(df['day'].values)
        month = df['month'].unique()[0]
        year = df['year'].unique()[0]
        latest_date = f'{year}-{month}-{latest_day}'
        return f'output/{self.household}/{latest_date}'

    @staticmethod
    def write_output(df, output_path: str, file_name: str) -> None:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        df.to_excel(f'{output_path}/{file_name}')
        logging.info(f'Wrote {df.count()} records to {output_path}.')
    
    # @staticmethod
    # def to_datetime_format(df: pd.DataFrame, col: str, time_format: str = '%d/%m/%Y') -> list:
    #     return [datetime.strptime(value[0], time_format) for value in df[[col]].values.tolist()]

    @staticmethod
    def ignore_useless_data(transactions: typing.TextIO) -> None:
        useless_data = True
        while useless_data:
            line = transactions.readline()
            if line == ';\n':
                useless_data = False


def main(
        year_month: str,
        household: str,
        file_name: str
) -> None:
    transactions = Transactions(household=household, year_month=year_month)
    df = transactions.read_input(file_name=file_name)
    # df = transactions.preprocess(df)
    # df = transactions.split_up_date(df)
    # df = transactions.filter_on_month_of_interest(df)
    # output_path = transactions.get_output_path(df)
    # transactions.write_output(df, output_path, f'{year_month}_output.xlsx')
    # logging.info(f"Wrote output with {len(df)} rows for {year_month} to {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to update transactions')
    parser.add_argument('--file_name', default=FILE_NAME)
    parser.add_argument('--household', default=FAMILY)
    parser.add_argument('--year_month', default=LATEST_MONTH)
    args = parser.parse_args()
    main(
        file_name=args.file_name,
        household=args.household,
        year_month=args.year_month
    )
