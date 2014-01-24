#! /bin/sh

python ../server/server.py&
sleep 1
python ../client/client.py 127.0.0.1&
python ../client/client.py 127.0.0.1&
python ../client/client.py 127.0.0.1&
python ../client/client.py 127.0.0.1&
