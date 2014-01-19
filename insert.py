import randomcity
import tempfile
import subprocess
import os
import pymongo

c = pymongo.MongoClient()
db = c.plastikonf
devices_coll = db.devices


mac=input("MAC: ").replace(":", "").upper()
pin=input("PSK: ")

editor = os.getenv("EDITOR")
editor = editor if editor is not None else "nano"

while True :
	essid = "WH-"+randomcity.get_city()
	wpakey = randomcity.get_pw()
	adminpw = randomcity.get_pw()
	print("ESSID: "+essid)
	print("WPA  : "+wpakey)
	print("ADMIN: "+adminpw)
	c=input("[Y]es, [n]ew, [e]dit: ").lower()
	if c=="y" or c=="" :
		break
	elif c == "n" :
		continue
	elif c=="e" :
		tf = tempfile.mkstemp()[1]
		fi = open(tf, "w")
		fi.write("\n".join((essid, wpakey, adminpw)))
		fi.close()
		subprocess.call((editor, tf))
		fi=open(tf)
		essid, wpakey, adminpw = map(str.strip, fi.readlines())
		fi.close()
		os.remove(tf)
		print("ESSID: "+essid)
		print("WPA  : "+wpakey)
		print("ADMIN: "+adminpw)
		break

devices_coll.insert({"mac": mac, "pin":pin, "essid":essid, "psk": wpakey, "adminpw":adminpw, "state":"inserted", "tries":0})
