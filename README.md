# drs-compliance-suite
Tests to verify the compliance of a DRS implementation with GA4GH Data Repository Service (DRS) specification. 
This compliance suite currently supports the following DRS versions and will aim to support future versions of DRS as well.
* DRS 1.2.0

## Installations
Python 3.x is required to run DRS Compliance Suite. We recomment using a virtual environment to run the compliance suite.

Install Python virtualenv package and create a new Python virtual environment
```
pip3 install virtualenv
python3 -m virtualenv drs_venv
```
To activate the virtual environment
```
source <path_to_virtual_env>/bin/activate
```
To deactivate or exit the virtual environment
```
deactivate
```

Install the packages from requirements.txt
```
cd drs-compliance-suite
pip install -r requirements.txt
```

Add PYTHONPATH to env variables
```
export PYTHONPATH=<absolute path to drs-compliance-suite>
```

## Running natively in a developer environment

* First spin up a DRS starter kit on port 5000 or a port of your choice. Make sure to specify the port number correctly in the next step.
* The following command will run the DRS complaince suite against the specified DRS implementation.
``` 
python compliance_suite/report_runner.py --server_base_url "http://localhost:5000/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --auth_type "basic"
```
### Command Line Arguments
#### <TODO: Add a table with default values, data type !!>
#### Required:
* **--server_base_url** : base url of the DRS implementation that is being tested by the compliance suite
* **--platform_name** : name of the platform hosting the DRS server
* **--platform_description** : description of the platform hosting the DRS server
* **--auth_type** : type of authentication used in the DRS server implementation. It can be one of the following -
  * "none"
  * "basic"
  * "bearer"
  * "passport"

Depending on the auth type selected, the appropriate credentials must be provided by the end user
* credentials may be found for the associated auth type
  * "basic" : config_basic.json
  * "bearer" : config_bearer.json
  * "passport" : config_passport.json

## Running the good mock server
```
python unittests/good_mock_server.py --auth_type "none" --app_host "0.0.0.0" --app_port "8089"
```
Make sure that the good mock server is running smoothly by making a GET request to 
```
http://localhost:8089/ga4gh/drs/v1/service-info
```
You should get a response status of 200

### Command Line Arguments
#### Required:
* **--app_port** : port where the mock server is running
#### Optional:
* **--auth_type** : type of authentication. It can be one of the following -
  * "none"
  * "basic"
  * "bearer"
  * "passport"
* **--app_host** : name of the host where the mock server is running

## Running unittests for testing
Note: Both bad and good mock servers should be running beforehand
#### Running the mock servers
```
python unittests/good_mock_server.py --auth_type "none" --app_host "0.0.0.0" --app_port "8089"
python unittests/bad_mock_server.py --auth_type "none" --app_host "0.0.0.0" --app_port "8088"
```
###### Run the tests
```
py.test -v
```
###### Check the code coverage of the tests
```
pytest --cov=compliance_suite unittests/ 
```

## Running workflows
#### CWL
###### `cwltool`
```
cwltool --outdir output tools/cwl/drs_compliance_suite.cwl tools/cwl/drs_compliance_suite.cwl.json
```
Note: `output` is the subdirectory where the report will be saved, can be customized.
###### `dockstore`
```
dockstore tool launch --local-entry tools/cwl/drs_compliance_suite.cwl --json tools/cwl/drs_compliance_suite.cwl.json --script
```
Notes:
* Saves the output file in the outermost directory (`/drs-compliance-suite/`).
* `--script` is used to override `dockstore`'s requirement that every python package must match versions.

#### WDL
```
dockstore workflow launch --local-entry tools/wdl/drs_compliance_suite.wdl --json tools/wdl/drs_compliance_suite.wdl.json
```
Notes:
* Saves the output file in the folder created to run the workflow. Can `cd` into the folder to retrieve the report.
* Find this printed line once the workflow is complete (`...` are randomly generated IDs):
```
[YYYY-MM-DD HH:MM:SS,MS] [info] SingleWorkflowRunnerActor workflow finished with status 'Succeeded'.
{
  "outputs": {
    "drsComplianceReportWorkflow.createDrsComplianceReport.drs_compliance_report": "/private/var/folders/.../cromwell-executions/drsComplianceReportWorkflow/.../call-createDrsComplianceReport/execution/wdl-test-drs-compliance-report.json"
  },
  "id": "..."
}
```