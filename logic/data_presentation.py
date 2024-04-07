from abc import ABC
from src.settings import settings
from src.errors import exception_proxy, operation_exception

class convert(ABC):
    """ Настройки """
    __settings: settings = None
    """ Словарь с данными """
    __data: dict = {}
    """ Список полей """
    __fields = []

    def __init__(self, _settings: settings, _data: dict) -> None:

        """
        :param _settings: Настройки
        :param _data: Словарь с данными
        """

        exception_proxy.is_valide(_settings, settings)
        exception_proxy.is_valide(_data, dict)
        self.__data = _data
        self.__settings = _settings

        super(convert, self).__init__()


    def create(self, typeKey: str):
        """
            Сформировать отчет
        :param typeKey: тип данных
        :return:
        """
        exception_proxy.is_valide(typeKey, str)
        self.__fields = self.build(typeKey, self.__data)
        return ""

    @staticmethod
    def build(typeKey: str, data: dict) -> list:
        exception_proxy.is_valide(typeKey, str)
        if data is None:
            raise operation_exception("Набор данных некорректен")

        if len(data) == 0:
            raise operation_exception("Набор данных пуст")

        item = data[typeKey][0]

        result = list(filter(lambda x: not x.startswith("_") and not x.startswith("create_"), dir(item)))

        return result


    def _build(self, typeKey: str) -> list:
        """
            Предобработка возвращает набор полей класса TypeKey
        :param typeKey:
        :return:
        """
        return convert.build(typeKey, self.__data)

    @property
    def fields(self) -> list:
        """
        Набор полей
        :return: list
        """
        return self.__fields

    @property
    def data(self) -> dict:
        """
        Набор данных
        :return: dict
        """
        return self.__data

    def get_class_attributes(self, obj):
        """
        Получает список имен атрибутов класса
        """
        if obj is None:
            return []
        return [attr for attr in vars(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]