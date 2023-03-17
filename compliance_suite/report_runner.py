from ga4gh.testbed.report.report import Report
from compliance_suite.validate_response import ValidateResponse
import json
import requests
from base64 import b64encode
from compliance_suite.helper import Parser
import os
from compliance_suite.constants import *
from supported_drs_versions import SUPPORTED_DRS_VERSIONS

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


# TODO: 1. endpoint calls into a function
# TODO: 2. get version from params and confirm its in the list of supported versions.
#  parse args & setup.py should get the list of supported version from one source


def report_runner(server_base_url, platform_name, platform_description, auth_type):

    # Read input DRS objects from config folder
    # TODO: Add lower and upper limits to input DRS objects
    input_drs_objects = get_input_drs_objects()

    # get authentication information from respective config file based on type of authentication
    headers = {}
    config = get_authentication_config(auth_type)
    drs_object_passport_map = {}
    if (auth_type == "basic"):
        username = config["username"]
        password = config["password"]
        b64_encoded_username_password = b64encode(str.encode("{}:{}".format(username, password))).decode("ascii")
        headers = { "Authorization" : "Basic {}".format(b64_encoded_username_password) }
    elif (auth_type == "bearer"):
        bearer_token = config["bearer_token"]
        headers =  { "Authorization" : "Bearer {}".format(bearer_token) }
    elif (auth_type == "passport"):
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
    test_service_info(
        service_info_phase,
        server_base_url,
        headers,
        auth_type,
        schema_dir = "",
        schema_file = SERVICE_INFO_SCHEMA,
        expected_status_code = "200",
        expected_content_type = "application/json")

    service_info_phase.set_end_time_now()

    # TODO : Add a test case to check that drs version from service-info == drs_version provided.
    # input params - must provide a drs_version
    # TODO: remove version hardcoding
    drs_version_schema_dir = "v" + "1.2.0" + "/"

    ### PHASE: /objects/{object_id}
    drs_object_phase = report_object.add_phase()
    drs_object_phase.set_phase_name("drs object info endpoint")
    drs_object_phase.set_phase_description("run all the tests for drs object info endpoint")

    for this_drs_object in input_drs_objects:

        # TODO: Add code to figure out what the expected_status_code
        #  and expected_content_type are for each drs_object_id.
        test_drs_object_info(
            drs_object_phase,
            server_base_url,
            headers,
            auth_type,
            drs_object_passport_map = drs_object_passport_map,
            drs_object_id = this_drs_object["drs_id"],
            schema_dir = drs_version_schema_dir,
            schema_file = DRS_OBJECT_SCHEMA,
            expected_status_code = "200",
            expected_content_type = "application/json")

    # TODO: add extra tests to check the case where auth is required but not provided,
    #  it should return an error response object with appropriate status code

    drs_object_phase.set_end_time_now()

    # PHASE: /objects/{object_id}/access/{access_id}
    drs_access_phase = report_object.add_phase()
    drs_access_phase.set_phase_name("drs access endpoint")
    drs_access_phase.set_phase_description("run all the tests for drs access endpoint")

    for this_drs_object in input_drs_objects:
        test_drs_object_access(
            drs_access_phase,
            server_base_url,
            headers,
            auth_type,
            drs_object_passport_map = drs_object_passport_map,
            drs_object_id = this_drs_object["drs_id"],
            drs_access_id = this_drs_object["access_id"],
            schema_dir = drs_version_schema_dir,
            schema_file = DRS_ACCESS_SCHEMA,
            expected_status_code = "200",
            expected_content_type = "application/json")

    drs_access_phase.set_end_time_now()
    report_object.set_end_time_now()
    report_object.finalize()
    return report_object.to_json()

def get_input_drs_objects():
    """
    Returns the input DRS objects from the config folder.
    """
    with open(os.path.join(CONFIG_DIR, "input_drs_objects.json"), "r") as f:
        return json.load(f)["drs_objects"]

def get_authentication_config(auth_type):
    """
    Returns the authentication information from the respective config file based on the type of authentication.
    """
    if auth_type in ("basic","bearer","passport"):
        with open(os.path.join(CONFIG_DIR, f"config_{auth_type}.json"), "r") as f:
            return json.load(f)

