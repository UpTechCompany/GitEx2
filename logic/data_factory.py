from logic.data_presentation import convert
from logic.formats.data_csv import csv_convert
from logic.formats.data_markdown import markdown_convert
from logic.formats.data_json import json_convert
from logic.formats.data_csv import csv_convert
from logic.formats.data_markdown import markdown_convert
from src.errors import exception_proxy, argument_exception, operation_exception
from storage.storage_model import storage_model

class process_factory:
    __maps = {}

    def __init__(self):
        self.__build_structure()

    def __build_structure(self):
        self.__maps["turn"] = storage_model

    def create(self, process_type: str, transactions: list):
        exception_proxy.is_valide(process_type, str)
        exception_proxy.is_valide(transactions, list)

        if not transactions:
            raise operation_exception("Список транзакций пуст")

        if process_type not in self.__maps.keys():
            raise operation_exception(f"Тип процесса {process_type} не поддерживается")

        process_class = self.__maps[process_type]
        result = process_class.process_storage_turn(transactions)

        return result