from src.reference import reference
from models.nomenclature import nomenclature_model
from models.unit import unit_model
from storage.storage_model import storage_model
from storage.storage_type_model import StorageTypeModel

class StorageTransactionModel(reference):
    def __init__(self):
        super().__init__()
        self._date = None
        self._quantity = 0
        self._operation_type = None
        self._stock = None
        self._units = None
        self._nomenclature = None
        self._period = None

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def operation_type(self):
        return self._operation_type

    @operation_type.setter
    def operation_type(self, value):
        self._operation_type = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    @property
    def nomenclature(self):
        return self._nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        self._nomenclature = value
