# drs-compliance-suite
Tests to verify the compliance of a DRS implementation with GA4GH Data Repository Service (DRS) specification. 
This compliance suite currently supports the following DRS versions and will aim to support more versions of DRS in the future.
* DRS 1.2.0

## Installations
- [Python 3.x](https://www.python.org/downloads/) is required to run DRS Compliance Suite natively or using PyPI package.
- [Docker Desktop](https://docs.docker.com/get-docker/) is required to run DRS Compliance Suite using a docker image.
## Running DRS Compliance Suite
### 1. Natively

Install the packages from requirements.txt
```
cd drs-compliance-suite
pip3 install -r requirements.txt
```

Add PYTHONPATH to env variables
```
export PYTHONPATH=<absolute path to drs-compliance-suite>
```

Run the compliance suite
```
python3 compliance_suite/report_runner.py --server_base_url "http://localhost:8085/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --drs_version "1.2.0" --config_file "compliance_suite/config/config_samples/config_basic.json" --serve --serve_port 56565
```
Note: This specific command is an example of running the compliance suite on a local deployment of DRS that is running on port 8085. \
When running the compliance suite, it's important to configure the command line arguments according to the specific DRS implementation you're testing.
Please refer to the [Command Line Arguments](#command-line-arguments) section for details on each of these arguments.

### 2. Using PyPI Package

Install the latest version of the `drs-compliance-suite` PyPI package using pip3
```
pip3 install drs-compliance-suite --upgrade
```
Run the compliance suite
```
drs-compliance-suite --server_base_url "http://localhost:8085/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --drs_version "1.2.0" --config_file "compliance_suite/config/config_samples/config_basic.json" --serve --serve_port 56565
```
Note: This specific command is an example of running the compliance suite on a local deployment of DRS that is running on port 8085. \
When running the compliance suite, it's important to configure the command line arguments according to the specific DRS implementation you're testing.
Please refer to the [Command Line Arguments](#command-line-arguments) section for details on each of these arguments.

### 3. Using Docker

Pull the latest docker image from dockerhub. 
```
docker pull ga4gh/drs-compliance-suite:1.0.3
```
Run the compliance suite using the docker image. Make sure your config file is available at `config/config_drs.json` 

```
docker run -d --name drs-compliance-suite -v $(PWD)/output/:/usr/src/app/output/ -v ${PWD}/config/:/usr/src/app/config/ -p 57568:57568 ga4gh/drs-compliance-suite:1.0.3 --server_base_url "http://host.docker.internal:8085/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --report_path "./output/drs-cs-report.json" --drs_version "1.2.0" --config_file "./config/config_drs.json" --serve --serve_port 57568
```
Note: 
* To run this docker image on MAC ARM processor, append `--platform linux/x86_64` to the above command.
* This specific command is an example of running the compliance suite on a local deployment of DRS that is running on port 8085. \
When running the compliance suite, it's important to configure the command line arguments according to the specific DRS implementation you're testing.
Please refer to the [Command Line Arguments](#command-line-arguments) section for details on each of these arguments.

### Command Line Arguments
| Command Line Argument | Description | Optional/Required | Default Value |
| --------------------- | ----------- | ----------------- | ------------- |
| --server_base_url | The base URL of the DRS implementation that is being tested by the compliance suite. | Required | N/A |
| --platform_name | The name of the platform hosting the DRS server. | Required | N/A |
| --platform_description | The description of the platform hosting the DRS server. | Required | N/A |
| --drs_version | The version of DRS implemented by the DRS server taht is being tested for compliance. It can be one of the following: "1.2.0" | Required | N/A |
| --config_file | The file path of the JSON config file. The config file must contain auth information for service-info endpoint and different DRS objects. Refer to the [config-file](#config-file) section for more details. | Required | N/A |
| --report_path | The path of the output JSON report file. | Optional | "./output/drs_compliance_report.json" |
| --serve | If this flag is set to True, the output report is served as an HTML webpage at the port specified by `--serve_port`. | Optional | False |
| --serve-port | The port where the output report HTML is deployed. | Optional | 57568 |

#### Config File:

The compliance suite is provided with information for testing the DRS server through a user-provided JSON config file. This file includes the following details:
- Authorization information for the service-info endpoint
- A few DRS Object IDs that are present in the DRS server
- Authorization information for each of these DRS objects
- Indication of whether the DRS object is a bundle or a single blob

Here's a template for a config file that can be used to configure these details:
```
{
  "service_info": {
      "auth_type": "basic",
      "auth_token": "dXNlcm5hbWU6cGFzc3dvcmQ="
  },
  "drs_objects" : [
      {
          "drs_id": "697907bf-d5bd-433e-aac2-1747f1faf366",
          "auth_type": "none",
          "auth_token": "",
          "is_bundle": false
      },
      {
          "drs_id": "0bb9d297-2710-48f6-ab4d-80d5eb0c9eaa",
          "auth_type": "basic",
          "auth_token": "dXNlcm5hbWU6cGFzc3dvcmQ=",
          "is_bundle": false
      },
      {
          "drs_id" : "41898242-62a9-4129-9a2c-5a4e8f5f0afb",
          "auth_type": "bearer",
          "auth_token": "secret-bearer-token-1",
          "is_bundle": true
      },
      {
          "drs_id" : "a1dd4ae2-8d26-43b0-a199-342b64c7dff6",
          "auth_type": "passport",
          "auth_token": "43b-passport-a1d",
          "is_bundle": true
      }
  ]
}
```
- The "auth_type" specifies the type of authorization, which can be one of the following: ["basic", "bearer", "passport", "none"]
- The "auth_token" field contains the corresponding authorization token value.
- If "auth_type" is set to "basic", the "auth_token" can be created by using base64 encoding.
- If "auth_type" is set to "none", the "auth_token" field should be left blank with a value of "".
- The "is_bundle" flag indicates whether the DRS object is a bundle or a single blob. If set to True, the object is a bundle, and if set to False, the object is a single blob.

You can find some sample config files [here](./compliance_suite/config/config_samples)

## Unittesting

Firstly, run the mock servers using this script command
```
bash unittests/start.sh
```


Run the unittests with coverage
```
python -m pytest unittests/
```

Once you are done with unittesting, make sure you terminate the mock servers and remove temporary log files by running this command
```
bash unittests/stop.sh
```

## Changelog

### v1.0.3
* provide flexibility in providing different auth information for drs object and drs access endpoints
* remove incorrect skip status setting

### v1.0.2
* Reduce the docker image size by using python:3.11-slim-bullseye instead of python:3

### v1.0.1
* Fixed a bug in the docker deployment of DRS Compliance Suite 
* Update README documentation

### v1.0.0
* DRS Compliance Suite for [Data Repository Service v1.2.0](https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.2.0/docs/)