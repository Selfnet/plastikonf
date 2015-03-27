import subprocess
import urllib.parse
import base64
import time
import tempfile
import os

from Crypto.Cipher import DES
from hashlib import md5
#source https://gist.github.com/zhangyoufu/6046912

files = {
#"WR720" : "default_config.bin",
"WR740" :  "configs/default_config_wr740.bin.txt",
#"WR1043" : "configs/default_config_wr1043.bin.txt", #old version v1.11
"WR1043" : "configs/default_config_wr1043-v2.bin.txt", #new version v2.00
"WR841"	: "configs/default_config_wr841.bin.txt",
"WR841v9"	: "configs/default_config_wr841v9.bin.txt",
}

prices = {
	"WR740" : "20",
	"WR1043" : "45",
	"WR841":"20"
}

class Config :
	def __init__(self, fi) :
		self.data = list(map(str.strip, open(fi, "r").read().split("\n")))
		self.data = list(filter(len, self.data))
		self.key = b'\x47\x8D\xA5\x0B\xF9\xE3\xD2\xCF'
		self.crypto = DES.new( self.key, DES.MODE_ECB )

	def apply(self, prefix, subst) :
		for i in range(len(self.data)) :
			if self.data[i].find(prefix) == 0: 
				self.data[i] = prefix + " " + subst
	def encrypt(self) :
		txt = "\r\n".join(self.data).encode("utf8")
		md5sum = md5(txt).digest()
		txt = md5sum + txt + b"\0"
		padding = len(txt)%8
		txt += b"\0"*(8-padding)
		assert len(txt)%8==0
		return self.crypto.encrypt(txt)


class Device :
	def __init__(self, ip, password="admin") :
		self.ip = ip
		self.password = password
		self.user = "admin"
		self.type = None
	
	def ping(self) :
		return not bool(subprocess.call(("ping", "-c1", "-W5", self.ip), stdout=-1))
	def curl(self, path, opts=("",)) :
		try :
			cmd = [
				"curl", "-b",
				'Authorization=Basic%s'%urllib.parse.quote(b" "+base64.b64encode((self.user+":"+self.password).encode())),
				"--user", self.user+":"+self.password,
				"--connect-timeout", "5",
				"--referer", "http://192.168.0.1/",
				"-s"
			]
			cmd.extend(opts)
			cmd.append("http://%s/%s"%(self.ip, path))
			print(" ".join(cmd))
			z=subprocess.check_output(cmd).decode("cp1252")
		except subprocess.CalledProcessError:
			return False
		if z.find("Username or Password is incorrect.") != -1 :
			print("curl: wrong pw")
			return False
		
		return z
	
	def get_type(self) :
		#page = 	self.curl("frames/top.htm")
		page = 	self.curl("userRpm/StatusRpm.htm")
		if page == False :
			return False
		if page.find("WR740N") != -1 :
			return "WR740"
		elif page.find("WR720") != -1 :
			return "WR720"
		elif page.find("WR1043") != -1 :
			return "WR1043"
		elif page.find("WR841N v9") != -1 :
			return "WR841v9"
		elif page.find("WR841N") != -1 :
			return "WR841"
		
		else :
			return False

	def config_init(self) :
		self.type = self.get_type()
		#self.type = "WR841"
		if self.type == False :
			return False
		self.config = Config(files[self.type])
		return True
	
	def set_essid(self, essid) :
		self.config.apply("wlan_mbssid_str 1", essid)
	
	def set_wpakey(self, key) :
		self.config.apply("wlan_PskSecret 1", key)
	
	def set_adminpw(self, pw) :
		self.config.apply("lgn_pwd", pw)
	
	def upload_config(self) :
		blob = self.config.encrypt()
		finame = tempfile.mkstemp()[1]
		fi = open(finame, "wb")
		fi.write(blob)
		fi.close()
		r=self.upload_config_file(finame)
		os.remove(finame)
		return r
	
	def upload_config_file(self, fi) :
		r = self.curl("incoming/RouterBakCfgUpload.cfg", ("--form",  "filename=@"+fi))
		if not r :
			return False
		time.sleep(1)
		r2 = self.curl("userRpm/ConfUpdateTemp.htm")
		return r2 and r
	
		
if __name__ == "__main__" :
	d = Device("192.168.0.1")
	#print(d.ping())
	print(d.get_type())
	#print(d.curl(""))
	#d.config_init()
	#d.set_essid("Hallo")
	#d.set_wpakey("asdfghjk")
	#d.set_adminpw("root")


	
