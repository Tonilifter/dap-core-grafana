# Repsol Core API for Service Component Catalog Back functions 

This is service component catalog web back api.

The methods are implemented and exposed as a REST API using Flask.

# Getting Started
1.Installation process

This library requires Python 3.x and the following packages (this list is based on ubuntu, other distributions
may use different names): gcc, g++, python-dev, unixodbc-dev.

Using virtualenv is recommended. Use the following commands to create and activate a virtual environment named `myenv`:

```
virtualenv myenv -p python3.6
source myenv/bin/activate
```

2.Software dependencies

The dependencies are located on requirements.txt file and its need to configure the file pyenv/py.conf with Azure Artifacts credentials:

```
pip install -r requirements.txt
```

To use GIT credentials to download dapexcelpreprocessor_lib is able to use requirements_local.txt instead of requirements.txt.

3.API references

This API is documented automatically using swagger, the swagger doc is available when
the api starts on base path.

To document with swagger are using flask with flask_restplus. More info on: 

https://towardsdatascience.com/working-with-apis-using-flask-flask-restplus-and-swagger-ui-7cf447deda7f



# Build and Test
For unit tests:
```
tox -c tox_unit_test.ini
```
For integration tests:
```
tox -c tox_integration_test.ini
```

For testing purposes, if you need to execute this service in your local computer,
 it is needed to define these environment variables:

```
AZURE_LOGS_WORKSPACE_ID = Azure Log Analytics Workspace ID
AZURE_LOGS_WORKSPACE_KEY = Azure Log Analytics Custom Log Primary Key
OPERATION_LOGS_NAME = Name of Custom Logs in Azure Log Analytics, if empty the value OperationalCoreLog is used
```

Execute the api with flask using the command:

```
FLASK_APP=log_api_entrypoint.py flask run
```

# Contribute
For collaborate on this repo we use the Git Flow strategy with 2 main branches: master and develop

The new functionalities should be developed on feature branches and make a pull request that should be approved before to merge to develop branch.

On lab and test environments the branch used to deploy will be develop.
On preproduction and production environments the branch will be master. 

