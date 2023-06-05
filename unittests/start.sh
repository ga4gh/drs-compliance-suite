#!/bin/sh

nohup python unittests/bad_mock_server.py --auth_type "none" --app_host "0.0.0.0" --app_port "8088" > bad.log 2>&1 &
echo $! > bad_pid.txt

nohup python unittests/good_mock_server_v1.2.0.py --auth_type "none" --app_host "0.0.0.0" --app_port "8089" > good_none.log 2>&1  &
echo $! > good_none_pid.txt

nohup python unittests/good_mock_server_v1.2.0.py --auth_type "basic" --app_host "0.0.0.0" --app_port "8090" > good_basic.log 2>&1 &
echo $! > good_basic_pid.txt

nohup python unittests/good_mock_server_v1.2.0.py --auth_type "bearer" --app_host "0.0.0.0" --app_port "8091" > good_bearer.log 2>&1 &
echo $! > good_bearer_pid.txt

nohup python unittests/good_mock_server_v1.2.0.py --auth_type "passport" --app_host "0.0.0.0" --app_port "8092" > good_passport.log 2>&1 &
echo $! > good_passport_pid.txt
