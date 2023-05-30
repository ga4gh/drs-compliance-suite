expected_good_mock_server_report = {
    "schema_name": "ga4gh-testbed-report",
    "schema_version": "0.1.0",
    "testbed_name": "DRS Compliance Suite",
    "testbed_version": "v1.0.3",
    "testbed_description": "Test the compliance of a DRS implementation with GA4GH DRS v1.2.0 specification",
    "platform_name": "ga4gh starter kit drs",
    "platform_description": "GA4GH reference implementation of DRS specification",
    "phases": [
        {
            "phase_name": "phase_service_info_endpoint",
            "phase_description": "run all the tests for service_info endpoint",
            "tests": [
                {
                    "test_name": "test_GET_service_info_success",
                    "test_description": "success case of GET service-info",
                    "message": "",
                    "case": [
                        {
                            "case_name": "status_code",
                            "case_description": "check if the service-info response is as expected",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Response Status Code is as expected"
                        },
                        {
                            "case_name": "content-type",
                            "case_description": "check if the response Content-Type is as expected",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Response header 'Content-Type' is as expected"
                        },
                        {
                            "case_name": "required response fields",
                            "case_description": "check if the response contains all the required attributes",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Required attributes - {} are present in the service info response"
                        },
                        {
                            "case_name": "required response service type fields",
                            "case_description": "check if the response 'type' field contains all the required attributes",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Required attributes - {} are present in the service info - type response"
                        },
                        {
                            "case_name": "required response service type fields",
                            "case_description": "check if the response 'type' field contains all the required attributes",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Required attributes - {} are present in the service info - organization response"
                        }
                    ],
                    "summary": {
                        "unknown": 0,
                        "passed": 5,
                        "warned": 0,
                        "failed": 0,
                        "skipped": 0
                    },
                    "status": "PASS"
                }
            ],
            "summary": {
                "unknown": 0,
                "passed": 5,
                "warned": 0,
                "failed": 0,
                "skipped": 0
            },
            "status": "PASS"
        },
        {
            "phase_name": "phase_drs_object_endpoint",
            "phase_description": "run all the tests for drs_object endpoint",
            "tests": [
                {
                    "test_name": "test_GET_drs_object_info_success",
                    "test_description": "success case of GET drs_object by object_id",
                    "message": "",
                    "case": [
                        {
                            "case_name": "status_code",
                            "case_description": "check if the drs object info response is as expected",
                            "log_message": [],
                            "status": "FAIL",
                            "message": "Response Status Code is not as expected"
                        },
                        {
                            "case_name": "content-type",
                            "case_description": "check if the response Content-Type is as expected",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        },
                        {
                            "case_name": "required response fields",
                            "case_description": "check if the response contains all the required attributes",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        }
                    ],
                    "summary": {
                        "unknown": 0,
                        "passed": 0,
                        "warned": 0,
                        "failed": 1,
                        "skipped": 2
                    },
                    "status": "FAIL"
                },
                {
                    "test_name": "test_GET_drs_object_info_not_found",
                    "test_description": "GET drs_object by object_id when object_id is not present in the database",
                    "message": "",
                    "case": [
                        {
                            "case_name": "status_code",
                            "case_description": "check if the drs object info response is as expected",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Response Status Code is as expected"
                        },
                        {
                            "case_name": "content-type",
                            "case_description": "check if the response Content-Type is as expected",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Response header 'Content-Type' is as expected"
                        },
                        {
                            "case_name": "required response fields",
                            "case_description": "check if the response contains all the required attributes",
                            "log_message": [],
                            "status": "FAIL",
                            "message": "Required attributes - {} are absent in the drs object info response for object_id = {}"
                        }
                    ],
                    "summary": {
                        "unknown": 0,
                        "passed": 2,
                        "warned": 0,
                        "failed": 1,
                        "skipped": 0
                    },
                    "status": "FAIL"
                }
            ],
            "summary": {
                "unknown": 0,
                "passed": 2,
                "warned": 0,
                "failed": 2,
                "skipped": 2
            },
            "status": "FAIL"
        }
    ],
    "summary": {
        "unknown": 0,
        "passed": 7,
        "warned": 0,
        "failed": 2,
        "skipped": 2
    },
    "status": "FAIL"
}

