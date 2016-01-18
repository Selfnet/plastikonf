import string
import tempfile
import subprocess
import shutil

class TeXTemplate(string.Template) :
        delimiter = "#"

class TeX2PDF :
	def __init__(self, tpl, extrafiles=(), **kwargs) :
		self.od = tempfile.mkdtemp()
		with open(tpl) as _ :
			t = TeXTemplate(_.read())
		of = open(self.od+"/"+"doc.tex", "w")
		of.write(t.substitute(**kwargs))
		of.close()
		for f in extrafiles :
			shutil.copy(f, self.od)
		subprocess.check_call(("pdflatex", "-interaction", "nonstopmode", "doc.tex"), cwd=self.od, stdout=-1, stderr=-1)
	
	def __enter__(self) :
		return self.od+"/doc.pdf"
	
	def __exit__(self, *_) :
		shutil.rmtree(self.od)
	
if __name__ == "__main__" :
	t=TeX2PDF("labels/aufkleber.tex", ("labels/whnetz-logo-sw.pdf",), essid="H", psk="allo", adminpw="12", mac="34", price="12")
