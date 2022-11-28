from ga4gh.testbed.report.report import Report
from compliance_suite.validate_response import ValidateResponse
import json
import requests
from base64 import b64encode
from datetime import datetime
from compliance_suite.helper import Parser
import os
from compliance_suite.constants import *
from ga4gh.testbed.report.status import Status

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def report_runner(server_base_url, platform_name, platform_description, auth_type):

    # Read input DRS objects from config folder
    # TODO: Add lower and upper limits to input DRS objects
    with open(CONFIG_DIR+"/input_drs_objects.json", 'r') as file:
        input_drs = json.load(file)
    input_drs_objects = input_drs["drs_objects"]

    # get authentication information from respective config file based on type of authentication
    headers = {}
    if (auth_type == "basic"):
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
        username = config["username"]
        password = config["password"]
        b64_encoded_username_password = b64encode(str.encode("{}:{}".format(username, password))).decode("ascii")
        headers = { "Authorization" : "Basic {}".format(b64_encoded_username_password) }
    elif (auth_type == "bearer"):
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
        bearer_token = config["bearer_token"]
        headers =  { "Authorization" : "Bearer {}".format(bearer_token) }
    elif (auth_type == "passport"):
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
        drs_object_passport_map = config["drs_object_passport_map"]

    # Create a compliance report object
    report_object = Report()
    report_object.set_testbed_name(TESTBED_NAME)
    report_object.set_testbed_version(TESTBED_VERSION)
    report_object.set_testbed_description(TESTBED_DESCRIPTION)
    report_object.set_platform_name(platform_name)
    report_object.set_platform_description(platform_description)

    ### PHASE: /service-info
    service_info_phase = report_object.add_phase()
    service_info_phase.set_phase_name("service info endpoint")
    service_info_phase.set_phase_description("run all the tests for service_info endpoint")

    ### TEST: GET service-info
    service_info_test = service_info_phase.add_test()
    service_info_test.set_test_name("service-info")
    service_info_test.set_test_description("validate service-info status code, content-type "
                                           "and response schemas")

    SERVICE_INFO_URL = "/service-info"
    response = requests.request(
        method = "GET",
        url = server_base_url + SERVICE_INFO_URL,
        headers = headers)

    expected_status_code = "200"
    expected_content_type = "application/json"

    ### CASE: response status_code
    add_case_status_code(
        test_object = service_info_test,
        expected_status_code = expected_status_code,
        case_name = "service-info response status code validation",
        case_description = "check if the response status code is " + expected_status_code,
        response = response)

    ### CASE: response content_type
    add_case_content_type(
        test_object = service_info_test,
        expected_content_type = expected_content_type,
        case_name = "service-info response content-type validation",
        case_description = "check if the content-type is " + expected_content_type,
        response = response)

    # if any of the above two cases fail, the report runner
    # will not be able to obtain the server's implemented DRS version number.
    # Finalize and return report
    for this_case in service_info_test.get_cases():
        if this_case.get_status() != Status.PASS:
            service_info_test.set_message("Stopping the report as the implemented DRS version "
                                          "can not be obtained from the service-info endpoint")
            service_info_test.set_end_time_now()
            service_info_phase.set_end_time_now()
            report_object.set_end_time_now()
            report_object.finalize()
            return report_object.to_json()

    ### CASE: response schema
    add_case_response_schema(
        test_object = service_info_test,
        schema_name = SERVICE_INFO_SCHEMA,
        case_name = "service-info success response schema validation",
        case_description = "validate service-info response schema when status = " + expected_status_code,
        response = response)

    # Get the DRS version number from service-info
    # If the version is not supported by the compliance suite,
    # finalize and return report

    response_json = response.json()
    server_drs_version = None
    if "type" in response_json and "version" in response_json["type"]:
        server_drs_version = response_json["type"]["version"]
    if server_drs_version not in SUPPORTED_DRS_VERSIONS \
            or response_json["type"]["artifact"].lower() != "drs":
        service_info_test.set_message("Stopping the report as the implemented DRS version " + server_drs_version +
                                      " is not supported by this Compliance Suite. "
                                      "DRS versions currently supported by the DRS Compliance Suite - "
                                      + ",".join(SUPPORTED_DRS_VERSIONS))
        service_info_test.set_end_time_now()
        service_info_phase.set_end_time_now()
        report_object.set_end_time_now()
        report_object.finalize()
        return report_object.to_json()

    service_info_test.set_end_time_now()
    service_info_phase.set_end_time_now()
    drs_version_schema_dir = "v" + server_drs_version + "/"

    ### PHASE: /object/{drs_id}
    drs_object_phase = report_object.add_phase()
    drs_object_phase.set_phase_name("drs object info endpoint")
    drs_object_phase.set_phase_description("run all the tests for drs object info endpoint")

    for this_drs_object in input_drs_objects:
        expected_status_code = "200"
        expected_content_type = "application/json"

        ### TEST: GET /objects/{drs_id}
        drs_object_test = drs_object_phase.add_test()
        drs_object_test.set_test_name("run test cases on the drs object info endpoint for drs id = "
                                      + this_drs_object["drs_id"])
        drs_object_test.set_test_description("validate drs object status code, content-type and "
                                             "response schemas")

        this_drs_object_passport = None
        if auth_type=="passport":
            # this_drs_object_passport = this_drs_object["passport"]
            this_drs_object_passport = drs_object_passport_map[this_drs_object["drs_id"]]
            request_body = {"passports":[this_drs_object_passport]}
            response = requests.request(
                method = "POST",
                url = server_base_url + DRS_OBJECT_INFO_URL + this_drs_object["drs_id"],
                headers = headers,
                json = request_body)
        else:
            response = requests.request(method = "GET",
                                        url = server_base_url + DRS_OBJECT_INFO_URL + this_drs_object["drs_id"],
                                        headers = headers)

        ### CASE: response status_code
        add_case_status_code(
            test_object = drs_object_test,
            expected_status_code = expected_status_code,
            case_name = "drs object response status code validation",
            case_description = "check if the response status code is " + expected_status_code,
            response = response)

        ### CASE: response content_type
        add_case_content_type(
            test_object = drs_object_test,
            expected_content_type = expected_content_type,
            case_name = "drs object response content-type validation",
            case_description = "check if the content-type is " + expected_content_type,
            response = response)

        ### CASE: response schema
        add_case_response_schema(
            test_object = drs_object_test,
            schema_name = drs_version_schema_dir + DRS_OBJECT_SCHEMA,
            case_name = "drs object response schema validation",
            case_description = "validate drs object response schema when status = " + expected_status_code,
            response = response)

        drs_object_test.set_end_time_now()
    drs_object_phase.set_end_time_now()

    # TEST: GET /objects/{drs_id}/access/{access_id}
    drs_access_phase = report_object.add_phase()
    drs_access_phase.set_phase_name("drs access endpoint")
    drs_access_phase.set_phase_description("run all the tests for drs access endpoint")

    for this_drs_object in input_drs_objects:
        expected_status_code = "200"
        expected_content_type = "application/json"

        ### TEST: GET /objects/{drs_id}/access/{access_id}
        drs_access_test = drs_access_phase.add_test()
        drs_access_test.set_test_name("run test cases on the drs access endpoint for "
                                      "drs id = " + this_drs_object["drs_id"]
                                      + " and access id = " + this_drs_object["access_id"])
        drs_access_test.set_test_description("validate drs access status code, content-type and "
                                             "response schemas")

        this_drs_object_passport = None
        if auth_type=="passport":
            this_drs_object_passport = drs_object_passport_map[this_drs_object["drs_id"]]
            request_body = {"passports":[this_drs_object_passport]}
            response = requests.request(
                method = "POST",
                url = server_base_url
                      + DRS_OBJECT_INFO_URL + this_drs_object["drs_id"]
                      + DRS_ACCESS_URL + this_drs_object["access_id"],
                headers = headers,
                json = request_body)
        else:
            response = requests.request(method = "GET",
                                        url = server_base_url
                                              + DRS_OBJECT_INFO_URL + this_drs_object["drs_id"]
                                              + DRS_ACCESS_URL + this_drs_object["access_id"],
                                        headers = headers)

        ### CASE: response status_code
        add_case_status_code(
            test_object = drs_access_test,
            expected_status_code = expected_status_code,
            case_name = "drs access response status code validation",
            case_description = "check if the response status code is " + expected_status_code,
            response = response)

        ### CASE: response content_type
        add_case_content_type(
            test_object = drs_access_test,
            expected_content_type = expected_content_type,
            case_name = "drs access response content-type validation",
            case_description = "check if the content-type is " + expected_content_type,
            response = response)

        ### CASE: response schema
        add_case_response_schema(
            test_object = drs_access_test,
            schema_name = drs_version_schema_dir + DRS_ACCESS_SCHEMA,
            case_name = "drs access response schema validation",
            case_description = "validate drs access response schema when status = " + expected_status_code,
            response = response)

        drs_access_test.set_end_time_now()
    drs_access_phase.set_end_time_now()
    report_object.set_end_time_now()
    report_object.finalize()
    return report_object.to_json()

