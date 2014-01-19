from string import Template
import zmq
import subprocess
import config

tpl = Template(open("netctl.template", "r").read())

ctx=zmq.Context()
sock=ctx.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:54654")
while True :
	rx = sock.recv_json()
	cmd = rx["cmd"]
	resp = {"status":"ok"}
	if cmd == "connect" :
		essid = rx["essid"]
		wpkey = rx["wpakey"]
		fi = open("/etc/netctl/"+config.netctl_profile, "w")
		fi.write(tpl.substitute(iface=config.iface, essid=essid, wpakey=wpkey))
		fi.close()
		print("Connecting to "+essid)
		r=subprocess.call(("netctl", "start", config.netctl_profile))
		if r :
			resp["status"] = "failed"
			resp["reason"] = "unable to conenct to wifi"
			print("Connection failed")
		else :
			print("Connected")
	
	elif cmd == "disconnect" :
		print("Disconnecting...")
		r=subprocess.call(("netctl", "stop", config.netctl_profile))
		if r :
			resp["status"] = "failed"
			resp["reason"] = "unable to disconnect from wifi"
			print("Disconnect failed")
		else :
			print("Disconnected")
	
	sock.send_json(resp)
		
