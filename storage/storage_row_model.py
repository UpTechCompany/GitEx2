from datetime import datetime

from models.unit import unit_model
from models.nomenclature import nomenclature_model


class storage_row_model:
    def __init__(self):
        self.__storage_name = None
        self.__nomenclature = None
        self.__count = None
        self.__type_tranzaction = None
        self.__unit = None
        self.__period = None

    @property
    def storage_name(self):
        return self.__storage_name

    @storage_name.setter
    def storage_name(self, value: str):
        self.__storage_name = value

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        self.__nomenclature = value

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value: int):
        self.__count = value

    @property
    def type_tranzaction(self):
        return self.__type_tranzaction

    @type_tranzaction.setter
    def type_tranzaction(self, value: bool):
        self.__type_tranzaction = value

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, value: unit_model):
        self.__unit = value

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, value: datetime):
        self.__period = value