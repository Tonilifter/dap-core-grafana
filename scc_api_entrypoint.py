"""Landing Back API Entrypoint"""
import json
import requests

from dap_core_commons.azure.active_directory_utils import get_token_from_service_principal
from dap_core_commons.azure.service_principal_service import ServicePrincipalService
from dap_core_commons.utils.core_utils import CoreUtils
from waitress import serve
from flask import Flask, request, Response
from flask_cors import CORS
from flask_restplus import Resource, fields

from dap_core_commons.logger.logging_utils import get_logger
from dap_core_commons.server.server_utils import ServerUtils
from dap_core_commons.property.property_reader import PropertyReader
from dap_core_commons.swagger.custom_swagger_api import CustomSwaggerApi
from dap_core_commons.auth.token_utils import token_required
from dap_core_commons.azure.key_vault_service import KeyVaultService
from dap_core_commons.azure.service_principal_utils import ServicePrincipalUtils
from dap_core_commons.exceptions.configuration_exception import ConfigurationException
from dap_excelpreprocessor_lib.config.validate_config import ValidateConfig

import dap_core_scc.utils.constants.varenv_constants as VarenvConstants
import dap_core_scc.utils.constants.swagger_constants as SwaggerConstants
import dap_core_scc.config.landing_config as SccConfig


app = Flask(__name__)
CORS(app)

_LOGGER = get_logger(SccConfig.SSC_API_NAME)

_PROPERTY_READER = PropertyReader(SccConfig.PROPERTY_READER)
_API_PREFIX = _PROPERTY_READER.get_property(VarenvConstants.API_PREFIX)
_NAMESPACE = _PROPERTY_READER.get_property(VarenvConstants.NAMESPACE)

_DEFAULT_PORT = 80

_MIMETYPE = "application/json"

_SP_EXTRACT = "extract"

base_path = ""
if _API_PREFIX:
    if not _API_PREFIX.startswith('/'):
        base_path += "/"
    base_path += _API_PREFIX

app.config['SWAGGER_BASEPATH'] = base_path

