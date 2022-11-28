from compliance_suite.report import Report, Phase, TestbedTest, Case
import json
import requests
from base64 import b64encode
from datetime import datetime
from compliance_suite.generate_json import generate_report_json
from compliance_suite.helper import Parser
import os
from compliance_suite.constants import SCHEMA_SERVICE_INFO, SCHEMA_ERROR, SCHEMA_DRS_OBJECT

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')

def report_runner(server_base_url, platform_name, platform_description, auth_type):
    # TODO: impelement bearer and passport, take the auth info from user
    is_passport_auth = False
    if (auth_type == "none"):
        headers = {}
        with open(CONFIG_DIR+"/config_"+auth_type+".json", 'r') as file:
            config = json.load(file)
    elif (auth_type == "basic"):
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
        headers = {}
        is_passport_auth = True
    drs_objects = config["drs_objects"]
    report_object = Report(
        schema_name = "ga4gh-testbed-report",
        schema_version = "0.1.0",
        testbed_name = "DRS Compliance Suite",
        testbed_version = "v0.0.0",
        testbed_description = "Test the compliance of a DRS implementation with GA4GH DRS v1.2.0 specification",
        platform_name = platform_name,
        platform_description = platform_description,
        input_parameters = {}
    )
    report_object.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    ##################################
    #### Phase: service-info......####
    ##################################
    service_info_phase = Phase("service info endpoint", "run all the tests for service_info endpoint")
    service_info_phase.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")

    #### Test 1: Test service-info endpoint response ####
    service_info_test_1 = get_service_info_test(
        test_name = "service-info",
        test_description = "validate service-info status code, content-type, response and error schemas",
        server_base_url = server_base_url,
        headers = headers,
        expected_status_code = "200",
        expected_content_type= "application/json")
    service_info_phase.tests.append(service_info_test_1)
    service_info_phase.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")



    #####################################
    #### Phase: drs object info......####
    #####################################

    drs_object_phase = Phase("drs object info endpoint", "run all the tests for drs object info endpoint")
    drs_object_phase.start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")

    for this_drs_object in drs_objects:

        if this_drs_object["is_present_in_drs_server"]:
            expected_status_code = "200"
            present_absent_sub_str = "present"
        else:
            expected_status_code = "404"
            present_absent_sub_str = "absent"

        drs_object_passport = None
        if is_passport_auth:
            drs_object_passport = this_drs_object["passport"]

        this_drs_object_test = get_drs_object_test(
            test_name = "run test cases on the drs object info endpoint for drs id = "
                        + this_drs_object["id"] + ". drs object is "+present_absent_sub_str+" in the drs server",
            test_description = "validate drs object status code, content-type, response "
                               "and error schemas when drs object is "+present_absent_sub_str+" in the drs server",
            drs_object_id = this_drs_object["id"],
            server_base_url = server_base_url,
            headers = headers,
            expected_status_code = expected_status_code,
            expected_content_type = "application/json",
            is_passport_auth = is_passport_auth,
            drs_object_passport = drs_object_passport
        )
        drs_object_phase.tests.append(this_drs_object_test)
    drs_object_phase.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")

    report_object.phases.append(service_info_phase)
    report_object.phases.append(drs_object_phase)
    report_object.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    report_json = generate_report_json(report_object)
    return report_json

def get_service_info_test(
        test_name,
        test_description,
        server_base_url,
        headers,
        expected_status_code,
        expected_content_type):
    #### Service Info Test Cases ####
    #### 1. response status = 200 ####
    service_info_test_1_start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    SERVICE_INFO_URL = "/service-info"
    response = requests.request(method = "GET", url = server_base_url + SERVICE_INFO_URL, headers = headers)
    # check that response_status is 200 -> if no -> case fail, if yes -> case pass
    # if no -> check error response json valid or not
    # if yes -> check success response json valid or not

    # CASE: CHECK RESPONSE STATUS CODE
    case_validate_service_info_response_status = Case(
        case_name="service-info response status code validation",
        case_description="check if the response status code is " + expected_status_code,
        actual_response=response
    )
    case_validate_service_info_response_status.validate_status_code(expected_status_code)

    # CASE: CHECK RESPONSE CONTENT TYPE
    case_validate_service_info_response_content_type = Case(
        case_name="service-info response content-type validation",
        case_description="check if the content-type is " + expected_content_type,
        actual_response=response
    )
    case_validate_service_info_response_content_type.validate_content_type(expected_content_type)

    skip_case_service_info_response = False
    skip_case_service_info_error = False
    skip_case_service_info_response_msg = ""
    skip_case_service_info_error_msg = ""

    if case_validate_service_info_response_status.status != "PASS" \
            or case_validate_service_info_response_content_type.status != "PASS":
        skip_case_service_info_response = True
        skip_case_service_info_response_msg = "skip validating service-info success response because status!={}" \
                                              " or content-type!={}".format(expected_status_code, expected_content_type)
    else:
        skip_case_service_info_error = True
        skip_case_service_info_error_msg = "skip validating service-info error response because status={}" \
                                           " and content-type={}".format(expected_status_code, expected_content_type)

    # CASE: CHECK SUCCESS RESPONSE SCHEMA
    case_validate_service_info_response_schema = Case(
        case_name="service-info success response schema validation",
        case_description="validate service-info response schema when status= 200",
        actual_response=response,
        response_schema_file = SCHEMA_SERVICE_INFO,
        skip_case=skip_case_service_info_response,
        skip_case_message=skip_case_service_info_response_msg
    )
    case_validate_service_info_response_schema.validate_response_schema()

    # CASE: CHECK ERROR RESPONSE SCHEMA
    case_validate_service_info_error_response_schema = Case(
        case_name="service-info error response schema validation",
        case_description="validate service-info response schema when status!= 200",
        actual_response=response,
        response_schema_file = SCHEMA_ERROR,
        skip_case=skip_case_service_info_error,
        skip_case_message=skip_case_service_info_error_msg
    )
    case_validate_service_info_error_response_schema.validate_response_schema()

    service_info_test_obj = TestbedTest(test_name,test_description)
    # Add cases to test object
    service_info_test_obj.cases = [
        case_validate_service_info_response_status,
        case_validate_service_info_response_content_type,
        case_validate_service_info_response_schema,
        case_validate_service_info_error_response_schema
    ]
    service_info_test_obj.start_time = service_info_test_1_start_time
    service_info_test_obj.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    return service_info_test_obj

