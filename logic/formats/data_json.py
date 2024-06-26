from logic.data_presentation import convert
from src.errors import operation_exception
from src.reference import reference
import json

class json_convert(convert):

    def create(self, typeKey: str):
        super().create(typeKey)
        result = []

        # Исходные данные
        items = self.data[typeKey]
        if items == None:
            raise operation_exception("Невозможно сформировать данные. Данные не заполнены!")

        if len(items) == 0:
            raise operation_exception("Невозможно сформировать данные. Нет данных!")

        data = {}
        for item in items:
            for field in self.fields:
                value = getattr(item, field)
                data[field] = value

            result.append(data)

        data = json.dumps(result)
        return data

