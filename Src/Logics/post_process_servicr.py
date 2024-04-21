from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import sys

sys.path.append(os.path.join(Path(__file__).parent, 'src'))

from Src.errors import error_proxy
from pathlib import Path
from Src.Storage import storage

from Src.Logics.storage_prototype import storage_prototype
from Src.Logics.json_reporting import json_reporting
from Src.exceptions import argument_exception
from Src.Logics.process_factory import process_factory
from Src.Logics.storage_observer import storage_observer
from Src.Models.event_type import event_type
from Src.Logics.storage_service import storage_service


# PERENESTI I ZAMENIT MAIN

class post_processing_service(storage_service):
    __nomenclature = None
    __storage = None

    def __init__(self, data: list):
        super().__init__(data)
        self.__storage = storage()
        storage_observer.observers.append(self)

    @property
    def nomenclature_id(self):
        return self.__nomenclature

    @nomenclature_id.setter
    def nomenclature_id(self, nom_id: uuid.UUID):
        if not isinstance(nom_id, uuid.UUID):
            raise argument_exception("неверный тип аргумента")
        storage_observer.observers.append(self)
        self.__nomenclature = nom_id

    def handle_event(self, handle_type: str):
        super().handle_event(handle_type)

        if handle_type == event_type.deleted_nomenclature():
            self.clear_reciepe()
            self.clear_journal()

    def clear_reciepe(self):

        key = storage.reciepe_key()
        for index, cur_rec in enumerate(self.__storage.data[key]):
            for cur_id in list(cur_rec.ingridient_proportions.keys()):
                print(cur_id == self.__nomenclature)
                if self.__nomenclature == cur_id:
                    res = cur_rec.ingridient_proportions
                    res.pop(self.__nomenclature)
                    storage().data[key][index].ingridient_proportions = res

    def clear_journal(self):
        key = storage.journal_key()
        res = []
        for cur_line in (self.__storage.data[key]):
            if cur_line.nomenclature.id != self.__nomenclature:
                res.append(cur_line)

        self.__storage.data[key] = res
        storage_observer.raise_event(event_type.changed_block_period())