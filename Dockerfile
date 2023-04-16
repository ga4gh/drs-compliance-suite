# base image
FROM python:3.11-slim-bullseye

# set a directory for the app
WORKDIR /usr/src/app

# copy only required files to the container
COPY docker-requirements.txt .
COPY supported_drs_versions.py .
COPY compliance_suite /usr/src/app/compliance_suite

# set python path to current dir
ENV PYTHONPATH /usr/src/app

RUN pip3 install -r docker-requirements.txt

# run the command
ENTRYPOINT ["python","compliance_suite/report_runner.py"]