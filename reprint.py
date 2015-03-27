import pymongo

c = pymongo.MongoClient()
db = c.plastikonf
devices_coll = db.devices


while True:
	print("Enter MAC to reprint")
	mac=input("MAC: ").strip().replace(":", "").upper()



	r=devices_coll.update({"mac": mac}, {"$set":{"state":"configured"}})
	if r["nModified"] != 1:
		print("not found")
