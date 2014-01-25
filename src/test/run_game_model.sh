#! /bin/sh

python $(dirname $0)/../server/server.py&
sleep 1
python $(dirname $0)/../client/client.py 127.0.0.1&
python $(dirname $0)/../client/client.py 127.0.0.1&
python $(dirname $0)/../client/client.py 127.0.0.1&
python $(dirname $0)/../client/client.py 127.0.0.1&
