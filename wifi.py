import zmq
ctx=zmq.Context()
sock=ctx.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:54654")

def connect(essid, wpakey) :
	disconnect()
	sock.send_json({"cmd":"connect", "essid": essid, "wpakey":wpakey})
	return sock.recv_json()

def disconnect() :
	sock.send_json({"cmd":"disconnect"})
	return sock.recv_json()

