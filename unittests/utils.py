# Mimicks a HTTP request response
class MockResponse():
    def __init__(self, response, status_code, headers):
        self.response = response
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self.response

# Mimicks a case (see "Case" class in compliance_suite/report.py)
class MockCase():
    def __init__(self, case_name, actual_response):
        self.case_name = case_name
        self.status = "NOT TESTED"
        self.log_message = []
        self.message = ""
        self.actual_response = actual_response
        self.expected_response = ""