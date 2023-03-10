import json
from unittests.utils import *
from compliance_suite.report_runner import *
from compliance_suite.validate_response import *
from ga4gh.testbed.report.test import Test
from ga4gh.testbed.report.status import Status
from unittests.resources.expected_drs_objects import *

drs_id = "697907bf-d5bd-433e-aac2-1747f1faf366"

# spec has required fields
# unittest tests if cs is testing correctly
# check validate schema code runs bad drs object, expect a fail or error from cs

# import drs_object.json

def new_test_object(test_name, test_desc):
    test_obj = Test()
    test_obj.set_test_name(test_name)
    test_obj.set_test_description(test_desc)
    return test_obj

def test_valid_drs_object():
    # test for good drs-object
    test_object = new_test_object("test_valid_drs_object", "testing drs-object")
    schema_name = "v1.2.0/drs_object.json"
    case_name = "test valid drs-object"
    case_description = "validate drs-object "

    response = MockResponse(expected_good_drs_object, 200, {})

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.PASS

def test_invalid_id():

    # test for missing or not string drs_id field
    # expect status == "FAIL"

    test_object = new_test_object("test_invalid_id", "testing drs-object")
    schema_name = "v1.2.0/drs_object.json"
    case_name = "test invalid id"
    case_description = "validate drs-object id"

    response = MockResponse(expected_bad_drs_objects[1], 200, {})

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_self_uri():

    test_object = new_test_object("test_invalid_self_uri", "testing drs-object")
    schema_name = "v1.2.0/drs_object.json"
    case_name = "test invalid self_uri"
    case_description = "validate drs-object self uri"

    response = MockResponse(expected_bad_drs_objects[3], 200, {})

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_size():

    test_object = new_test_object("test_invalid_size", "testing drs-object")
    schema_name = "v1.2.0/drs_object.json"
    case_name = "test invalid size"
    case_description = "validate drs-object size"

    response = MockResponse(expected_bad_drs_objects[2], 200, {})

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_created_time():

    test_object = new_test_object("test_invalid_created_time", "testing drs-object")
    schema_name = "v1.2.0/drs_object.json"
    case_name = "test invalid created_time"
    case_description = "validate drs-object created_time"

    response = MockResponse(expected_bad_drs_objects[4], 200, {})

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_checksums():

    test_object = new_test_object("test_invalid_checksums", "testing drs-object")
    schema_name = "v1.2.0/drs_object.json"
    case_name = "test invalid checksums"
    case_description = "validate drs-object checksums"

    response = MockResponse(expected_bad_drs_objects[0], 200, {})

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL