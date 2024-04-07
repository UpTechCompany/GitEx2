import uuid
from abc import ABC
from src.errors import error_proxy, exception_proxy


class reference(ABC):
    __id = None
    __name = ""
    __description = ""
    __error = error_proxy()

    def __init__(self, name):
        __id = uuid.uuid4()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        exception_proxy.is_valide(value.strip(), str, 50)
        self.__name = value.strip()

    @staticmethod
    def create_dictionary(items: list):
        exception_proxy.is_valide(items, list)
        result = {}
        for position in items:
            result[position.name] = position

        return result

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        exception_proxy.is_valide(value.strip(), str)
        self.__description = value.strip()

    @property
    def id(self):
        return self.__id

    @property
    def is_error(self):
        return self.__error.error != ""

    @staticmethod
    def create_fields(source) -> list:
        result = list(filter(lambda x: not x.startswith("_") and not x.startswith("create_"), dir(source)))
        return result

    def __str__(self) -> str:
        return self.id









