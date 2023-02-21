import os
from compliance_suite.report_runner import *

def test_report_runner():
    #returns report_object.to_json()
    os.system("python compliance_suite/report_runner.py --server_base_url \"http://localhost:8089/ga4gh/drs/v1\" --platform_name \"good mock server\" --auth_type \"basic\"")
    actual_final_json = json.loads(
        open("output/drs_compliance_report.json", "r").read()
    )
    expect_final_json = json.loads(
        open("unittests/output/expect_final_json.json", "r").read()
    )
    actual_json_s = str(actual_final_json).replace("'", '"').replace("\\","")
    expect_json_s = str(expect_final_json).replace("'", '"').replace("\\","")

    assert actual_json_s == expect_json_s
