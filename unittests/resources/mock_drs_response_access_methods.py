from unittests.utils import MockResponse

# access_methods are present but empty
mock_response_0 = MockResponse(response = {"access_methods" : []})

# access_methods are absent
mock_response_1 = MockResponse(response = {"test_key" : "test_value"})

# Access methods are present, with one method containing "access_id" and another method containing "access_url"
mock_response_2 = MockResponse(response = {"access_methods" : [
    {"access_id":"338e433b-e0f4-4261-9d25-1863b2dcf08d","type":"https"},
    {"access_url":{"url":"s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"},"type":"s3","region":"us-east-2"}
]})

# Access methods are present, with one method containing "access_id",
# another method containing "access_url", and the last method being empty.
mock_response_3 = MockResponse(response = {"access_methods" : [
    {"access_id":"338e433b-e0f4-4261-9d25-1863b2dcf08d","type":"https"},
    {"access_url":{"url":"s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"},"type":"s3","region":"us-east-2"},
    {}
]})

# Access methods are present, with one method containing "access_id",
# another method containing "access_url", and the last method containing both "access_id" and "access_url".
mock_response_4 = MockResponse(response = {"access_methods" : [
    {"access_id":"338e433b-e0f4-4261-9d25-1863b2dcf08d","type":"https"},
    {"access_url":{"url":"s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"},"type":"s3","region":"us-east-2"},
    {"access_id":"338e433b-e0f4-4261-9d25-1863b2dcf08f","access_url":{"url":"s3://ga4gh-demo-data/phenopackets/Zhang-2009-EDA-proband.json"},"type":"http"}
]})