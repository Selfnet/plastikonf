import zmq
ctx=zmq.Context()
sock=ctx.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:54654")
sock.send_json({"cmd":"connect", "essid": "TP-LINK_62E826", "wpakey":"01817119"})
print(sock.recv_json())

try :
	print("asd")
	raise ValueError
	print("asdf")
except :
	pass
finally :
	print("asdg")
