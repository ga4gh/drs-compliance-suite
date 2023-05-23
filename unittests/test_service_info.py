"""

import json
from compliance_suite.report_runner import *
from unittests.utils import *
from ga4gh.testbed.report.test import Test
from ga4gh.testbed.report.status import Status

# CONSTANTS

schema_name = "service_info.json"
test_description = "testing service-info"
expected_status_code = "200"
expected_content_type = "application/json"

with open("unittests/resources/good_service_info_1.json", 'r') as file:
    good_service_info_resp_1 = json.load(file)

with open("unittests/resources/bad_service_info_1.json", 'r') as file:
    bad_service_info_resp_1 = json.load(file)

# Response object with .json() and .status_code() methods
# This method will be used by the mock to replace requests.get
class SampleResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def status_code(self):
        return self.status_code()

def new_test_object(test_name, test_desc):
    test_obj = Test()
    test_obj.set_test_name(test_name)
    test_obj.set_test_description(test_desc)
    return test_obj


def test_good_service_info_resp():
    # Test if the compliance suite works as expected when
    # service_info endpoint response has all the required fields with right values
    test_object = new_test_object("test_good_service_info_1", test_description)
    case_name = "test schema validation 1"
    case_description = "validate service-info response schema"

    response = MockResponse(response = good_service_info_resp_1, status_code = 200)

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].case_name == "test schema validation 1"
    assert test_object.cases[0].status == Status.PASS
    assert test_object.cases[0].message == "Schema Validation Successful"

    assert response.response["type"]["group"] == "org.ga4gh"
    assert response.response["type"]["artifact"] == "drs"

def test_bad_service_info_resp():
    # TODO: Raise a bug
    # Test if the compliance suite works as expected when
    # service_info endpoint response has incorrect value for type.group
    # i.e, type.group != org.ga4gh
    test_object = new_test_object("test_bad_service_info_1", test_description)
    case_name = "test schema validation 2"
    case_description = "validate service-info response schema"

    response = MockResponse(response = bad_service_info_resp_1, status_code = 200)

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].case_name == "test schema validation 2"
    # assert test_object.cases[0].status == Status.FAIL
    # assert "Stack Trace:" in test_object.cases[0].message

def test_valid_status_code():
    # test for expected status code = 200
    # expects case status = PASS
    test_object = new_test_object("test_good_status_code", test_description)
    case_name = "test status code validation 1"
    case_description = "validate service-info status code"
    response = MockResponse(response = good_service_info_resp_1, status_code = 200)

    add_case_status_code(test_object, expected_status_code, case_name, case_description, response)

    assert test_object.cases[0].status == Status.PASS

def test_invalid_status_code():
    # test for expected status code = 500
    # expects case status = FAIL
    test_object = new_test_object("test_bad_status_code", test_description)
    case_name = "test status code validation 2"
    case_description = "validate service-info status code"
    response = MockResponse(response = bad_service_info_resp_1, status_code = 500)

    add_case_status_code(test_object, expected_status_code, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL
    
def test_valid_content_type():
    # test for matching content type
    # expects case status = PASS
    test_object = new_test_object("test_good_content_type", test_description)
    case_name = "test content type validation 1"
    case_description = "validate service-info content type"
    response = MockResponse(good_service_info_resp_1, 200, {"Content-Type": "application/json"})

    add_case_content_type(test_object, expected_content_type, case_name, case_description, response)

    assert test_object.cases[0].status == Status.PASS

def test_invalid_content_type():
    # test for matching content type
    # expects case status = PASS
    test_object = new_test_object("test_bad_content_type", test_description)
    case_name = "test content type validation 2"
    case_description = "validate service-info content type"
    response = MockResponse(bad_service_info_resp_1, 200, {"Content-Type": "something else"})

    add_case_content_type(test_object, expected_content_type, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

"""