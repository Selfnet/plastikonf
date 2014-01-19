import subprocess
import random
import os

def get_city() :
	fi = open("worldcitiespop.txt", "rb")
	size = os.fstat(fi.fileno()).st_size
	while True :
		pos = random.randrange(61, size-100)
		fi.seek(pos)
		fi.readline()
		city = fi.readline().strip().split(b",")[2]
		if all(map(lambda z:z<128 ,city)) and len(city) <= 8 and city.find(b" ") == -1 and city.find(b"'") == -1 and city.find (b"`") == -1:
			fi.close()
			return city.decode()
	


def get_pw() :
	return subprocess.check_output(("pwgen", "-nvc")).decode().strip()
