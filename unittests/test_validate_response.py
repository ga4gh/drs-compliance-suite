import json
from compliance_suite.validate_response import ValidateResponse

def test_constructor():

    tvr = ValidateResponse()
    assert tvr.actual_response == ""
    assert tvr.expected_response == ""
    assert tvr.response_schema_file == ""
    assert tvr.case == ""

def test_valid_status_code():
    tvr = ValidateResponse()
    actual_json = json.loads(
        open("unittests/output/expect_final_json.json", "r").read()
    )

    for phase in actual_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][0]
            assert cases["message"] == "response status code = 200"
            assert cases["status"] == "PASS"
    
def test_valid_content_type():
    tvr = ValidateResponse()
    actual_json = json.loads(
        open("unittests/output/expect_final_json.json", "r").read()
    )

    for phase in actual_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][1]
            assert cases["message"] == "content type = application/json"
            assert cases["status"] == "PASS"
    
def test_valid_response_schema():
    tvr = ValidateResponse()
    actual_json = json.loads(
        open("unittests/output/expect_final_json.json", "r").read()
    )

    for phase in actual_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][2]
            assert cases["message"] == "Schema Validation Successful"
            assert cases["status"] == "PASS"
    

# need to call report_runner function but it only returns as json
# where to find attributes for tvr in this case? 
