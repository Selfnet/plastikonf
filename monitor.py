import pymongo
import sys
import termcolor
import time
import subprocess
c = pymongo.MongoClient()
db = c.plastikonf
devices_coll = db.devices
while True :
	rows, columns = map(int, subprocess.check_output(("stty", "size")).split())
	sys.stdout.write("\x1b[2J") #cls
	sys.stdout.write("\x1b[H") #home
	sys.stdout.write("MAC".ljust(14))
	sys.stdout.write("ESSID".ljust(14))
	sys.stdout.write("state".ljust(14))
	sys.stdout.write("\n")
	for dev in devices_coll.find().sort("at", pymongo.DESCENDING).limit(rows-2) :
		state = dev["state"]
		out = ""
		out += dev["mac"].ljust(14)
		out += dev["essid"].ljust(14)
		out += dev["state"].ljust(14)
		if state == "finalized" :
			out = termcolor.colored(out, "green")
		elif state == "configured"  :
			out = termcolor.colored(out, "yellow")
		sys.stdout.write(out)
		sys.stdout.write("\n")
	time.sleep(1)