expected_bad_mock_server_report = {
    "schema_name": "ga4gh-testbed-report",
    "schema_version": "0.1.0",
    "testbed_name": "DRS Compliance Suite",
    "testbed_version": "v1.0.3",
    "testbed_description": "Test the compliance of a DRS implementation with GA4GH DRS v1.2.0 specification",
    "platform_name": "ga4gh starter kit drs",
    "platform_description": "GA4GH reference implementation of DRS specification",
    "phases": [
        {
            "phase_name": "phase_service_info_endpoint",
            "phase_description": "run all the tests for service_info endpoint",
            "tests": [
                {
                    "test_name": "test_GET_service_info_success",
                    "test_description": "success case of GET service-info",
                    "message": "",
                    "case": [
                        {
                            "case_name": "status_code",
                            "case_description": "check if the service-info response is as expected",
                            "log_message": [],
                            "status": "FAIL",
                            "message": "Response Status Code is not as expected"
                        },
                        {
                            "case_name": "content-type",
                            "case_description": "check if the response Content-Type is as expected",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        },
                        {
                            "case_name": "required response fields",
                            "case_description": "check if the response contains all the required attributes",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        },
                        {
                            "case_name": "required response service type fields",
                            "case_description": "check if the response 'type' field contains all the required attributes",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        },
                        {
                            "case_name": "required response service type fields",
                            "case_description": "check if the response 'type' field contains all the required attributes",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        }
                    ],
                    "summary": {
                        "unknown": 0,
                        "passed": 0,
                        "warned": 0,
                        "failed": 1,
                        "skipped": 4
                    },
                    "status": "FAIL"
                }
            ],
            "summary": {
                "unknown": 0,
                "passed": 0,
                "warned": 0,
                "failed": 1,
                "skipped": 4
            },
            "status": "FAIL"
        },
        {
            "phase_name": "phase_drs_object_endpoint",
            "phase_description": "run all the tests for drs_object endpoint",
            "tests": [
                {
                    "test_name": "test_GET_drs_object_info_success",
                    "test_description": "success case of GET drs_object by object_id",
                    "message": "",
                    "case": [
                        {
                            "case_name": "status_code",
                            "case_description": "check if the drs object info response is as expected",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Response Status Code is as expected"
                        },
                        {
                            "case_name": "content-type",
                            "case_description": "check if the response Content-Type is as expected",
                            "log_message": [],
                            "status": "PASS",
                            "message": "Response header 'Content-Type' is as expected"
                        },
                        {
                            "case_name": "required response fields",
                            "case_description": "check if the response contains all the required attributes",
                            "log_message": [],
                            "status": "FAIL",
                            "message": "Required attributes - {} are absent in the drs object info response for object_id = {}"
                        }
                    ],
                    "summary": {
                        "unknown": 0,
                        "passed": 2,
                        "warned": 0,
                        "failed": 1,
                        "skipped": 0
                    },
                    "status": "FAIL"
                },
                {
                    "test_name": "test_GET_drs_object_info_not_found",
                    "test_description": "GET drs_object by object_id when object_id is not present in the database",
                    "message": "",
                    "case": [
                        {
                            "case_name": "status_code",
                            "case_description": "check if the drs object info response is as expected",
                            "log_message": [],
                            "status": "FAIL",
                            "message": "Response Status Code is not as expected"
                        },
                        {
                            "case_name": "content-type",
                            "case_description": "check if the response Content-Type is as expected",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        },
                        {
                            "case_name": "required response fields",
                            "case_description": "check if the response contains all the required attributes",
                            "log_message": [],
                            "status": "SKIP",
                            "message": "Skipping this case as response status is not as expected"
                        }
                    ],
                    "summary": {
                        "unknown": 0,
                        "passed": 0,
                        "warned": 0,
                        "failed": 1,
                        "skipped": 2
                    },
                    "status": "FAIL"
                }
            ],
            "summary": {
                "unknown": 0,
                "passed": 2,
                "warned": 0,
                "failed": 2,
                "skipped": 2
            },
            "status": "FAIL"
        }
    ],
    "summary": {
        "unknown": 0,
        "passed": 2,
        "warned": 0,
        "failed": 3,
        "skipped": 6
    },
    "status": "FAIL"
}