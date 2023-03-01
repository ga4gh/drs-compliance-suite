import json
from compliance_suite.report_runner import add_case_response_schema
from ga4gh.testbed.report.test import Test
from ga4gh.testbed.report.status import Status

with open("resources/good_service_info_1.json", 'r') as file:
    good_service_info_resp_1 = json.load(file)

with open("resources/bad_service_info_1.json", 'r') as file:
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



def test_good_service_info_resp_1():
    # Test if the compliance suite works as expected when
    # service_info endpoint response has all the required fields with right values
    compliance_report_test_object_1 = Test()
    compliance_report_test_object_1.set_test_name("test_good_service_info_1")
    compliance_report_test_object_1.set_test_description("testing service_info")
    schema_name = "service_info.json"
    case_name = "test schema validation 1"
    case_description = "validate service-info response schema"

    resp = SampleResponse(good_service_info_resp_1,200)

    add_case_response_schema(compliance_report_test_object_1,schema_name, case_name, case_description, resp)

    assert compliance_report_test_object_1.cases[0].case_name == "test schema validation 1"
    assert compliance_report_test_object_1.cases[0].status == Status.PASS
    assert compliance_report_test_object_1.cases[0].message == "Schema Validation Successful"

def test_bad_service_info_resp_1():
    # TODO: Raise a bug
    # Test if the compliance suite works as expected when
    # service_info endpoint response has incorrect value for type.group
    # i.e, type.group != org.ga4gh
    compliance_report_test_object_1 = Test()
    compliance_report_test_object_1.set_test_name("test_bad_service_info_1")
    compliance_report_test_object_1.set_test_description("testing service_info")
    schema_name = "service_info.json"
    case_name = "test schema validation 2"
    case_description = "validate service-info response schema"

    resp = SampleResponse(bad_service_info_resp_1,200)

    add_case_response_schema(compliance_report_test_object_1,schema_name, case_name, case_description, resp)

    assert compliance_report_test_object_1.cases[0].case_name == "test schema validation 2"
    assert compliance_report_test_object_1.cases[0].status == Status.FAIL
    assert "Stack Trace:" in compliance_report_test_object_1.cases[0].message