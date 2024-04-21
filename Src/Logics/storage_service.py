from Src.Logics.convert_factory import convert_factory
from Src.Logics.process_factory import process_factory
from Src.Logics.storage_prototype import storage_prototype
from Src.exceptions import argument_exception, exception_proxy, operation_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipe_model import receipe_model
from Src.Models.storage_model import storage_model
from Src.Models.receipe_row_model import receipe_row_model
from Src.Storage.storage import storage

from datetime import datetime
import json

from Src.settings import settings


class storage_service:
    __data = []
    __options = None
    __blocked = []

    def __init__(self, data: list) -> None:
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")

        self.__data = data
        prototype = storage_prototype(storage().data[storage.journal_key()])

    def __processing(self, data: list) -> list:
        """
            Сформировать обороты
        Args:
            data (list): _description_

        Returns:
            list: _description_
        """
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")

        # Подобрать процессинг
        key_turn = process_factory.turn_key()
        processing = process_factory().create(key_turn)

        # Обороты
        turns = processing().process(data)
        return turns

    # Набор основных методов

    def create_turns(self, start_period: datetime, stop_period: datetime) -> list:
        """
            Получить обороты за период
        Args:
            start_period (datetime): Начало
            stop_period (datetime): Окончание

        Returns:
            list: обороты за период
        """
        exception_proxy.validate(start_period, datetime)
        exception_proxy.validate(stop_period, datetime)

        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры!")

        # Фильтруем
        prototype = storage_prototype(self.__data)
        filter = prototype.filter_by_period(start_period, stop_period)

        return self.__processing(filter.data)

    def create_turns_by_nomenclature(self, start_period: datetime, stop_period: datetime,
                                     nomenclature: nomenclature_model) -> list:
        """
            Получить обороты за период по конкретной номенклатуры
        Args:
            start_period (datetime): Начало
            stop_period (datetime): Окончание
            nomenclature (nomenclature_model): Номенклатуры

        Returns:
            list: Обороты
        """
        exception_proxy.validate(start_period, datetime)
        exception_proxy.validate(stop_period, datetime)
        exception_proxy.validate(nomenclature, nomenclature_model)

        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры!")

        # Фильтруем
        prototype = storage_prototype(self.__data)
        filter = prototype.filter_by_period(start_period, stop_period)
        filter = filter.filter_by_nomenclature(nomenclature)
        if not filter.is_empty:
            raise operation_exception(f"Невозможно сформировать обороты по указанным данных: {filter.error}")

        return self.__processing(filter.data)

    def create_turns_only_nomenclature(self, nomenclature: nomenclature_model) -> list:
        """
            Получить обороты по номенклатуре
        Args:
            nomenclature (nomenclature_model): _description_

        Returns:
            list: Обороты
        """
        exception_proxy.validate(nomenclature, nomenclature_model)
        prototype = storage_prototype(self.__data)
        filter = prototype.filter_by_nomenclature(nomenclature)
        if not filter.is_empty:
            raise operation_exception(f"Невозможно сформировать обороты по указанным данных: {filter.error}")

        return self.__processing(filter.data)

    def create_turns_by_receipt(self, receipt: receipe_model) -> list:
        """
            Сформировать обороты по указанному рецепту
        Args:
            receipt (receipe_model): _description_

        Returns:
            list: _description_
        """
        exception_proxy.validate(receipt, receipe_model)

        if len(receipt.consist) == 0:
            raise operation_exception("Переданный рецепт некорректный. Не содержит в себе список номенклатуры!")

        # Отфильтровать по рецепту
        transactions = []
        filter = storage_prototype(self.__data)
        for item in receipt.rows():
            filter = filter.filter_by_nomenclature(item.nomenclature)
            if filter.is_empty:
                for transaction in filter.data:
                    transactions.append(transaction)

            filter.data = self.__data

        return self.__processing(transactions)

    def build_debits_by_receipt(self, receipt: receipe_model) -> list:
        """
            Сформировать проводки списания по рецепту
        Args:
            receipt (receipe_model): _description_

        Returns:
            list: _description_
        """
        exception_proxy.validate(receipt, receipe_model)

        if len(receipt.consist) == 0:
            raise operation_exception("Переданный рецепт некорректный. Не содержит в себе список номенклатуры!")

        turns = self.create_turns_by_receipt(receipt)
        if len(turns) <= 0:
            raise operation_exception("По указанному рецепту не найдеты обороты!")

        if len(receipt.rows()) > len(turns):
            raise operation_exception(
                "Невозможно сформировать список транзакций для списания т.к. нет достаточно остатков!")

        # Формируем список проводок на списание
        processing = process_factory().create(process_factory.debit_key())
        transactions = processing().process(receipt.rows())
        key = storage.storage_transaction_key()

        data = storage().data[key]
        for transaction in transactions:
            data.append(transaction)

    # Набор основных методов

    def data(self) -> list:
        """
            Получить отфильтрованные данные
        Returns:
            list: _description_
        """
        return self.__data

    @staticmethod
    def create_response(data: list, app):
        """"
            Сформировать данные для сервера
        """
        if app is None:
            raise argument_exception("Некорректно переданы параметры!")

        # Преоброзование
        data = convert_factory().serialize(data)
        json_text = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)

        # Подготовить ответ
        result = app.response_class(
            response=f"{json_text}",
            status=200,
            mimetype="application/json; charset=utf-8"
        )

        return result

    def create_blocked_turns(self):
        prototype = storage_prototype(storage().data[storage.journal_key()])
        transactions = prototype.filter_date(datetime(1999, 1, 1), self.__options.block_period)

        proces = process_factory()
        data = proces.create(storage.process_turn_key(), transactions.data)

        storage().data[storage.b_turn_key()] = data
        self.__blocked = data

        return data

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value: settings):
        if not isinstance(value, settings):
            raise argument_exception("неверный аргумент")
        self.__options = value

    # объединить обороты
    @staticmethod
    def _colide_turns(base_turns: list, added_turns: list):
        if len(added_turns) == 0:
            return base_turns

        for index, cur_base_turn in enumerate(base_turns):

            for aded_index, cur_added_turn in enumerate(added_turns):

                if cur_base_turn.nomenclature == cur_added_turn.nomenclature and cur_base_turn.storage_id == cur_added_turn.storage_id:
                    base_turns[index].amount += cur_added_turn.amount
                    added_turns.pop(aded_index)
                    break

        for cur_added_turn in added_turns:
            base_turns.append(cur_added_turn)
        return base_turns

    # получить обооты за период по номенклатуре
    def create_turns_by_nomenclature(self, start_date: datetime, finish_date: datetime, id: uuid.UUID) -> dict:

        if not isinstance(start_date, datetime) or not isinstance(finish_date, datetime):
            raise argument_exception("Неверный аргумент")

        if start_date > finish_date:
            raise argument_exception("Неверно переданы аргументы")

        prototype = storage_prototype(self.__data)

        transactions = prototype.filter_number_id(id)

        base = storage_prototype(self.__blocked).filter_number_id(id)

        reference = reference_conventor(nomenclature_model,
                                        error_proxy,
                                        nomenclature_group_model,
                                        range_model,
                                        storage_journal_row,
                                        storage_turn_model)

        proces = process_factory()

        data = proces.create(storage.process_turn_key(), transactions.data)

        data = self._colide_turns(base.data, data)

        result = {}
        for index, cur_tran in enumerate(data):
            result[index] = reference.convert(cur_tran)

        return result
