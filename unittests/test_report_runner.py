import json
from compliance_suite.report_runner import *

def test_report_runner():

    actual_final_json = json.loads(report_runner(server_base_url = "http://localhost:8089/ga4gh/drs/v1",
                                    platform_name = "good mock server",
                                    platform_description = "test",
                                    auth_type = "basic"))

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
            
    expect_final_json = json.loads(
        open("unittests/output/expected_good.json", "r").read()
    )
    actual_json_s = str(actual_final_json).replace("'", '"').replace("\\","")
    expect_json_s = str(expect_final_json).replace("'", '"').replace("\\","")

    assert actual_json_s == expect_json_s