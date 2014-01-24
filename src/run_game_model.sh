#! /bin/sh

python server/server.py&
python client/client.py 127.0.0.1&
python client/client.py 127.0.0.1&
python client/client.py 127.0.0.1&
python client/client.py 127.0.0.1&
