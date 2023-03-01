from compliance_suite.report_runner import *

def test_constructor():

    tvr = ValidateResponse()
    assert tvr.actual_response == ""
    assert tvr.expected_response == ""
    assert tvr.response_schema_file == ""
    assert tvr.case == ""

def test_valid_status_code():
    actual_json = json.loads(report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                            platform_name = "good mock server",
                                            platform_description = "test",
                                            auth_type = "basic"))
    for phase in actual_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][0]
            assert cases["message"] == "response status code = 200"
            assert cases["status"] == "PASS"
    
def test_valid_content_type():
    actual_json = json.loads(report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                            platform_name = "good mock server",
                                            platform_description = "test",
                                            auth_type = "basic"))

    for phase in actual_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][1]
            assert cases["message"] == "content type = application/json"
            assert cases["status"] == "PASS"
    
def test_valid_response_schema():
    actual_json = json.loads(report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                            platform_name = "good mock server",
                                            platform_description = "test",
                                            auth_type = "basic"))

    for phase in actual_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][2]
            assert cases["message"] == "Schema Validation Successful"
            assert cases["status"] == "PASS"
    