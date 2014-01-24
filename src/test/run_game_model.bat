start cmd.exe /K "python ../server/server.py"
ping -n 1 127.0.0.1
start cmd.exe /K "python ../client/client.py 127.0.0.1"
start cmd.exe /K "python ../client/client.py 127.0.0.1"
start cmd.exe /K "python ../client/client.py 127.0.0.1"
start cmd.exe /K "python ../client/client.py 127.0.0.1"