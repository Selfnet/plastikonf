import subprocess
import pymongo
import config
import time

c = pymongo.MongoClient()
db = c.plastikonf
wifis_coll = db.wifis

while True :
	try :
		x=subprocess.check_output(("iwlist", config.iface, "scan"))
	except subprocess.CalledProcessError :
		time.sleep(1)
		continue
	l=x.decode().split("\n")
	#essids_scanned = filter(len, map(lambda z: z.strip()[7:-1], filter(lambda z: "ESSID:" in z, l)))
	#macs_scanned = map(lambda z: z.strip().split("Address:")[1].strip().replace(":", ""), filter(lambda z: "Address:" in z, l))
	wifis_scanned={}
	for w in map(str.strip, l) :
		if "Address:" in w :
			lastmac = w.strip().split("Address:")[1].strip().replace(":", "")
			wifis_scanned[lastmac] = None
		elif "ESSID:" in w :
			wifis_scanned[lastmac] = w.strip()[7:-1]
	wifis_scanned = set(wifis_scanned.items())
	wifis_db = set(map(lambda z: (z["mac"], z["essid"]), wifis_coll.find()))
	print(wifis_scanned-wifis_db) #insert
	print(wifis_db-wifis_scanned) #drop

	for w in wifis_scanned-wifis_db :
		wifis_coll.insert({"essid": w[1], "mac": w[0]})

	for w in wifis_db-wifis_scanned :
		wifis_coll.remove({"essid": w[1], "mac": w[0]})
		
	time.sleep(1)