def test_service_info(
        service_info_phase,
        server_base_url,
        headers,
        auth_type,
        schema_dir,
        schema_file,
        expected_status_code,
        expected_content_type):
    service_info_test = service_info_phase.add_test()
    service_info_test.set_test_name("service-info")
    service_info_test.set_test_description("validate service-info status code, content-type "
                                       "and response schemas")

    response = send_request(
        server_base_url,
        SERVICE_INFO_URL,
        headers,
        auth_type)

    add_common_test_cases(
        test_object = service_info_test,
        endpoint_name = "Service Info",
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    service_info_test.set_end_time_now()

def test_drs_object_info(
        drs_object_phase,
        server_base_url,
        headers,
        auth_type,
        drs_object_passport_map,
        drs_object_id,
        schema_dir,
        schema_file,
        expected_status_code,
        expected_content_type):

    drs_object_test = drs_object_phase.add_test()
    drs_object_test.set_test_name(f"run test cases on the drs object info endpoint for drs id = {drs_object_id}")
    drs_object_test.set_test_description("validate drs object status code, content-type and response schemas")

    response = send_request(
        server_base_url,
        DRS_OBJECT_INFO_URL + drs_object_id,
        headers,
        auth_type,
        drs_object_passport_map = drs_object_passport_map,
        drs_object_id = drs_object_id)

    add_common_test_cases(
        test_object = drs_object_test,
        endpoint_name = "DRS Object Info",
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    drs_object_test.set_end_time_now()

def test_drs_object_access(
        drs_access_phase,
        server_base_url,
        headers,
        auth_type,
        drs_object_passport_map,
        drs_object_id,
        drs_access_id,
        schema_dir,
        schema_file,
        expected_status_code,
        expected_content_type):

    drs_access_test = drs_access_phase.add_test()
    drs_access_test.set_test_name(f"run test cases on the drs access endpoint for drs id = {drs_object_id} "
                                  f"and access id = {drs_access_id}")
    drs_access_test.set_test_description("validate drs access status code, content-type and response schemas")

    response = send_request(
        server_base_url,
        DRS_OBJECT_INFO_URL + drs_object_id + DRS_ACCESS_URL + drs_access_id,
        headers,
        auth_type,
        drs_object_passport_map = drs_object_passport_map,
        drs_object_id = drs_object_id)

    add_common_test_cases(
        test_object = drs_access_test,
        endpoint_name = "DRS Access",
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    drs_access_test.set_end_time_now()

def send_request(
        server_base_url,
        endpoint_url,
        headers,
        auth_type,
        **kwargs):

    request_body = {}
    if auth_type == "passport" and endpoint_url != SERVICE_INFO_URL:
        # endpoints that allow auth_type: "passport"
        # 1. DRS Objects: /objects/{object_id}
        # 2. DRS Object Access: /objects/{object_id}/access/{access_id}
        drs_object_passport = kwargs["drs_object_passport_map"][kwargs["drs_object_id"]]
        request_body = {"passports": [drs_object_passport]}
        http_method = "POST"
    elif auth_type in ("basic", "bearer", "none") or endpoint_url == SERVICE_INFO_URL:
        # endpoint Service Info: /service-info allows auth_type: "basic", "bearer" or "none"
        http_method = "GET"
    else:
        raise ValueError("Invalid auth_type")

    response = requests.request(
        method = http_method,
        url = server_base_url + endpoint_url,
        json = request_body,
        headers = headers)

    return response

def add_common_test_cases(
        test_object,
        endpoint_name,
        response,
        expected_status_code,
        expected_content_type,
        schema_dir,
        schema_file):
    """
    Adds common test cases to a Test object
    Common test cases:
        1. validate response status_code
        2. validate response content_type
        3. validate response json schema
    """

    ### CASE: response status_code
    add_test_case(
        test_object = test_object,
        case_type = "status_code",
        case_name = f"{endpoint_name} response status code validation",
        case_description = f"Check if the response status code is {expected_status_code}",
        response = response,
        expected_status_code = expected_status_code)

    ### CASE: response content_type
    add_test_case(
        test_object = test_object,
        case_type = "content_type",
        case_name = f"{endpoint_name} response content-type validation",
        case_description = f"Check if the content-type is {expected_content_type}",
        response = response,
        expected_content_type = expected_content_type)

    ### CASE: response schema
    add_test_case(
        test_object = test_object,
        case_type = "response_schema",
        case_name = f"{endpoint_name} response schema validation",
        case_description = f"Validate {endpoint_name}  response schema when status = {expected_status_code}",
        response = response,
        schema_name = os.path.join(schema_dir, schema_file))

def add_test_case(test_object, case_type, **kwargs):
    """
    Adds a test case to a Test object based on type of the case.
    """
    test_case = test_object.add_case()
    test_case.set_case_name(kwargs['case_name'])
    test_case.set_case_description(kwargs['case_description'])

    validate_response = ValidateResponse()
    validate_response.set_case(test_case)
    validate_response.set_actual_response(kwargs['response'])

    if case_type == 'status_code':
        validate_response.validate_status_code(kwargs['expected_status_code'])
    elif case_type == 'content_type':
        validate_response.validate_content_type(kwargs['expected_content_type'])
    elif case_type == 'response_schema':
        validate_response.set_response_schema_file(kwargs['schema_name'])
        validate_response.validate_response_schema()

    test_case.set_end_time_now()

def main():
    args = Parser.parse_args()

    output_report = report_runner(server_base_url = args.server_base_url,
                                platform_name = args.platform_name,
                                platform_description = args.platform_description,
                                auth_type = args.auth_type)

    output_report_json = json.loads(output_report)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    # write output report to file
    with open(args.report_path, 'w', encoding='utf-8') as f:
        json.dump(output_report_json, f, ensure_ascii=False, indent=4)

if __name__=="__main__":
    main()