"""Swagger constants unit test"""
import unittest
import dap_core_landing.utils.constants.swagger_constants as swagger_constants


class SwaggerConstantsIntTest(unittest.TestCase):

    def test_constants(self):
        self.assertIsNotNone(swagger_constants.APPLICATIONS_SWAGGER_MODEL_DOC)
        self.assertIsNotNone(swagger_constants.APPLICATIONS_SWAGGER_MODEL_NAME)
        self.assertIsNotNone(swagger_constants.ERROR_SWAGGER_MODEL_DOC)
        self.assertIsNotNone(swagger_constants.ERROR_SWAGGER_MODEL_NAME)
        self.assertIsNotNone(swagger_constants.STATUS_SWAGGER_MODEL_DOC)
        self.assertIsNotNone(swagger_constants.STATUS_SWAGGER_MODEL_NAME)
