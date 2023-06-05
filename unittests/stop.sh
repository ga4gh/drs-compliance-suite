#!/bin/sh

kill -9 `cat bad_pid.txt`
rm bad_pid.txt
rm bad.log

kill -9 `cat good_none_pid.txt`
rm good_none_pid.txt
rm good_none.log

kill -9 `cat good_basic_pid.txt`
rm good_basic_pid.txt
rm good_basic.log

kill -9 `cat good_bearer_pid.txt`
rm good_bearer_pid.txt
rm good_bearer.log

kill -9 `cat good_passport_pid.txt`
rm good_passport_pid.txt
rm good_passport.log
