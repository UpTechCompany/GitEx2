import unittest
from unittest.mock import patch
from Src.settings_manager import settings_manager


class TestSettingsManager(unittest.TestCase):

    def test_save_settings_manager(self):
        manager = settings_manager()
        s = manager.settings
        manager.settings.name = "Test Companys"
        manager.settings.inn = "1234567890123"
        manager.save()

        assert s == manager.settings