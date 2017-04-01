"""
converter file Handler
In goes a file, out comes a string.
If no convertion is present for filetype:
	then return statement of filetype
"""
import textract
import tempfile
import os
import urllib2

class FileConverter:
    valid = False
    txt = ""
    def __init__(self, url):
	valid_types = ['doc','txt','docx','pdf','rtf','odt']
        filetype = url.split(".")[len(url.split(".")) - 1]
	if(filetype in valid_types):
		valid = True
		content = urllib2.urlopen(url)
		with tempfile.NamedTemporaryFile(delete=False, suffix="."+filetype) as temp:
			temp.write(content.read())
		temp.close()
		self.txt = textract.process(temp.name)
		os.remove(temp.name)
	else:
		self.txt = "error, non-valid format"
    	
#   def __del__(self):