def get_drs_object_test (
        test_name,
        test_description,
        drs_object_id,
        server_base_url,
        headers,
        expected_status_code,
        expected_content_type,
        is_passport_auth,
        drs_object_passport):
    #### DRS Object Test Cases ####
    #### 1. response status = 200 ####
    drs_object_test_start_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    DRS_OBJECT_INFO_SUB_URL = "/objects/"
    if is_passport_auth:
        request_body = {"passports":[drs_object_passport]}
        response = requests.request(
            method = "POST",
            url = server_base_url + DRS_OBJECT_INFO_SUB_URL + drs_object_id,
            headers = headers,
            json = request_body)
    else:
        response = requests.request(method = "GET", url = server_base_url + DRS_OBJECT_INFO_SUB_URL + drs_object_id, headers = headers)
    # check that response_status is 200 -> if no -> case fail, if yes -> case pass
    # if no -> check error response json valid or not
    # if yes -> check success response json valid or not

    # CASE: CHECK RESPONSE STATUS CODE
    case_validate_drs_object_response_status = Case(
        case_name="drs object response status code validation",
        case_description="check if the response status code = " + expected_status_code,
        actual_response=response
    )
    case_validate_drs_object_response_status.validate_status_code(expected_status_code)

    # CASE: CHECK RESPONSE CONTENT TYPE
    case_validate_drs_object_response_content_type = Case(
        case_name="drs object response content-type validation",
        case_description="check if the content-type is " + expected_content_type,
        actual_response=response
    )
    case_validate_drs_object_response_content_type.validate_content_type(expected_content_type)

    skip_case_drs_object_response = False
    skip_case_drs_object_error = False
    skip_case_drs_object_response_msg = ""
    skip_case_drs_object_error_msg = ""

    # TODO: FIX THIS!!!
    if  (expected_status_code == "200") and (
            case_validate_drs_object_response_status.status == "PASS"
            and case_validate_drs_object_response_content_type.status == "PASS"):
        skip_case_drs_object_error = True
        skip_case_drs_object_error_msg = "skip validating drs object error response schema because " \
                                         "status={} and content-type={}".format(expected_status_code, expected_content_type)

    elif (expected_status_code == "200") and (
            case_validate_drs_object_response_status.status != "PASS"
            or case_validate_drs_object_response_content_type.status != "PASS"):
        skip_case_drs_object_response = True
        skip_case_drs_object_response_msg = "skip validating drs object success response schema because " \
                                            "status!={} or content-type!={}. Instead validate the response using error schema".format(expected_status_code, expected_content_type)

    else:
        skip_case_drs_object_response = True
        skip_case_drs_object_response_msg = "skip validating drs object success response schema because " \
                                            "expected status = {}. Instead validate the response using error schema".format(expected_status_code)

    # CASE: CHECK SUCCESS RESPONSE SCHEMA
    case_validate_drs_object_response_schema = Case(
        case_name="drs object success response schema validation",
        case_description="response status= 200",
        actual_response=response,
        response_schema_file = SCHEMA_DRS_OBJECT,
        skip_case=skip_case_drs_object_response,
        skip_case_message=skip_case_drs_object_response_msg
    )
    case_validate_drs_object_response_schema.validate_response_schema()

    # CASE: CHECK ERROR RESPONSE SCHEMA
    case_validate_drs_object_error_response_schema = Case(
        case_name="drs object error response schema validation",
        case_description="response status!= 200",
        actual_response=response,
        response_schema_file = SCHEMA_ERROR,
        skip_case=skip_case_drs_object_error,
        skip_case_message=skip_case_drs_object_error_msg
    )
    case_validate_drs_object_error_response_schema.validate_response_schema()

    drs_object_test_obj = TestbedTest(test_name,test_description)
    # Add cases to test object
    drs_object_test_obj.cases = [
        case_validate_drs_object_response_status,
        case_validate_drs_object_response_content_type,
        case_validate_drs_object_response_schema,
        case_validate_drs_object_error_response_schema
    ]
    drs_object_test_obj.start_time = drs_object_test_start_time
    drs_object_test_obj.end_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
    return drs_object_test_obj


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
    with open(output_report_file_path, 'w', encoding='utf-8') as f:
        json.dump(output_report_json, f, ensure_ascii=False, indent=4)
        
if __name__=="__main__":
    main()