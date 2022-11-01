# base image
FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install drs-compliance
RUN python setup.py install

# set python path to current dir
ENV PYTHONPATH /usr/src/app

RUN pip3 install -r requirements.txt

# run the command
ENTRYPOINT ["drs-compliance"]