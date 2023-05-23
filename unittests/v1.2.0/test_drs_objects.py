"""

import json
from unittests.utils import *
from compliance_suite.report_runner import *
from compliance_suite.validate_response import *
from ga4gh.testbed.report.test import Test
from ga4gh.testbed.report.status import Status
from unittests.resources.expected_drs_objects import *

# CONSTANTS
schema_name = "v1.2.0/drs_object.json"
test_description = "testing drs-object"

def new_test_object(test_name, test_desc):
    test_obj = Test()
    test_obj.set_test_name(test_name)
    test_obj.set_test_description(test_desc)
    return test_obj

def test_valid_drs_object():
    # test for good drs-object
    test_object = new_test_object("test_valid_drs_object", test_description)
    case_name = "test valid drs-object"
    case_description = "validate drs-object"

    response = MockResponse(response = expected_good_drs_object)

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.PASS

def test_invalid_id():

    test_object = new_test_object("test_invalid_id", test_description)
    case_name = "test invalid id"
    case_description = "validate drs-object id"

    response = MockResponse(response = expected_bad_drs_objects[1])

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_self_uri():

    test_object = new_test_object("test_invalid_self_uri", test_description)
    case_name = "test invalid self_uri"
    case_description = "validate drs-object self uri"

    response = MockResponse(response = expected_bad_drs_objects[3])

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_size():

    test_object = new_test_object("test_invalid_size", test_description)
    case_name = "test invalid size"
    case_description = "validate drs-object size"

    response = MockResponse(response = expected_bad_drs_objects[2])

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_created_time():

    test_object = new_test_object("test_invalid_created_time", test_description)
    case_name = "test invalid created_time"
    case_description = "validate drs-object created_time"

    response = MockResponse(response = expected_bad_drs_objects[4])

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

def test_invalid_checksums():

    test_object = new_test_object("test_invalid_checksums", test_description)
    case_name = "test invalid checksums"
    case_description = "validate drs-object checksums"

    response = MockResponse(response = expected_bad_drs_objects[0])

    add_case_response_schema(test_object, schema_name, case_name, case_description, response)

    assert test_object.cases[0].status == Status.FAIL

"""