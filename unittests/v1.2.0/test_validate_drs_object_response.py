from compliance_suite.validate_drs_object_response import *
from unittests.resources.mock_drs_response_access_methods import *
import unittest
from parameterized import parameterized
from ga4gh.testbed.report.case import Case

class TestValidateDRSObjectResponse(unittest.TestCase):

    def setUp(self):
        self.validator = ValidateDRSObjectResponse()
        self.mock_case = Case()

    @parameterized.expand([
        (mock_response_0, Status.FAIL),
        (mock_response_1, Status.FAIL),
        (mock_response_2, Status.PASS),
        (mock_response_3, Status.PASS),
        (mock_response_4, Status.PASS)
    ])
    def test_validate_has_access_methods(self, mock_response, expected_status):
        self.validator.set_actual_response(mock_response)
        self.validator.set_case(self.mock_case)
        self.validator.validate_has_access_methods()
        self.assertEqual(expected_status,self.validator.case.get_status())

    expected_message_0 = "access_methods is not provided. It is required and should be non-empty for a single-blob"
    expected_message_1 = "At least 'access_url' or 'access_id' is provided in all access_methods"
    expected_message_2 = "Neither 'access_url' nor 'access_id' is provided in some or all access_methods - "

    @parameterized.expand([
        (mock_response_0, Status.FAIL, [], expected_message_0),
        (mock_response_1, Status.FAIL, [], expected_message_0),
        (mock_response_2, Status.PASS, ["338e433b-e0f4-4261-9d25-1863b2dcf08d"], expected_message_1),
        (mock_response_3, Status.FAIL, ["338e433b-e0f4-4261-9d25-1863b2dcf08d"], expected_message_2 + "3"),
        (mock_response_4, Status.PASS, ["338e433b-e0f4-4261-9d25-1863b2dcf08d", "338e433b-e0f4-4261-9d25-1863b2dcf08f"],expected_message_1)
    ])
    def test_validate_has_access_info(self, mock_response, expected_status, expected_access_id_list, expected_message):
        self.validator.set_actual_response(mock_response)
        self.validator.set_case(self.mock_case)
        actual_access_id_list = self.validator.validate_has_access_info()
        self.assertEqual(expected_status,self.validator.case.get_status())
        self.assertListEqual(expected_access_id_list, actual_access_id_list, "Actual access_id list doesn't match the expected list")
        self.assertEqual(self.validator.case.get_message(),expected_message)