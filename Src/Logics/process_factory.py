from Src.Logics.processing import processing
from Src.Logics.turn_processing import turn_processing
from Src.Models.storage_row_model import storage_row_turn_model
from Src.exceptions import exception_proxy, argument_exception, operation_exception
from Src.Logics.debit_processing import debit_processing


#
# Фабрика процессов обработки складских транзакций
#
class process_factory:
    __maps = {}

    def __init__(self) -> None:
        self.__build_structure()

    def __build_structure(self):
        """
            Сформировать структуру
        """
        self.__maps[process_factory.turn_key()] = turn_processing
        self.__maps[process_factory.debit_key()] = debit_processing

    @staticmethod
    def process_storage_turn(journal: list):
        if not isinstance(journal, list):
            raise argument_exception("Неверный аргумент")

        if len(journal) == 0:
            return []

        if not isinstance(journal[0], storage_row_turn_model):
            raise argument_exception("Неверный массив")

        result = {}

        for cur_line in journal:
            # айди склада и имя номенклатуры, для того чтобы рассортировать строки складского журнала
            key = cur_line.nomenclature.name + ' ' + str(cur_line.storage_id)
            keys = list(result.keys())

            koef = 1 - 2 * (cur_line.operation_type == "delete")

            if key in keys:
                result[key].amount += cur_line.amount * koef
            else:

                # в turnmodel хранятся данные о складе, а также  количестве,  типе и единицах измерения номенклатуры
                result[key] = turn_processing.create_turn(cur_line.storage_id, cur_line.amount * koef,
                                                          cur_line.nomenclature, cur_line.nomenclature.ran_mod)

        # по требованию задания мы возвращаем список, поэтому list(result.values())
        return list(result.values())

    def create(self, process_key: str) -> processing:
        """
            Подобрать нужный процессинг
        Args:
            process_key (str): Ключ
            data (list[storage_row_model]): Исходные данные
        Returns:
            processing: нужный процессинг
        """
        exception_proxy.validate(process_key, str)
        if process_key not in self.__maps.keys():
            raise argument_exception(f"Указанный процесс {process_key} не реализован!")

        current_processing = self.__maps[process_key]
        if current_processing is None:
            raise operation_exception("Некорректно сконфигурирована текущая фабрика!")

        return current_processing

    # Статические методы

    @staticmethod
    def turn_key() -> str:
        """
            Сформировать обороты
        Returns:
            str: _description_
        """
        return "turns"

    @staticmethod
    def debit_key() -> str:
        """
            Сформировать проводки списания
        Returns:
            str: _description_
        """
        return "debits"

        # Код взят: https://github.com/UpTechCompany/GitExample/blob/6665bc70c4933da12f07c0a0d7a4fc638c157c40/storage/storage.py#L30

    @staticmethod
    def process_keys(cls):
        """
            Получить список ключей
        Returns:
            _type_: _description_
        """
        keys = []
        methods = [getattr(cls, method) for method in dir(cls) if callable(getattr(cls, method))]
        for method in methods:
            if method.__name__.endswith("_key") and callable(method):
                keys.append(method())
        return keys