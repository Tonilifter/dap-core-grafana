"""Flask restplus swagger api documentation constants"""
from flask_restplus import fields


APPLICATIONS_SWAGGER_MODEL_NAME = "Application"
APPLICATIONS_SWAGGER_MODEL_DOC = {
    'application_id': fields.String(required=True,
                                    title="Application Id",
                                    description=f"This value identifies an application "
                                    f"and must be unique.",
                                    example="sample_app"),
    'name': fields.String(required=True,
                          title="Application Name",
                          description=f"Application title or name, must be unique.",
                          example="Sample App"),
    'description_es': fields.String(required=True,
                                       title="Spanish Description",
                                       description=f"Application Description (Spanish)",
                                       example="Aplicacion de ejemplo"),
    'description_en': fields.String(required=True,
                                    title="English Description",
                                    description=f"Application Description (English)",
                                    example="Sample Application"),
    'url': fields.String(required=True,
                         title="Application URL",
                         description=f"The application full url",
                         example="https://sampleurl.repsol.com"),
    'active': fields.Boolean(required=False,
                             title="Active",
                             description="Is Active indicator", default=True,
                             example=True),
    'tags': fields.List(fields.String, required=False, title="Tags",
                        description="A list of application tags", example=["core", "analytics"])
}

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

LOGANALYTICS_SWAGGER_MODEL_NAME = "Log Analytics Response"
LOGANALYTICS_SWAGGER_MODEL_DOC = {
    'tables': fields.String(
        title="Tables",
        description=f"Response tables",
        example={
                    "name": "{resultname}",
                    "columns": [
                        {
                            "name": "{name}",
                            "type": "{type}"
                        }
                    ],
                    "rows": [
                        [
                            12.3456789012345678
                        ]
                    ]
                }
        )
}

GOVERNANCE_SWAGGER_MODEL_NAME = "Governance Response"
GOVERNANCE_SWAGGER_MODEL_DOC = {
    'Number': fields.Integer(
        title='',
        description=f"",
        example="00"),
}

DEVOPS_COLUMNS_SWAGGER_MODEL_NAME = "DevOps Columns Response"
DEVOPS_COLUMNS_SWAGGER_MODEL_DOC = {
    'referenceName': fields.String(
        title='referenceName',
        description=f"referenceName",
        example="System.Title"),
    'name': fields.String(
        title='name',
        description=f"name",
        example="Title"),
    'url': fields.String(
        title='url',
        description=f"url",
        example="https://repsol-digital-team.visualstudio.com/_apis/wit/fields/System.Title"),
}

DEVOPS_WORKITEMS_SWAGGER_MODEL_NAME = "DevOps WorkItems Response"
DEVOPS_WORKITEMS_SWAGGER_MODEL_DOC = {
    'id': fields.String(
        title='id',
        description=f"id",
        example="000000"),
    'url': fields.String(
        title='url',
        description=f"url",
        example="https://repsol-digital-team.visualstudio.com/_apis/wit/workItems/{000000}"),
}

