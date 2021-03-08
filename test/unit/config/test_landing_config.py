"""Varenv constants unit test"""
import unittest
import dap_core_landing.config.landing_config as LandingConfig


class LandingConfigTest(unittest.TestCase):

    def test_constants(self):
        self.assertIsNotNone(LandingConfig.PROPERTY_READER)
        self.assertIsNotNone(LandingConfig.LANDING_API_NAME)
