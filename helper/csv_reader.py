import csv
import logging

from helper.reader import Reader


class CsvReader(Reader):
    def read(
            self,
            path: str,
            columns: list[str],
            delimiter: str = ';'
    ) -> list[dict]:

        with open(f'{path}') as transactions:
            self.ignore_useless_data(transactions)
            csv_reader = csv.DictReader(self.lowercase_header(transactions), delimiter=delimiter)
            result = [{col: row[col] for col in columns} for row in csv_reader]
        logging.info(f'Number of records read: {len(result)}.')
        return result
