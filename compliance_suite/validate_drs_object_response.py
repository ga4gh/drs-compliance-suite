from compliance_suite.validate_response import ValidateResponse
from ga4gh.testbed.report.status import Status

class ValidateDRSObjectResponse(ValidateResponse):
    def __init__(self):
        super().__init__()

    def validate_has_access_methods(self, is_bundle):
        """
        Validates that "access_methods" are provided and non-empty
        """
        if self.case.get_status() == Status.SKIP: # TODO: if is_bundle then SKIP this test case
            self.case.set_end_time_now()
            return
        else:
            response_json = self.actual_response.json()
            if ("access_methods" in response_json and response_json["access_methods"]):
                self.case.set_message("'access_methods' is provided and it is non-empty.")
                self.case.set_status_pass()
            else:
                if is_bundle:
                    self.case.set_message(f"access_methods is not provided. It is not required for a DRS Bundle")
                    self.case.set_status_pass()
                else:
                    self.case.set_message("'access_methods' is not provided. It is required and should be non-empty for a single-blob")
                    self.case.set_status_fail()
            self.case.set_end_time_now()
        return

    def validate_has_access_info(self, is_bundle):
        access_id_list = []
        if self.case.get_status() == Status.SKIP:
            self.case.set_end_time_now()
            return access_id_list

        response_json = self.actual_response.json()
        access_methods = response_json.get("access_methods", [])
        methods_with_no_access_info = []

        for i in range(len(access_methods)):
            access_method = access_methods[i]
            if "access_url" not in access_method and "access_id" not in access_method:
                methods_with_no_access_info.append(str(i+1))
            if "access_id" in access_method:
                access_id_list.append(access_method["access_id"])
        if (not methods_with_no_access_info) and access_methods:
            self.case.set_message(f"At least 'access_url' or 'access_id' is provided in all access_methods")
            self.case.set_status_pass()
        elif not access_methods:
            if is_bundle:
                self.case.set_message(f"access_methods is not provided. It is not required for a DRS Bundle")
                self.case.set_status_pass()
            else:
                self.case.set_message(f"access_methods is not provided. It is required and should be non-empty for a single-blob")
                self.case.set_status_fail()
        else:
            self.case.set_message(f"Neither 'access_url' nor 'access_id' is provided in some or all access_methods - {', '.join(methods_with_no_access_info)}")
            self.case.set_status_fail()

        self.case.set_end_time_now()
        return access_id_list