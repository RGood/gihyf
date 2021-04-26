rm -rf bin lib include

virtualenv . -p /usr/bin/python3 

./bin/pip install flask pymongo praw configparser pyyaml prawdditions dnspython