def add_case_status_code(test_object,expected_status_code, case_name, case_description, response):
    case_response_status = test_object.add_case()
    case_response_status.set_case_name(case_name)
    case_response_status.set_case_description(case_description)

    validate_response_status = ValidateResponse()
    validate_response_status.set_case(case_response_status)
    validate_response_status.set_actual_response(response)
    validate_response_status.validate_status_code(expected_status_code)

    case_response_status.set_end_time_now()

def add_case_content_type(test_object,expected_content_type, case_name, case_description, response):
    case_response_content_type = test_object.add_case()
    case_response_content_type.set_case_name(case_name)
    case_response_content_type.set_case_description(case_description)

    validate_response_content_type = ValidateResponse()
    validate_response_content_type.set_case(case_response_content_type)
    validate_response_content_type.set_actual_response(response)
    validate_response_content_type.validate_content_type(expected_content_type)

    case_response_content_type.set_end_time_now()

def add_case_response_schema(test_object,schema_name, case_name, case_description, response):
    case_response_schema = test_object.add_case()
    case_response_schema.set_case_name(case_name)
    case_response_schema.set_case_description(case_description)

    validate_response_schema = ValidateResponse()
    validate_response_schema.set_case(case_response_schema)
    validate_response_schema.set_actual_response(response)
    validate_response_schema.set_response_schema_file(schema_name)
    validate_response_schema.validate_response_schema()

    case_response_schema.set_end_time_now()

def main():
    args = Parser.parse_args()
    output_report_file_path = "./output/report_"+datetime.strftime(datetime.utcnow(), "%Y-%m-%d_%H-%M-%S")+".json"

    output_report = report_runner(server_base_url = args.server_base_url,
                                platform_name = args.platform_name,
                                platform_description = args.platform_description,
                                auth_type = args.auth_type)

    output_report_json = json.loads(output_report)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    # write output report to file
    with open(output_report_file_path, 'w', encoding='utf-8') as f:
        json.dump(output_report_json, f, ensure_ascii=False, indent=4)

if __name__=="__main__":
    main()