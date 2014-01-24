# Author : MM
# Purpose: Basic wrapper for communication

import struct
import json

LENGTH_FORMAT = "<I"
UINT_LEN_BYTES = 4

# Only works on primitives! lists and dicts and ints and stuff
def send_data(socket, obj):
	data = json.dumps(obj)
	return _send_frame(data)

# Returns an object that is being sent to us
def get_data(socket):
	return json.loads(_get_frame(socket))

def _get_frame(socket):
	read_len = struct.unpack(LENGTH_FORMAT, socket.recv(UINT_LEN_BYTES))[0]
	data = ""
	while len(data) < read_len:
		data += socket.recv(read_len - len(data))
	return data

def _send_frame(socket, data):
	try:
		length = struct.pack(LENGTH_FORMAT, len(data))
		socket.send(length + data)
	except:
		return False
	return True