authorization = {
    'bearerToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

app_server = CustomSwaggerApi(app, version="1.0.0",
                              title="Core Scc Web Back API",
                              description="Core Ssc Web Back API",
                              validate=True,
                              authorizations=authorization)

apps_ns = app_server.namespace("applications", description="Service Components Catalog Applications endpoint")
status_ns = app_server.namespace("status", description="API Status")
metrics_ns = app_server.namespace("metrics", description="API Metrics")

app_model = app_server.model(SwaggerConstants.APPLICATIONS_SWAGGER_MODEL_NAME,
                             SwaggerConstants.APPLICATIONS_SWAGGER_MODEL_DOC)
err_model = app_server.model(SwaggerConstants.ERROR_SWAGGER_MODEL_NAME,
                             SwaggerConstants.ERROR_SWAGGER_MODEL_DOC)
status_model = app_server.model(SwaggerConstants.STATUS_SWAGGER_MODEL_NAME,
                                SwaggerConstants.STATUS_SWAGGER_MODEL_DOC)
loganalytics_response_model = app_server.model(SwaggerConstants.LOGANALYTICS_SWAGGER_MODEL_NAME,
                                               SwaggerConstants.LOGANALYTICS_SWAGGER_MODEL_DOC)
governance_response_model = app_server.model(SwaggerConstants.GOVERNANCE_SWAGGER_MODEL_NAME,
                                             SwaggerConstants.GOVERNANCE_SWAGGER_MODEL_DOC)
devops_columns_model = app_server.model(SwaggerConstants.DEVOPS_COLUMNS_SWAGGER_MODEL_NAME,
                                        SwaggerConstants.DEVOPS_COLUMNS_SWAGGER_MODEL_DOC)
devops_workitems_model = app_server.model(SwaggerConstants.DEVOPS_WORKITEMS_SWAGGER_MODEL_NAME,
                                          SwaggerConstants.DEVOPS_WORKITEMS_SWAGGER_MODEL_DOC)
devops_features_model = app_server.model(SwaggerConstants.DEVOPS_FEATURES_SWAGGER_MODEL_NAME,
                                         SwaggerConstants.DEVOPS_FEATURES_SWAGGER_MODEL_DOC)
devops_response_model = app_server.model("DevOps Response",
                                    {
                                        'queryType': fields.String(
                                            title='queryType',
                                            description=f"queryType",
                                            example='flat'),
                                        'queryResultType': fields.String(
                                            title='queryResultType',
                                            description=f"queryResultType",
                                            example='workItem'),
                                        'asOf': fields.String(
                                            title='asOf',
                                            description=f"asOf",
                                            example='2020-01-01T00:00:00.000Z'),
                                        'columns': fields.Nested(devops_columns_model, as_list=True),
                                        'workItems': fields.Nested(devops_workitems_model, as_list=True),
                                    })

headers_parser = app_server.parser()
headers_parser.add_argument('Authorization', location='headers')


def _get_kv_secret(kv_name, secret_name):
    kv_service = KeyVaultService(None, kv_name, SccConfig.PROPERTY_READER)

    return kv_service.get_secret_value(secret_name)


_LANDING_SP_SECRET_NAME = ServicePrincipalUtils.get_id_kv_secret_name("landing")
_AD_CLIENT_ID = _get_kv_secret(f"{_NAMESPACE}corekv", _LANDING_SP_SECRET_NAME)


@status_ns.route("")
class StatusEndpoint(Resource):
    """
    Endpoint to return an ok status
    :return: a 200 message with status ok
    """

    @status_ns.doc("Status")
    @app_server.response(200, 'Success', status_model)
    @app_server.response(500, 'Internal server error', err_model)
    def get(self):
        """
        Endpoint to return an ok status
        :return: a 200 code with json message with status up!
        """
        _LOGGER.info(f"{request.path} - {request.method}")
        property_list = [VarenvConstants.NAMESPACE]
        secret_list = [_LANDING_SP_SECRET_NAME]
        try:
            ValidateConfig().validate(property_list=property_list, secret_names=secret_list,
                                      check_metadata_db=True)
            return ServerUtils.get_status_response()
        except ConfigurationException as ex:
            _LOGGER.error(ex)
            error_detail = {
                "error": 500,
                "error_detail": "Error initializing api configuration, retry"
                                " and if problem persists contact with a administrator"
            }

            return ServerUtils.get_error_response(
                500, error_detail)


@metrics_ns.route("/devops/featuredetails")
class FeatureDetailsEndpoint(Resource):

    @token_required(ad_client_id=_AD_CLIENT_ID)
    @apps_ns.doc('Get details from a specific feature', security='bearerToken')
    @app_server.response(200, 'Success', app_model)
    @app_server.response(400, 'Error on request body')
    @app_server.response(403, 'Authorization header is wrong/expired')
    @app_server.response(404, 'Application not found', err_model)
    @app_server.response(500, 'General error modifying application', err_model)
    def get(self):
        """
        Return details about a feature through query to DevOps API
        :return: Details about a feature
        """
        _LOGGER.info(f"{request.path} - {request.method} - Querying feature details")
        tenant_id = CoreUtils.get_tenant_id(SccConfig.PROPERTY_READER)
        sp_service = ServicePrincipalService(SccConfig.PROPERTY_READER)
        sp = sp_service.get_service_principal_for_sp_name(tenant_id, _SP_EXTRACT)
        url = f"https://coreutils{_NAMESPACE}akcore.cloudapp.repsol.com/" \
              f"dap-core-extraction-utils/metrics/devops/featuredetails"
        token = get_token_from_service_principal(service_principal=sp)
        headers = {
            'Authorization': f"Bearer {token}"
        }

        result = requests.get(url, headers=headers)

        return Response(response=result,
                        status=result.status_code,
                        mimetype=_MIMETYPE)


if __name__ == "__main__":
    host = f'*:{_DEFAULT_PORT}'
    _LOGGER.info(f"Starting service component catalog api on {host}")
    serve(app, listen=host)
