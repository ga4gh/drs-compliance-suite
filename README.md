# drs-compliance-suite
Tests to verify the compliance of a DRS implementation with GA4GH DRS v1.2 specification 

## Installations
Python 3.x is required to run DRS Compliance Suite.

## Running natively in a developer environment

* First spin up a DRS starter kit on port 5000 or a port of your choice. Make sure to specify the port number correctly in the next step.
* The following command will run the DRS complaince suite against the specified DRS implementation.
``` 
python3 report_runner.py --server_base_url "http://localhost:5000/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --auth_type "basic" --report_path "./output/test_name.json"
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
## Running the good mock server
```
python unittests/good_mock_server.py --auth_type "none" --app_host "0.0.0.0" --app_port "8089"
```
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