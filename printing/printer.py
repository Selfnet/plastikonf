#!/usr/bin/env python
from PIL import Image
import sys 
import random
import socket
import os
import tempfile
import subprocess

header = list(open(os.path.dirname(os.path.realpath(__file__))+"/header.prn", "rb").read())

class PDF2PNG :
	callstring = "convert -density 300 -crop 720x305+0+20 -background white"
	def __init__(self, png) :
		self.tf = tempfile.mkstemp(".png")[1]
		subprocess.check_call(self.callstring.split()+[png, self.tf])
	
	def __enter__(self) :
		return self.tf
		
	def __exit__(self, *_) :
		os.remove(self.tf)

def format_image(img) :
	img = Image.open(img).convert("L")
	out=list(header)
	randrange=1
	for y in range(305) :
		packet = [0x67,0, 104]
		packet.extend((0,)*90)
		
		for x in range(720) :
			if img.getpixel((719-x,y)) <250 :
				packet [int(x/8)+3] |= (1<<(7-(x&7))) 	
		packet.extend((0,)*14)
		out.extend(packet)

	out.append(0x1a)
	return bytes(out)

def print_to_ip(img ,ip, port=9100) :
	out = format_image(img)
	s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, port))
	s.send(out)
	s.close()
