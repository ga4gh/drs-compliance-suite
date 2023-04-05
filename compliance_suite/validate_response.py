from ga4gh.testbed.report.status import Status
import json
import os
import jsonschema
from jsonschema import validate

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), 'schemas')

class ValidateResponse():
    def __init__(self):
        self.actual_response = ""
        self.expected_response = ""
        self.response_schema_file = ""
        self.case = ""

    def set_actual_response(self, actual_response):
        self.actual_response = actual_response

    def set_expected_response(self, expected_response):
        self.expected_response = expected_response

    def set_response_schema_file(self, response_schema_file):
        self.response_schema_file = response_schema_file

    def set_case(self, case):
        self.case = case

    def get_schema(self, schema_file_name):
        """
        Loads the given schema if available,
        Throws an error if the file does not exist
        """
        if not os.path.exists(schema_file_name):
            raise ValueError(f"Schema file '{schema_file_name}' does not exist")
        with open(schema_file_name, 'r') as file:
            schema = json.load(file)
        return schema

    def validate_response_schema(self):
        if self.case.get_status() == Status.SKIP:
            self.case.set_end_time_now()
            return
        expected_schema_file_path = os.path.join(SCHEMA_DIR, self.response_schema_file)
        expected_schema = self.get_schema(expected_schema_file_path)
        absolute_schema_file_path = os.path.dirname(os.path.abspath(expected_schema_file_path))
        reference_resolver = jsonschema.RefResolver(base_uri=f"file://{absolute_schema_file_path}/", referrer=None)
        try:
            validate(instance=self.actual_response.json(), resolver=reference_resolver, schema=expected_schema)
            self.case.set_message("Schema Validation Successful")
            self.case.set_status_pass()
        except Exception as e:
            self.case.set_message(e.message if hasattr(e,"message") else str(e))
            self.case.add_log_message(f"Stack Trace: {str(e)}")
            self.case.set_status_fail()
        self.case.set_end_time_now()

    def validate_status_code(self, expected_status_code):
        if self.case.get_status() == Status.SKIP:
            self.case.set_end_time_now()
            return
        elif str(self.actual_response.status_code) == expected_status_code:
            self.case.set_message(f"Response status code is {self.actual_response.status_code}")
            self.case.set_status_pass()
        else:
            self.case.set_message(f"Expected status code {expected_status_code}, but got {self.actual_response.status_code}")
            self.case.set_status_fail()
        self.case.set_end_time_now()

    def validate_content_type(self, expected_content_type):
        if self.case.get_status() == Status.SKIP:
            self.case.set_end_time_now()
            return
        actual_content_type = self.actual_response.headers.get("Content-Type")
        if actual_content_type is None:
            self.case.set_status_fail()
            self.case.set_message("Missing Content-Type header")
        elif actual_content_type.startswith(expected_content_type):
            self.case.set_status_pass()
            self.case.set_message("Content-Type matches expected type")
        else:
            self.case.set_status_fail()
            self.case.set_message(f"Expected Content-Type {expected_content_type}, but got Unexpected Content-Type: {actual_content_type}")
        self.case.set_end_time_now()

    def validate_expand_bundle(self):
        if self.case.get_status() != Status.SKIP:
            #print(self.actual_response.json())
            if 'contents' in self.actual_response.json():
                expected_schema_file_path = os.path.join(SCHEMA_DIR, self.response_schema_file)
                expected_schema = self.get_schema(expected_schema_file_path)
                absolute_schema_file_path = os.path.dirname(os.path.abspath(expected_schema_file_path))
                reference_resolver = jsonschema.RefResolver(base_uri=f"file://{absolute_schema_file_path}/", referrer=None)
                print()
                try:
                    validate(instance=self.actual_response.json(), resolver=reference_resolver, schema=expected_schema)
                    self.case.set_status_pass()
                    self.case.set_message("Schema Validation Successful")
                except Exception as e:
                    self.case.set_message(e.message if hasattr(e,"message") else str(e))
                    self.case.add_log_message(f"Stack Trace: {str(e)}")
                    self.case.set_status_fail()
            else:
                self.case.set_status_skip()
        else:
            pass
        self.case.set_end_time_now()
        return