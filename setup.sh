#!/usr/bin/env bash

cd /autograder/
git clone https://github.com/jdalyuml/gradescope-cpp.git autograder-source

apt-get install -y python3 python3-pip python3-dev libboost-test-dev libboost-regex-dev libboost-date-time-dev valgrind 
# apt-get install -y libsfml-dev libpulse0 xvfb
# Install required Python libraries
pip3 install -r /autograder/source/requirements.txt

# Setup student account for lockdown
adduser student --no-create-home --disabled-password --gecos ""