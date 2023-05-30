from compliance_suite.report_runner import *

auth_types = ["none", "basic", "bearer", "passport"]
port_numbers = [8089, 8090, 8091, 8092]

def json_string_formatting(json_string):
    return str(json_string).replace("'", '"').replace("\\","")

def test_report_runner():


    for authtype, port in zip(auth_types, port_numbers):
        good_report = report_runner(server_base_url = "http://localhost:" + str(port) + "/ga4gh/drs/v1",
                                    platform_name = "good mock server",
                                    platform_description = authtype,
                                    drs_version = "1.2.0",
                                    config_file = "compliance_suite/config/config_samples/config_" + authtype + ".json")

        good_json = json.loads(good_report.to_json())

        # remove timestamps, otherwise assert will fail 100%
        good_json["start_time"] = ""
        good_json["end_time"] = ""
        for phase in good_json["phases"]:
            phase["start_time"] = ""
            phase["end_time"] = ""
            for test in phase["tests"]:
                test["start_time"] = ""
                test["end_time"] = ""
                for case in test["cases"]:
                    case["start_time"] = ""
                    case["end_time"] = ""

        # USE THIS: uncomment below to generate a new expected_[none/basic/bearer/passport].json
        # with open('unittests/output/expected_good_' + authtype + '.json', 'w', encoding="utf-8") as f: json.dump(good_json, f)

        expect_final_json = json.loads(
            open("unittests/output/expected_good_" + authtype + ".json", "r").read()
        )

        actual_json_s = json_string_formatting(good_json)
        expect_json_s = json_string_formatting(expect_final_json)

        # expect_final_json will vary throughout production of cs
        assert actual_json_s == expect_json_s

def test_send_request():
    #send_request(server_base_url,endpoint_url,auth_type,auth_token,**kwargs)

    # the other endpoints for possible future tests with drs_object_info and drs_object_access
    # endpoints = [SERVICE_INFO_URL, DRS_OBJECT_INFO_URL, DRS_ACCESS_URL]

    endpoint_url = SERVICE_INFO_URL

    with open("unittests/resources/request_samples.json", 'r') as file:
        expected_response = json.load(file)


    for authtype, port in zip(auth_types, port_numbers):
        server_base_url = "http://localhost:"+str(port)+"/ga4gh/drs/v1"

        config_file = "compliance_suite/config/config_samples/config_" + authtype + ".json"

        # the other endpoints for possible future tests with drs_object_info and drs_object_access
        config_service_info, config_drs_object_info, config_drs_object_access = get_config_json(config_file)
        auth_token = config_service_info["auth_token"]

        actual_response = send_request(server_base_url, endpoint_url, authtype, auth_token)

        actual_json_s = json_string_formatting(actual_response.text)
        expect_json_s = json_string_formatting(expected_response)

        assert actual_json_s == expect_json_s


        