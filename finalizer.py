import util
import pymongo
import time
import config
import wifi
import device as devlib
import printing.tex
import printing.printer
import subprocess

c = pymongo.MongoClient()
db = c.plastikonf
devices_coll = db.devices
wifis_coll = db.wifis

while True :
	wifis = tuple(map(lambda z: z["essid"], wifis_coll.find()))
	
	devices = tuple(devices_coll.find({"state":"configured", "essid":{"$in":wifis}}).sort("tries", pymongo.ASCENDING))
	if len(devices) == 0:
		print("No finalizable devices found, retrying in 1sec")
		time.sleep(1)
		continue
	device = devices[0]
	print("Selected "+device["essid"])
	print("Generating device label")
	with printing.tex.TeX2PDF("label_templates/aufkleber.tex", ("label_templates/whnetz-logo-sw.pdf",), essid=device["essid"], psk=device["psk"], adminpw=device["adminpw"], mac=device["mac"]) as pdf :
		print("Printing device label")
		with printing.printer.PDF2PNG(pdf) as png :
			#subprocess.call(("display", png))
			printing.printer.print_to_ip(png, config.printer_ip)
	
	print("Generating box label")	
	with printing.tex.TeX2PDF("label_templates/aufkleber-schachtel.tex", ("label_templates/whnetz-logo-sw.pdf",), essid=device["essid"], mac=device["mac"], price=20) as pdf :
		with printing.printer.PDF2PNG(pdf) as png :
			print("Printing box label")
			#subprocess.call(("display", png))
			printing.printer.print_to_ip(png, config.printer_ip)
	devices_coll.update({"_id":device["_id"]}, {"$set": {"state": "finalized"}})
	
