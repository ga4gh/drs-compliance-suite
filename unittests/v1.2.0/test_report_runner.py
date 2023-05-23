from compliance_suite.report_runner import *

auth_types = ["none", "basic", "bearer", "passport"]
def test_report_runner():

    good_report = report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                            platform_name = "good mock server",
                                            platform_description = "test",
                                            drs_version = "1.2.0",
                                            config_file = "compliance_suite/config/config_samples/config_basic.json")

    actual_good_json = json.loads(good_report.to_json())

    # TODO: None and BearerAuth 

    # remove timestamps, otherwise assert will fail 100%
    actual_good_json["start_time"] = ""
    actual_good_json["end_time"] = ""
    for phase in actual_good_json["phases"]:
        phase["start_time"] = ""
        phase["end_time"] = ""
        for test in phase["tests"]:
            test["start_time"] = ""
            test["end_time"] = ""
            for case in test["cases"]:
                case["start_time"] = ""
                case["end_time"] = ""

    expect_final_json = json.loads(
        open("unittests/output/expected_good.json", "r").read()
    )
    actual_json_s = str(actual_good_json).replace("'", '"').replace("\\","")
    expect_json_s = str(expect_final_json).replace("'", '"').replace("\\","")

    # expect_final_json will vary throughout production of cs
    assert actual_json_s == expect_json_s

def test_send_request():
    for auth_type in auth_types:
        
        auth_token = "user-1"

        request_body = {}
        if auth_type == "passport":
            request_body["passports"] = auth_token

        headers = {}
        if auth_type == "basic":
            headers = {"Authorization": "Basic {}".format(auth_token)}
        if auth_type == "bearer":
            headers = {"Authorization": "Bearer {}".format(auth_token)}


        response = send_request("http://localhost:8089/ga4gh/drs/v1",
                                SERVICE_INFO_URL,
                                auth_type,
                                auth_token)
        
        
        actual_response = requests.request(method = "GET",
                                            url = "http://localhost:8089/ga4gh/drs/v1" + SERVICE_INFO_URL,
                                            params = {},
                                            json = {},
                                            headers = headers)

def test_add_common_test_cases():
    return
        
def test_add_test_case_common():
    return

def test_add_access_methods_test_case():
    return