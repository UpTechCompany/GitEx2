from datetime import datetime
from src.reference import reference
from src.errors import error_proxy, exception_proxy
from src.reference import reference
from src.settings_manager import settings_manager
from logic.basic_converter import basic_convertor, datetime_convertor, reference_convertor
from src.errors import operation_exception
class convert_factory:
    __maps = {}

    def __init__(self):
        self.__maps[datetime] = datetime_convertor
        self.__maps[dict] = basic_convertor
        self.__maps[int] = basic_convertor
        self.__maps[str] = basic_convertor
        self.__maps[bool] = basic_convertor

        for inheritor in reference.__subclasses__():
            self.__maps[inheritor] = reference_convertor

    def convert(self, object):
        result = self.__convert_list("data", object)
        if result is not None:
            return result

        result = {}
        fields = reference.create_fields(object)

        for field in fields:
            attribute = getattr(object.__class__, field)
            if isinstance(attribute, property):
                value = getattr(object, field)

                dictionary = self.__convert_list(field, value)
                if dictionary is None:
                    dictionary = self.__convert_item(field, value)

                if len(dictionary) == 1:
                    result[field] = dictionary[field]
                else:
                    result[field] = dictionary

        return result

    def __convert_item(self, field: str, source):
        exception_proxy.is_valide(field, str)
        if source is None:
            return {field: None}

        if type(source) not in self.__maps.keys():
            raise operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}")

        convertor = self.__maps[type(source)]()
        dictionary = convertor.convert(field, source)

        if not convertor.is_empty:
            raise operation_exception(f"Ошибка при конвертации данных {convertor.error}")

        return dictionary

    def __convert_list(self, field: str, source):
        exception_proxy.is_valide(field, str)
        if not isinstance(source, list):
            return None

        items = []
        for item in source:
            items.append(self.__convert_item(field, item))

        return items