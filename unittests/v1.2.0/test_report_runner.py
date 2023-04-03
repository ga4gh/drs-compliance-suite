from compliance_suite.report_runner import *
import re

expect_final_json = json.loads(
    open("unittests/output/expected_good.json", "r").read()
)

def string_format(json):
    return str(json).replace("'", '"').replace("\\","")

expect_json_s = string_format(expect_final_json)

def remove_timestamps(actual_final_json):
    # remove timestamps, otherwise assert will fail 100%
    actual_final_json["start_time"] = ""
    actual_final_json["end_time"] = ""
    for phase in actual_final_json["phases"]:
        phase["start_time"] = ""
        phase["end_time"] = ""
        for test in phase["tests"]:
            test["start_time"] = ""
            test["end_time"] = ""
            for case in test["cases"]:
                case["start_time"] = ""
                case["end_time"] = ""
    return string_format(actual_final_json)

def validate_timestamp_format(timestamp):
    good_timestamp = re.search("(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})Z", timestamp)
    return good_timestamp != None

#def test_report_runner():

#    actual_final_json = json.loads(report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
#                                    platform_name = "good mock server",
#                                    platform_description = "test",
#                                    auth_type = "basic"))
#    actual_json_s = remove_timestamps(actual_final_json)
#    assert actual_json_s == expect_json_s



def test_auth_type():
    # run report runner 4 times, test auth type each time, see if valid json comes out to be 1 count
    unauth = 0
    auth = 0

    auth_list = ["none", "basic", "bearer", "passport"]
    for type in auth_list:

        actual_final_json = json.loads(report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                        platform_name = "good mock server",
                                        platform_description = "test",
                                        auth_type = type))
        
        assert validate_timestamp_format(actual_final_json["start_time"])
        assert validate_timestamp_format(actual_final_json["end_time"])
        for phase in actual_final_json["phases"]:
            assert validate_timestamp_format(phase["start_time"])
            assert validate_timestamp_format(phase["end_time"])
            for test in phase["tests"]:
                assert validate_timestamp_format(test["start_time"])
                assert validate_timestamp_format(test["end_time"])
                for case in test["cases"]:
                    assert validate_timestamp_format(case["start_time"])
                    assert validate_timestamp_format(case["end_time"])
        
        if actual_final_json["summary"]["passed"] == 27:
            auth += 1
        elif actual_final_json["summary"]["passed"] == 1:
            unauth += 1
    assert unauth == 3
    assert auth == 1