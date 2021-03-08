"""Applications service unit test"""
import unittest
import json
import copy
from unittest.mock import patch
from mock import MagicMock

from dap_extractionmetadata_lib.persistence.dto.landing_applications_dto \
    import LandingApplicationsDTO, LandingApplications
from dap_extractionmetadata_lib.utils.alchemy_encoder import AlchemyEncoder

from dap_core_landing.metadata.applications_service import ApplicationService
from dap_core_commons.logger.logging_utils import get_logger


class ApplicationServiceTest(unittest.TestCase):
    """Applications service unit test"""

    _LOGGER = get_logger("landing_api_tests")

    _APP_1 = LandingApplications(application_id="sample_app", name="SampleApp",
                                 description="Sample Application", description_en="Sample Application",
                                 url="http://app.repsol.com", active=True, tags="tag1,tag2")
    _APP_2 = LandingApplications(application_id="sample_app2", name="SampleApp2",
                                 description="Sample Application 2", description_en="Sample Application 2",
                                 url="http://app.repsol.com", active=True, tags="tag1,tag2")
    _APP_LIST = [_APP_1, _APP_2]

    _SESSION_MOCK = MagicMock()

    _METADATA_DB_MOCK = MagicMock()
    _METADATA_DB_MOCK.get_session.return_value = _SESSION_MOCK

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    def test_list_applications(self, _):
        self._SESSION_MOCK.query.return_value.order_by.return_value = self._APP_LIST

        app_service = ApplicationService()
        result, applications = app_service.list_applications()
        app_1_dto = LandingApplicationsDTO()
        app_1_dto.from_orm(self._APP_1)
        app_2_dto = LandingApplicationsDTO()
        app_2_dto.from_orm(self._APP_2)
        expected_result = AlchemyEncoder().to_json([app_1_dto, app_2_dto])

        self.assertTrue(result)
        self.assertIsNotNone(applications)
        self.assertTrue(len(applications) > 0)
        self.assertEqual(expected_result, applications)
        self._LOGGER.info(f"test_list_applications OK got applications: {applications}")

    def test_list_applications_error(self):
        app_service = ApplicationService()
        result, err_detail = app_service.list_applications()
        self.assertFalse(result)
        expected_result = {
            "error": 500,
            "error_detail": "Error obtaining applications from metadata db"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_list_applications_error OK, raises expected error")

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    @patch.object(ApplicationService, '_check_application_exists', return_value=False)
    def test_create_application(self, _, __):
        self._SESSION_MOCK.add.return_value = None
        self._SESSION_MOCK.commit.return_value = None
        self._SESSION_MOCK.query.return_value.filter.return_value.first.return_value = self._APP_1

        app_service = ApplicationService()
        app_1_dto_new = LandingApplicationsDTO()
        app_1_dto_new.from_orm(self._APP_1)

        new_app = {
            "application_id": app_1_dto_new.application_id,
            "name": app_1_dto_new.name,
            "description_es": app_1_dto_new.description_es,
            "url": app_1_dto_new.url,
            "active": app_1_dto_new.active,
            "description_en": app_1_dto_new.description_en,
            "tags": app_1_dto_new.tags
        }

        result, application = app_service.create_application(new_app)

        app_1_dto = LandingApplicationsDTO()
        app_1_dto.from_orm(self._APP_1)
        expected_result = AlchemyEncoder().to_json(app_1_dto_new)

        self.assertTrue(result)
        self.assertIsNotNone(application)
        self.assertEqual(expected_result, application)
        self._LOGGER.info(f"test_create_application OK new application: {application}")

    def test_create_application_error(self):
        app_service = ApplicationService()
        result, err_detail = app_service.create_application(None)
        self.assertFalse(result)
        expected_result = {
            "error": 500,
            "error_detail": "Error creating application"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_create_application_error OK, raises expected error")

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    @patch.object(ApplicationService, '_check_application_exists', return_value=True)
    def test_create_application_already_exists_error(self, _, __):
        app_1_dto_new = LandingApplicationsDTO()
        app_1_dto_new.from_orm(self._APP_1)

        app_service = ApplicationService()
        new_app = {
            "application_id": app_1_dto_new.application_id,
            "name": app_1_dto_new.name,
            "description_es": app_1_dto_new.description_es,
            "url": app_1_dto_new.url,
            "active": app_1_dto_new.active,
            "description_en": app_1_dto_new.description_en,
            "tags": app_1_dto_new.tags
        }
        result, err_detail = app_service.create_application(new_app)
        self.assertFalse(result)
        expected_result = {
            "error": 400,
            "error_detail": "Application id already exists"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_create_application_already_exists_error OK, raises expected error")

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    def test_modify_application(self, _):
        self._SESSION_MOCK.commit.return_value = None
        self._SESSION_MOCK.query.return_value.filter.return_value.update.return_value = None

        modify_desc = "modify_desc"
        app_modified = copy.copy(self._APP_1)
        app_modified.description_es = modify_desc
        self._SESSION_MOCK.query.return_value.filter.return_value.first.return_value = self._APP_1

        app_service = ApplicationService()

        app_updtd_dto = LandingApplicationsDTO()
        app_updtd_dto.from_orm(app_modified)

        app_updtd = {
            "application_id": app_updtd_dto.application_id,
            "name": app_updtd_dto.name,
            "description_es": modify_desc,
            "url": app_updtd_dto.url,
            "active": app_updtd_dto.active,
            "description_en": app_updtd_dto.description_en,
            "tags": app_updtd_dto.tags
        }

        result, application = app_service.modify_application(self._APP_1.application_id,
                                                             app_updtd)

        app_1_dto = LandingApplicationsDTO()
        app_1_dto.from_orm(app_modified)
        app_1_dto.description_es = modify_desc

        expected_result = AlchemyEncoder().to_json(app_updtd_dto)

        self.assertTrue(result)
        self.assertIsNotNone(application)
        self.assertEqual(expected_result, application)
        self._LOGGER.info(f"test_update_application OK new application: {application}")

    def test_modify_application_error(self):
        app_service = ApplicationService()
        result, err_detail = app_service.modify_application(None, None)
        self.assertFalse(result)
        expected_result = {
            "error": 500,
            "error_detail": "Error modifying application"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_modify_application_error OK, raises expected error")

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    def test_modify_application_not_found(self, _):
        self._SESSION_MOCK.query.return_value.filter.return_value.first.return_value = None

        app_service = ApplicationService()
        result, err_detail = app_service.modify_application("application_id", None)

        self.assertFalse(result)
        expected_result = {
            "error": 404,
            "error_detail": "Application id not found"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_modify_application_not_found OK, raises expected error")

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    def test_delete_application(self, _):
        self._SESSION_MOCK.commit.return_value = None
        self._SESSION_MOCK.query.return_value.filter.return_value.delete.return_value = None
        self._SESSION_MOCK.query.return_value.filter.return_value.first.return_value = self._APP_1

        app_service = ApplicationService()
        result, result = app_service.delete_application(self._APP_1.application_id)
        expected_result = AlchemyEncoder().to_json({})

        self.assertTrue(result)
        self.assertIsNotNone(result)
        self.assertEqual(expected_result, result)
        self._LOGGER.info(f"test_delete_application OK")

    def test_delete_application_error(self):
        app_service = ApplicationService()
        result, err_detail = app_service.delete_application(None)
        self.assertFalse(result)
        expected_result = {
            "error": 500,
            "error_detail": "Error deleting application"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_delete_application_error OK, raises expected error")

    @patch.object(ApplicationService, '_get_db_metadata', return_value=_METADATA_DB_MOCK)
    def test_delete_application_not_found(self, _):
        self._SESSION_MOCK.query.return_value.filter.return_value.first.return_value = None

        app_service = ApplicationService()
        result, err_detail = app_service.delete_application("application_id")

        self.assertFalse(result)
        expected_result = {
            "error": 404,
            "error_detail": "Application id not found"
        }
        self.assertEqual(json.dumps(expected_result), err_detail)
        self._LOGGER.info("test_delete_application_not_found OK, raises expected error")
