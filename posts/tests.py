from django.test import TestCase

from posts.singletons.config_manager import ConfigManager


class ConfigManagerTestCase(TestCase):
    def setUp(self):
        ConfigManager._instance = None

    def test_setting_persists_across_instances(self):
        cm1 = ConfigManager()
        cm1.set_setting("DEFAULT_PAGE_SIZE", 50)
        cm2 = ConfigManager()
        self.assertEqual(cm2.get_setting("DEFAULT_PAGE_SIZE"), 50)
