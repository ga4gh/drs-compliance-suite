from ga4gh.testbed.report.report import Report
from compliance_suite.validate_response import ValidateResponse
from compliance_suite.validate_drs_object_response import ValidateDRSObjectResponse
import json
import requests
from base64 import b64encode
from compliance_suite.helper import Parser
import os
from compliance_suite.constants import *
from compliance_suite.report_server import start_mock_server

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

drs_objects_access_id_map = {}

def report_runner(server_base_url, platform_name, platform_description, auth_type, drs_version):
    """
    Returns a Report Object which is generated by running compliance tests on various endpoints of a DRS server.
    """
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
    report_object.add_input_parameter("server_base_url",server_base_url)

    ### PHASE: /service-info
    service_info_phase = report_object.add_phase()
    service_info_phase.set_phase_name("service info")
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
    schema_dir = "v" + drs_version + "/"

    # TODO: extend support to DRS v1.3.0 -
    #  1. make a json map of endpoints per each DRS version
    #  using which phases are created and added to the report object
    #  2. schema_dir should take care of pulling the right schema for validation
    #  3. Add the version to supported_drs_versions
    #  4. add any version specific test cases


    ### PHASE: /objects/{object_id}
    drs_object_phase = report_object.add_phase()
    drs_object_phase.set_phase_name("drs object info")
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
            is_bundle = this_drs_object["is_bundle"],
            schema_dir = schema_dir,
            schema_file = DRS_OBJECT_SCHEMA,
            expected_status_code = "200",
            expected_content_type = "application/json")

    # TODO: add extra tests to check the case where auth is required but not provided,
    #  it should return an error response object with appropriate status code

    drs_object_phase.set_end_time_now()

    # PHASE: /objects/{object_id}/access/{access_id}
    drs_access_phase = report_object.add_phase()
    drs_access_phase.set_phase_name("drs object access")
    drs_access_phase.set_phase_description("run all the tests for drs access endpoint")

    for this_drs_object in input_drs_objects:
        for this_access_id in drs_objects_access_id_map[this_drs_object["drs_id"]]:
            test_drs_object_access(
                drs_access_phase,
                server_base_url,
                headers,
                auth_type,
                drs_object_passport_map = drs_object_passport_map,
                drs_object_id = this_drs_object["drs_id"],
                drs_access_id = this_access_id,
                schema_dir = schema_dir,
                schema_file = DRS_ACCESS_SCHEMA,
                expected_status_code = "200",
                expected_content_type = "application/json")

    drs_access_phase.set_end_time_now()
    report_object.set_end_time_now()
    report_object.finalize()
    return report_object

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
    service_info_test.set_test_name("Run test cases on the service-info endpoint")
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
        is_bundle,
        schema_dir,
        schema_file,
        expected_status_code,
        expected_content_type):

    global drs_objects_access_id_map
    drs_object_test = drs_object_phase.add_test()
    drs_object_test.set_test_name(f"Run test cases on the drs object info endpoint for drs id = {drs_object_id}")
    drs_object_test.set_test_description("validate drs object status code, content-type and response schemas")
    endpoint_name = "DRS Object Info"

    response = send_request(
        server_base_url,
        DRS_OBJECT_INFO_URL + drs_object_id,
        headers,
        auth_type,
        drs_object_passport_map = drs_object_passport_map,
        drs_object_id = drs_object_id)

    add_common_test_cases(
        test_object = drs_object_test,
        endpoint_name = endpoint_name,
        response = response,
        expected_status_code = expected_status_code,
        expected_content_type = expected_content_type,
        schema_dir = schema_dir,
        schema_file = schema_file)

    # Response with expand parameter set to true
    response = send_request(
        server_base_url,
        DRS_OBJECT_INFO_URL + drs_object_id,
        headers,
        auth_type,
        drs_object_passport_map = drs_object_passport_map,
        drs_object_id = drs_object_id,
        params = {'expand': True})

    # TODO: find way to determine if object is bundle or to be skipped
    # Skip test if contents field is not available
    if is_bundle:
        ### CASE: response expand bundle
        add_test_case_common(
            test_object = drs_object_test,
            case_type = "expand_bundle",
            case_name = "DRS Access expand bundle validation",
            case_description = f"Validate DRS bundle when expand = True",
            response = response,
            schema_name = os.path.join(schema_dir, 'drs_bundle.json'))
            
    add_access_methods_test_case(
        test_object = drs_object_test,
        case_type = "has_access_methods",
        case_description = f"Validate that {endpoint_name} response has "
                           f"access_methods field provided and that it is non-empty",
        endpoint_name = endpoint_name,
        response = response)

    drs_objects_access_id_map[drs_object_id] = add_access_methods_test_case(
        test_object = drs_object_test,
        case_type = "has_access_info",
        case_description =f"Validate that each access_method in the access_methods field "
                          f"of the {endpoint_name} response has atleast one of 'access_url'"
                          f"or 'access_id' provided",
        endpoint_name = endpoint_name,
        response = response)

    add_access_methods_test_case(
        test_object = drs_object_test,
        case_type = "has_access_methods",
        case_description = f"Validate that {endpoint_name} response has "
                           f"access_methods field provided and that it is non-empty",
        endpoint_name = endpoint_name,
        response = response)

    drs_objects_access_id_map[drs_object_id] = add_access_methods_test_case(
        test_object = drs_object_test,
        case_type = "has_access_info",
        case_description =f"Validate that each access_method in the access_methods field "
                          f"of the {endpoint_name} response has atleast one of 'access_url'"
                          f"or 'access_id' provided",
        endpoint_name = endpoint_name,
        response = response)

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
    drs_access_test.set_test_name(f"Run test cases on the drs access endpoint for drs id = {drs_object_id} "
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
        
        if 'expand' in kwargs.keys():
            request_body = {"passports": [drs_object_passport], "expand": True}
        else:
            request_body = {"passports": [drs_object_passport]}

        http_method = "POST"
    elif auth_type in ("basic", "bearer", "none") or endpoint_url == SERVICE_INFO_URL:
        # endpoint Service Info: /service-info allows auth_type: "basic", "bearer" or "none"
        http_method = "GET"
    else:
        raise ValueError("Invalid auth_type")

    if 'expand' in kwargs.keys() and auth_type != "passport":
        params = {'expand': True}
    else:
        params = {}

    response = requests.request(
        method = http_method,
        url = server_base_url + endpoint_url,
        params = params,
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
    add_test_case_common(
        test_object = test_object,
        case_type = "status_code",
        case_name = f"{endpoint_name} response status code validation",
        case_description = f"Check if the response status code is {expected_status_code}",
        response = response,
        expected_status_code = expected_status_code)

    ### CASE: response content_type
    add_test_case_common(
        test_object = test_object,
        case_type = "content_type",
        case_name = f"{endpoint_name} response content-type validation",
        case_description = f"Check if the content-type is {expected_content_type}",
        response = response,
        expected_content_type = expected_content_type)

    ### CASE: response schema
    add_test_case_common(
        test_object = test_object,
        case_type = "response_schema",
        case_name = f"{endpoint_name} response schema validation",
        case_description = f"Validate {endpoint_name} response schema when status = {expected_status_code}",
        response = response,
        schema_name = os.path.join(schema_dir, schema_file))

def add_test_case_common(test_object, case_type, **kwargs):
    """
    Adds a common test case to a Test object based on type of the case - status_code/ content_type/ response_schema.
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
    elif case_type == 'expand_bundle':
        validate_response.set_response_schema_file(kwargs['schema_name'])
        validate_response.validate_expand_bundle()
    test_case.set_end_time_now()

def add_access_methods_test_case(test_object, case_type, case_description, endpoint_name, response):
    """
    Adds a test case to a Test object to check if access information is present in the drs_object response.
    DRS v1.2.0 Spec - `access_methods`:
     - Required for single blobs; optional for bundles.
     - At least one of `access_url` and `access_id` must be provided.
    """
    test_case = test_object.add_case()
    test_case.set_case_name(f"{endpoint_name} has access information")
    test_case.set_case_description(case_description)

    validate_drs_response = ValidateDRSObjectResponse()
    validate_drs_response.set_case(test_case)
    validate_drs_response.set_actual_response(response)

    access_id_list = None
    if case_type == "has_access_methods":
        validate_drs_response.validate_has_access_methods()
    elif case_type == "has_access_info":
        access_id_list = validate_drs_response.validate_has_access_info()
    test_case.set_end_time_now()
    return access_id_list

def main():
    args = Parser.parse_args()

    output_report = report_runner(server_base_url = args.server_base_url,
                                platform_name = args.platform_name,
                                platform_description = args.platform_description,
                                auth_type = args.auth_type,
                                drs_version = args.drs_version)

    output_report_json = json.loads(output_report.to_json(pretty=True))

    if not os.path.exists("./output"):
        os.makedirs("./output")

    # write output report to file
    with open(args.report_path, 'w', encoding='utf-8') as f:
        json.dump(output_report_json, f, ensure_ascii=False, indent=4)

    if (args.serve):
        with open("./compliance_suite/web/temp_report.json", 'w', encoding='utf-8') as f:
            json.dump(output_report_json, f, ensure_ascii=False, indent=4)
        start_mock_server(args.serve_port)

if __name__=="__main__":
    main()