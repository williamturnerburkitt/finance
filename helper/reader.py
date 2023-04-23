from abc import ABC, abstractmethod
import itertools


class Reader(ABC):
    @abstractmethod
    def read(
            self,
            path: str,
            columns: list[str],
            delimiter: str = ';'
    ):
        pass

    @staticmethod
    def lowercase_header(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    @staticmethod
    def ignore_useless_data(transactions: typing.TextIO) -> None:
        useless_data = True
        while useless_data:
            line = transactions.readline()
            if line == ';\n':
                useless_data = False