DEVOPS_FEATURES_SWAGGER_MODEL_NAME = "DevOps Features Response"
DEVOPS_FEATURES_SWAGGER_MODEL_DOC = {
    'id': fields.Integer(
        title='id',
        description=f"id",
        example="000000"),
    'rev': fields.Integer(
        title='rev',
        description=f"rev",
        example="00"),
    'fields': fields.String(
        title='rev',
        description=f"rev",
        example={
            "System.AreaPath": "Data Analytics Hub\\Product Backlog ARIA",
            "System.TeamProject": "Data Analytics Hub",
            "System.IterationPath": "Data Analytics Hub\\Product Backlog ARIA\\xxxxxxxxx",
            "System.WorkItemType": "Feature",
            "System.State": "Done",
            "System.Reason": "{status}",
            "System.CreatedDate": "2020-01-01T00:00:00.00Z",
            "System.CreatedBy": {
                "displayName": "{user}",
                "url": "https://xxxxxxxx.vssps.visualstudio.com/{workspace}/_apis/Identities/xxxxxxxxxxx",
                "_links": {
                    "avatar": {
                        "href": "https://repsol-digital-team.visualstudio.com/_apis/GraphProfile/MemberAvatars/xxxxxxxxxxxxxxx"
                    }
                },
                "id": "8272711a-0592-6b0e-be4e-c4be213457b9",
                "uniqueName": "clara.cordero@servexternos.repsol.com",
                "imageUrl": "https://repsol-digital-team.visualstudio.com/_apis/GraphProfile/MemberAvatars/xxxxxxxxxxxxxxx",
                "descriptor": "aad.ODI3MjcxMWEtMDU5Mi03YjBlLWJlNGUtYzRiZTIxMzQ1N2I5"
            },
            "System.ChangedDate": "2021-01-01T00:00:00.000Z",
            "System.ChangedBy": {
                "displayName": "{user}",
                "url": "https://spsprodweu1.vssps.visualstudio.com/A1114b314-7f75-4e1e-880d-fc2a1831dedb/_apis/Identities/xxxxxxxxxxxxxxx",
                "_links": {
                    "avatar": {
                        "href": "https://repsol-digital-team.visualstudio.com/_apis/GraphProfile/MemberAvatars/xxxxxxxxxxxxxxxxxxxxx"
                    }
                },
                "id": "{id code}",
                "uniqueName": "{user mail}",
                "imageUrl": "https://repsol-digital-team.visualstudio.com/_apis/GraphProfile/MemberAvatars/xxxxxxxxxxxxxxxxxx",
                "descriptor": "{descriptor code}"
            },
            "System.CommentCount": "0",
            "System.Title": "{Title}",
            "System.BoardColumn": "Done",
            "System.BoardColumnDone": "{true/false}",
            "Microsoft.VSTS.Common.StateChangeDate": "2020-01-01T00:00:00.000Z",
            "Microsoft.VSTS.Common.ClosedDate": "2020-01-01T00:00:00.000Z",
            "Microsoft.VSTS.Common.ClosedBy": {
                "displayName": "{user}",
                "url": "https://xxxxxxx.vssps.visualstudio.com/{xxxxxxxxxxx}/_apis/Identities/xxxxxxxxxxxxxxxxxxx",
                "_links": {
                    "avatar": {
                        "href": "https://repsol-digital-team.visualstudio.com/_apis/GraphProfile/MemberAvatars/xxxxxxxxxxx"
                    }
                },
                "id": "{id}",
                "uniqueName": "{user}",
                "imageUrl": "{image url}",
                "descriptor": "{description code}"
            },
            "Microsoft.VSTS.Common.Priority": 2,
            "Microsoft.VSTS.Common.ValueArea": "Business",
            "Microsoft.VSTS.Scheduling.TargetDate": "2020-01-01T00:00:00Z",
            "Microsoft.VSTS.Scheduling.StartDate": "2020-01-01T00:00:00Z",
            "WEF_7BCCE3518911452F89BC6C7DA8A44D1A_Kanban.Column": "Done",
            "WEF_7BCCE3518911452F89BC6C7DA8A44D1A_Kanban.Column.Done": "false",
            "Custom.SubgrupoPlataforma": "CORE",
            "Custom.668985b1-6107-4100-a61c-8051338fee66": "{Text}",
            "Custom.77af11d5-b779-4048-a92e-3eb826e39785": "{Text}",
            "Custom.Estado": "{env}",
            "Custom.ContabilizadoComponente": "{true/false}",
            "Custom.DeliveredDate": "2020-01-01T00:00:00Z",
            "System.Description": "{url code}",
            "Custom.Instancia": "{url code}",
            "System.Tags": "CORE"
        }
    ),
    'links': fields.String(
        title='links',
        description=f"links",
        example={
            "self": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/workItems/000000"
            },
            "workItemUpdates": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/workItems/000000/updates"
            },
            "workItemRevisions": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/workItems/000000/revisions"
            },
            "workItemComments": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/workItems/000000/comments"
            },
            "html": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_workitems/edit/000000"
            },
            "workItemType": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/workItemTypes/Feature"
            },
            "fields": {
                "href": "https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/fields"
            }
        }),
    'url': fields.String(
        title='links',
        description=f"links",
        example="https://repsol-digital-team.visualstudio.com/{workspace}/_apis/wit/workItems/000000")
}
