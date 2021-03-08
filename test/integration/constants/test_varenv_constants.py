"""Varenv constants unit test"""
import unittest
import dap_core_scc.utils.constants.varenv_constants as varenv_constants


class VarenvConstantsIntTest(unittest.TestCase):

    def test_constants(self):
        self.assertIsNotNone(varenv_constants.NAMESPACE)
        self.assertIsNotNone(varenv_constants.AD_CLIENT_ID)
        self.assertIsNotNone(varenv_constants.AD_VALIDATION_FIELD)
        self.assertIsNotNone(varenv_constants.API_PREFIX)
