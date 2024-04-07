import os
import json
import uuid

from src.settings import settings
from src.errors import error_proxy, exception_proxy


class settings_manager(object):
    # Наименование файла по умолчанию
    __settings_file_name = "settings.json"
    # Словарь с исходными данными
    __data = None
    # Внутренний уникальный номер
    __uniqueNumber = None
    # Данные с настройками
    __settings = None
    # Описание ошибок
    __error = error_proxy()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.__uniqueNumber is None:
            self.__uniqueNumber = uuid.uuid4()
            self.opener(self.__settings_file_name)

            # После загрузки создаем объект класса settings
            self.__settings = settings()
            self.__load()

    @property
    def unique_number(self):
        return self.__uniqueNumber

    def __open(self):
        """
            Открыть файл с настройками
        """
        file_path = os.path.split(__file__)
        settings_file = "%s/%s" % (file_path[0], self.__settings_file_name)
        if not os.path.exists(settings_file):
            self.__error.set_error(Exception("ERROR: Невозможно загрузить настройки! Не найден файл %s", settings_file))

        try:
            with open(settings_file, "r") as read_file:
                self.__data = json.load(read_file)
        except:
            self.__error.set_error(Exception("ERROR: Невозможно загрузить настройки! Не найден файл %s", settings_file))

    def opener(self, file_name: str):
        """
            Открыть файл с настройками
        Args:
            file_name (str):
        """
        exception_proxy.is_valide(file_name, str)

        self._settings_file_name = file_name
        self.__open()
        self.__load()

    def __load(self):
        """
            Private: Загрузить словарь в объект
        """

        if len(self.__data) == 0:
            return

        # Список полей от типа назначения
        fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.__class__)))

        # Заполняем свойства
        for field in fields:
            keys = list(filter(lambda x: x == field, self.__data.keys()))
            if len(keys) != 0:
                value = self.__data[field]

                # Если обычное свойство - заполняем.
                if not isinstance(value, list) and not isinstance(value, dict):
                    setattr(self.__settings, field, value)

    @property
    def settings(self) -> settings:
        """
            Текущие настройки в приложении
        Returns:
            settings: _
        """
        return self.__settings

    @property
    def data(self):
        """
            Словарь, который содержит данные из настроек
        Returns:
            dict:
        """
        return self.__data

    @property
    def error(self) -> error_proxy:
        """
            Текущая информация об ошибке
        Returns:
            error_proxy:
        """
        return self.__error