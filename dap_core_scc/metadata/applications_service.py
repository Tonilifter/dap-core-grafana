"""Applications service module"""
import json
from dap_core_commons.logger.logging_utils import get_logger
from dap_core_commons.exceptions.custom_exception import CustomException
from dap_extractionmetadata_lib.db.sql.metadata.db_metadata import DbMetadata
from dap_extractionmetadata_lib.persistence.repository.landing_applications_repository \
    import LandingApplicationsRepository
from dap_extractionmetadata_lib.persistence.dto.landing_applications_dto import LandingApplicationsDTO
from dap_extractionmetadata_lib.utils.alchemy_encoder import AlchemyEncoder
import dap_core_landing.config.landing_config as LandingConfig


class ApplicationService:
    """Applications service with applications model utilities"""

    _LOGGER = get_logger(LandingConfig.LANDING_API_NAME)

    def __init__(self, property_reader=LandingConfig.PROPERTY_READER):
        self.property_reader = property_reader

    def _get_db_metadata(self):
        return DbMetadata(self.property_reader)

    def _check_application_exists(self, applications_repository, application_id):
        app_exists = applications_repository.get_by_id(application_id)
        if app_exists:
            return True

        return False

    def list_applications(self):
        """
        Get a list of landing applications
        :return: a tuple with boolean (successful or error) and a json string with list of
        landing applications or with the error detail.
        """
        db_metadata = None
        try:
            db_metadata = self._get_db_metadata()
            applications_repository = LandingApplicationsRepository(db_metadata.get_session())
            applications = applications_repository.list()

            if not applications:
                return True, json.dumps([])

            return True, AlchemyEncoder().to_json(applications)
        except CustomException as ex:
            self._LOGGER.error(f"Error obtaining applications from metadata db: {ex}")
            status = {
                "error": 500,
                "error_detail": "Error obtaining applications from metadata db"
            }
            return False, json.dumps(status)
        finally:
            if db_metadata:
                db_metadata.close_db()

    def create_application(self, application):
        """
        Create a new landing application
        :param application: application model
        :return: a tuple with boolean (successful or error) and a json string with new application or
        with the error detail.
        """
        db_metadata = None
        try:
            db_metadata = self._get_db_metadata()
            applications_repository = LandingApplicationsRepository(db_metadata.get_session())

            app_id = application['application_id']

            if self._check_application_exists(applications_repository, app_id):
                status = {
                    "error": 400,
                    "error_detail": "Application id already exists"

                }
                self._LOGGER.error(f"Error creating application, the application_id"
                                   f" {app_id} already exists")
                return False, json.dumps(status)

            application_dto = LandingApplicationsDTO(
                application_id=app_id,
                name=application['name'],
                description_es=application['description_es'],
                url=application['url'],
                active=application['active'],
                description_en=application['description_en'],
                tags=application['tags']
            )

            application_created = applications_repository.create(application_dto)

            return True, AlchemyEncoder().to_json(application_created)
        except CustomException as ex:
            self._LOGGER.error(f"Error creating application: {ex}")
            status = {
                "error": 500,
                "error_detail": "Error creating application"
            }
            return False, json.dumps(status)
        finally:
            if db_metadata:
                db_metadata.close_db()

    def modify_application(self, application_id, application):
        """
        Modify a landing application
        :param application_id: application identifier
        :param application: application model
        :return: a tuple with boolean (successful or error) and a json string with new application values or
        with the error detail.
        """
        db_metadata = None
        try:
            db_metadata = self._get_db_metadata()
            applications_repository = LandingApplicationsRepository(db_metadata.get_session())

            if not self._check_application_exists(applications_repository, application_id):
                status = {
                    "error": 404,
                    "error_detail": "Application id not found"
                }

                return False, json.dumps(status)

            application_dto = LandingApplicationsDTO(
                application_id=application_id,
                name=application['name'],
                description_es=application['description_es'],
                url=application['url'],
                active=application['active'],
                description_en=application['description_en'],
                tags=application['tags']
            )

            application_modified = applications_repository.update(application_dto)

            return True, AlchemyEncoder().to_json(application_modified)
        except CustomException as ex:
            self._LOGGER.error(f"Error modifying application: {ex}")
            status = {
                "error": 500,
                "error_detail": "Error modifying application"
            }
            return False, json.dumps(status)
        finally:
            if db_metadata:
                db_metadata.close_db()

    def delete_application(self, application_id):
        """
        Delete a landing application
        :param application_id: application identifier
        :return: a tuple with boolean (successful or error) and the error detail.
        """
        db_metadata = None
        try:
            db_metadata = self._get_db_metadata()
            applications_repository = LandingApplicationsRepository(db_metadata.get_session())

            if not self._check_application_exists(applications_repository, application_id):
                status = {
                    "error": 404,
                    "error_detail": "Application id not found"
                }

                return False, json.dumps(status)

            applications_repository.delete(application_id)

            return True, json.dumps({})
        except CustomException as ex:
            self._LOGGER.error(f"Error deleting application: {ex}")

            status = {
                "error": 500,
                "error_detail": "Error deleting application"
            }

            return False, json.dumps(status)
        finally:
            if db_metadata:
                db_metadata.close_db()
