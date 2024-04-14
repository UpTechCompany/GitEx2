from datetime import datetime

from Src.exceptions import exception_proxy


#
# Класс для описания настроек
#
class settings():
    _inn = 0
    _short_name = ""
    _first_start = True
    _mode = "csv"
    _block_period = None

    @property
    def data(self):
        return {
            "inn": self._inn,
            "short_name": self._short_name,
            "first_start": self._first_start,
            "mode": self._mode,
            "block_period": self._block_period
        }

    @property
    def inn(self):
        """
            ИНН
        Returns:
            int:
        """
        return self._inn

    @inn.setter
    def inn(self, value):
        if value.isdigit():
            self._inn = int(value)

    @property
    def short_name(self):
        """
            Короткое наименование организации
        Returns:
            str:
        """
        return self._short_name

    @short_name.setter
    def short_name(self, value: str):
        exception_proxy.validate(value, str)
        self._short_name = value

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
    def report_mode(self):
        """
            Режим построения отчетности
        Returns:
            _type_: _description_
        """
        return self._mode

    @report_mode.setter
    def report_mode(self, value: str):
        exception_proxy.validate(value, str)

        self._mode = value

    @property
    def block_period(self):
        return self._block_period

    @block_period.setter
    def block_period(self, value: datetime):
        if not isinstance(value, datetime):
            raise Exception("Некорректная дата блокировки!")

        self._block_period = value
