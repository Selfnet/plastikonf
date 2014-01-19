import util
import pymongo
import time
import wifi
import device as devlib

c = pymongo.MongoClient()
db = c.plastikonf
devices_coll = db.devices
wifis_coll = db.wifis

while True :
	wifis = tuple(map(lambda z: z["mac"], wifis_coll.find()))
	
	devices = tuple(devices_coll.find({"state":"inserted", "mac":{"$in":wifis}}).sort("tries", pymongo.ASCENDING))
	if len(devices) == 0:
		print("No configureable devices found, retrying in 1sec")
		time.sleep(1)
		continue
	device = devices[0]
	old_essid = util.essid_from_mac(device["mac"])
	pin = device["pin"]
	print("Selected "+old_essid+", try #"+str(device["tries"]))
	print("Trying to connect to "+old_essid)
	r=wifi.connect(old_essid, pin)
	if r["status"] != "ok" :
		print("Couldn't connect because "+r["reason"])
		devices_coll.update({"_id":device["_id"]}, {"$inc": {"tries": 1}})
		time.sleep(1)
		continue
	print("Connected, trying to upload config")
	dev = devlib.Device("192.168.0.1")
	if not dev.ping() :
		print("Device not reachable")
		devices_coll.update({"_id":device["_id"]}, {"$inc": {"tries": 1}})
		time.sleep(1)
		continue
	if not dev.config_init() :
		print("Device not accessible")
		devices_coll.update({"_id":device["_id"]}, {"$inc": {"tries": 1}})
		time.sleep(1)
		continue
	dev.set_essid(device["essid"])
	dev.set_wpakey(device["psk"])
	dev.set_adminpw(device["adminpw"])
	if not dev.upload_config() :
		print("Config upload failed")
		devices_coll.update({"_id":device["_id"]}, {"$inc": {"tries": 1}})
		time.sleep(1)
		continue
	
	print("All done")
	devices_coll.update({"_id":device["_id"]}, {"$set": {"state": "configured"}})
	#wifi.disconnect()
	
	
	
