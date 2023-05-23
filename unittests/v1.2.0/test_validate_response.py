from compliance_suite.report_runner import *

# TODO: check authorization type (no_auth and Bearer and Passport)
# currently only running basic auth

# report_runner(server_base_url, platform_name, platform_description, drs_version, config_file)
good_report = report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                        platform_name = "good mock server",
                                        platform_description = "test",
                                        drs_version = "1.2.0",
                                        config_file = "compliance_suite/config/config_samples/config_basic.json")

bad_report = report_runner(server_base_url = "http://localhost:8088/ga4gh/drs/v1",
                                        platform_name = "bad mock server",
                                        platform_description = "test",
                                        drs_version = "1.2.0",
                                        config_file = "compliance_suite/config/config_samples/config_basic.json")

actual_good_json = json.loads(good_report.to_json())

actual_bad_json = json.loads(bad_report.to_json())

def test_constructor():
    tvr = ValidateResponse()
    assert tvr.actual_response == ""
    assert tvr.expected_response == ""
    assert tvr.response_schema_file == ""
    assert tvr.case == ""

def test_valid_status_code():
    for phase in actual_good_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][0]
            assert cases["status"] == "PASS"
    
def test_valid_content_type():
    for phase in actual_good_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][1]
            assert cases["status"] == "PASS"
    

#   report runner unittest failing at test.json line 378 
#   copying the element block was causing some weird formatting errors in my IDE
    
def test_valid_response_schema():
    for phase in actual_good_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][2]
            # TODO: Basic auth requiring access_methods (Alex is unsure abt this) 
            # assert cases["status"] == "PASS"


def test_invalid_status_code():
    for phase in actual_bad_json["phases"]:
        for test in phase["tests"]:
            cases = test["cases"][0]
            assert cases["status"] == "FAIL"

# TODO: test authorization type
def test_authorization():
    return