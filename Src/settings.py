from src.errors import error_proxy
from enum import Enum


class ReportFormat(Enum):
    CSV = 1
    Markdown = 2
    Json = 3

class settings:
    def __init__(self):
        self.__name = ""
        self.__inn = ""
        self.__check = ""
        self.__corr_check = ""
        self.__bik = ""
        self.__type_of_company = ""
        self.__first_start = True
        self.__report_format = ReportFormat.CSV  # Default report format

    @property
    def name_of_company(self):
        return self.__name

    @name_of_company.setter
    def name_of_company(self, value: str):
        if not isinstance(value.strip(), str):
            error_proxy.set_error(Exception("Некорректное наименование!"))

        self.__name = value.strip()

    @property
    def INN(self):
        return self.__inn

    @INN.setter
    def INN(self, value: str):
        if not isinstance(value.strip(), str) or len(value.strip()) != 12:
            error_proxy.set_error(Exception("Некорректный ИНН!"))

        self.__inn = value.strip()

    @property
    def check(self):
        return self.__check

    @check.setter
    def check(self, value: str):
        if not isinstance(value.strip(), str) or len(value.strip()) != 11:
            error_proxy.set_error(Exception("Некорректный счет!"))

        self.__check = value.strip()

    @property
    def corr_check(self):
        return self.__corr_check

    @corr_check.setter
    def corr_check(self, value: str):
        if not isinstance(value.strip(), str) or len(value.strip()) != 11:
            error_proxy.set_error(Exception("Некорректный корреспондентский счет!"))

        self.__corr_check = value.strip()

    @property
    def BIK(self):
        return self.__bik

    @BIK.setter
    def BIK(self, value: str):
        if not isinstance(value.strip(), str) or len(value.strip()) != 9:
            error_proxy.set_error(Exception("Некорректный БИК!"))

        self.__bik = value.strip()

    @property
    def type_of_company(self):
        return self.__type_of_company

    @type_of_company.setter
    def type_of_company(self, value: str):
        if not isinstance(value.strip(), str) or len(value.strip()) != 5:
            error_proxy.set_error(Exception("Некорректный вид собственности!"))

        self.__type_of_company = value.strip()

    @property
    def is_first_start(self):
        """
           Флаг Первый старт
        """
        return self._first_start

    @is_first_start.setter
    def is_first_start(self, value: bool):
        self._first_start = value

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: ReportFormat):
        self.__report_format = value
