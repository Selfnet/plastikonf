import randomcity
import tempfile
import os
import pymongo
import time
import config

if config.speech_enable :
	import speechd
	speaker = speechd.Speaker("plastikonf")
	speaker.set_output_module("espeak")

def say(m) :
	if config.speech_enable :
		speaker.speak(m)

c = pymongo.MongoClient()
db = c.plastikonf
devices_coll = db.devices



while True :
	say("enter MAC")
	mac=input("MAC: ").strip().replace(":", "").upper()
	if len(tuple(devices_coll.find({"mac": mac}))) > 0 :
		say("duplicate MAC")
		print("duplicate MAC")
		continue
	if len(mac) != 12 or not all(map(lambda z: z.isdigit() or z in "ABCDEF", mac)):
		say("invalid MAC")
		print("invalid MAC")
		continue
	pin=input("PIN: ").strip()
	if len(pin) != 8 or not all(map(str.isdigit, pin)) :
		say("invalid PIN")
		print("invalid PIN")
		continue

	editor = os.getenv("EDITOR")
	editor = editor if editor is not None else "nano"

	while True :
		essid = "WH-"+randomcity.get_city()
		wpakey = randomcity.get_pw()
		adminpw = randomcity.get_pw()
		print("ESSID: "+essid)
		print("WPA  : "+wpakey)
		print("ADMIN: "+adminpw)
		say("please confirm")
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

	devices_coll.insert({"mac": mac, "pin":pin, "essid":essid, "psk": wpakey, "adminpw":adminpw, "state":"inserted", "tries":0, "at":int(time.time())})
