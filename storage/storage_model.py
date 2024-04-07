from datetime import datetime

from models.unit import unit_model
from models.nomenclature import nomenclature_model


class storage_model:
    def __init__(self):
        self.__storage_name = None
        self.__nomenclature = None
        self.__unit = None
        self.__period = None
        self.__address = None

    @property
    def storage_name(self):
        return self.__storage_name

    @storage_name.setter
    def storage_name(self, value: str):
        self.__storage_name = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        self.__nomenclature = value

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