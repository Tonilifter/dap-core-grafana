"""Flask restplus swagger api documentation constants"""
from flask_restplus import fields


ERROR_SWAGGER_MODEL_NAME = "Error"
ERROR_SWAGGER_MODEL_DOC = {
    'error': fields.Integer(required=True, title="Error code", description="Error code",
                            example="applications_not_found"),
    'error_detail': fields.String(required=True, title="Error description",
                                  description="Error description", example="No applications found")
}

STATUS_SWAGGER_MODEL_NAME = "Status"
STATUS_SWAGGER_MODEL_DOC = {
    'status': fields.String(required=True, title="Status", description="Status", example="ok")
}

COUNT_SWAGGER_MODEL_NAME = "Count Response"
COUNT_SWAGGER_MODEL_DOC = {
    'count': fields.Integer(
        title='count',
        description=f"count",
        example="12"),
}
