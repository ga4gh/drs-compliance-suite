import unittest
from parameterized import parameterized
from compliance_suite.report_runner import add_access_methods_test_case
from unittest.mock import patch, Mock

class TestReportRunner(unittest.TestCase):

    @parameterized.expand([
        ("has_access_methods"),
        ("has_access_info")])
    @patch('compliance_suite.report_runner.ValidateDRSObjectResponse')
    def test_add_access_methods_test_case(self, case_type, MockValidateDRSObjectResponse):

        test_object = Mock()
        case_description = "Test case for access methods"
        endpoint_name = "Test endpoint"
        response = Mock()
        mock_validate_drs_response = Mock()
        MockValidateDRSObjectResponse.return_value = mock_validate_drs_response
        access_id_list = add_access_methods_test_case(test_object, case_type, case_description, endpoint_name, response)

        # Assertions
        test_object.add_case.assert_called()
        test_case = test_object.add_case.return_value
        test_case.set_case_name.assert_called_with(f"{endpoint_name} has access information")
        test_case.set_case_description.assert_called_with(case_description)
        mock_validate_drs_response.set_case.assert_called_with(test_case)
        mock_validate_drs_response.set_actual_response.assert_called_with(response)
        test_case.set_end_time_now.assert_called()

        if case_type == "has_access_methods":
            mock_validate_drs_response.validate_has_access_methods.assert_called()
            mock_validate_drs_response.validate_has_access_info.assert_not_called()
            self.assertIsNone(access_id_list)
        else:
            mock_validate_drs_response.validate_has_access_methods.assert_not_called()
            mock_validate_drs_response.validate_has_access_info.assert_called()