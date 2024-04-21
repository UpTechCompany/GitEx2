import json
import uuid
from Src.Models.nomenclature_model import nomenclature_model
from Src.exceptions import argument_exception


class nomenclature_service:
    __data = []

    # конструктор
    def __init__(self, data: list):

        if len(data) == 0:
            raise argument_exception("Wrong argument")

        self.__data = data

    # возвращаем массив с добавленной номенклатурой
    def add_nom(self, nom: nomenclature_model):
        self.__data.append(nom)
        return self.__data

    # ищем номенклатуру и меняем её
    def change_nome(self, nom: nomenclature_model):
        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == nom.id:
                self.__data[index] = nom
                break
        return self.__data

    # ищем по айди, удаляем, возвращаем массив
    def delete_nom(self, id: str):
        # при разных типах данных hash возвращает разные коды, поэтому переводим id в uuid и сравениваем
        id = uuid.UUID(id)

        res = False

        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == id:
                self.__data.pop(index)
                res = True
                break
        return self.__data, res

    @staticmethod
    def create_response(data: dict, app):

        if app is None:
            raise argument_exception()
        json_text = json.dumps(data)

        # Подготовить ответ
        result = app.response_class(
            response=f"{json_text}",
            status=200,
            mimetype="application/json; charset=utf-8"
        )

        return result