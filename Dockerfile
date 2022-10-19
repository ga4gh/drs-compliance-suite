# base image
FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# set python path to current dir
ENV PYTHONPATH /usr/src/app

RUN pip3 install -r requirements.txt

# run the command
ENTRYPOINT ["python3", "compliance_suite/report_runner.py"]

#docker run ga4gh/drs-compliance-suite:test --server_base_url "http://localhost:8089/ga4gh/drs/v1" --platform_name "ga4gh starter kit drs" --platform_description "GA4GH reference implementation of DRS specification" --auth_type no_auth