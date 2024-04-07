from logic.data_presentation import convert

class csv_convert(convert):

    def create(self, typeKey: str):
        super().create(typeKey)

        result = ""

        items = list(self.data[typeKey])

        # Создаем заголовок CSV
        class_attributes = self.get_class_attributes(items[0]) if items else []
        result += ",".join(attr.split('_')[-1] for attr in class_attributes) + "\n"

        # Заполняем CSV данными
        for item in items:
            values = [str(getattr(item, attr)) for attr in class_attributes]
            result += ",".join(values) + "\n"

        return result


