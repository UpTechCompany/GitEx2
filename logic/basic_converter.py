from logic.data_presentation import convert
from datetime import datetime
from logic.data_factory import data_factory
from src.errors import argument_exception
class basic_convertor(convert):

    def convert(self, field: str, object) -> dict:
        super().create(field, object)

        if not isinstance(object, (int, str, bool)):
            self.error = f"Некорректный тип данных передан для конвертации: {type(object)}"
            return None
        try:
            return {field: object}
        except Exception as ex:
            self.error.set_error(ex)
        return None

class datetime_convertor(convert):
    def convert(self, field: str,  obj):
        if isinstance(obj, datetime.datetime):
            return {"datetime_value": obj.strftime("%Y-%m-%d %H:%M:%S")}
        else:
            raise argument_exception("Ошибка типа данных!")


class reference_convertor(convert):
    def convert(self, field: str, object) -> dict:
        factory = data_factory()
        return factory.create(object)