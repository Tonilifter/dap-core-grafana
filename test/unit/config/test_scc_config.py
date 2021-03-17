"""Varenv constants unit test"""
import unittest
import dap_core_scc.config.scc_config as SccConfig


class SccConfigTest(unittest.TestCase):

    def test_constants(self):
        self.assertIsNotNone(SccConfig.PROPERTY_READER)
        self.assertIsNotNone(SccConfig.SCC_API_NAME)
