class StorageTypeModel:
    def __init__(self, type):
        if type not in ["Списание", "Поступление"]:
            raise ValueError("Invalid type. Must be 'Списание' or 'Поступление'.")
        self.__type = type

    @property
    def type(self):
        return self.__type



