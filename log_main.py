import os
import sys
import re
import csv
#221.167.207.20 - tinyos [17/Jul/2016:08:07:21 +0900] "PROPFIND /webdav HTTP/1.1" 301 552 "-" "NetDrive 2.6.9"

#\D\d+\w+\d{4}[:]\d{2}[:]\d{2}[:]\d{2}
def parsing():
	#parsing
	#with open('contents.txt','r') as f:
	#	for line in f.readlines():
	#		log_exp = re.compile('[\d[.]\d[.]\d[.]\s\w\s\w\s[[]/d[/]\w[/]\d[:]\d[:]\d[:]\d\s]')
	#m = re.findall(r"(\d{0,3}[.]\d{0,3}[.]\d{0,3}[.]\d{0,3}) (\D) (\D+) (\D\d+[/]\w+[/]\d{4}[:]\d{2}[:]\d{2}[:]\d{2} \D\d{4}\D) (\D\w+) ((\D\w+)+) " ,'221.167.207.20 - tinyos [17/Jul/2016:08:07:21 +0900] "PROPFIND /webdav/webdav/media/movie/ HTTP/1.1" 301 552 "-" "NetDrive 2.6.9')
	#m = re.findall(r"(\d{0,3}[.]\d{0,3}[.]\d{0,3}[.]\d{0,3}) (\D) (\D+) (\D\d+[/]\w+[/]\d{4}[:]\d{2}[:]\d{2}[:]\d{2} \D\d{4}\D) (\D\w+) (\S*) (\S*) (\d* \d*) (\D\S*) (\D(\s?)\S*)" ,'221.167.207.20 - tinyos [17/Jul/2016:08:07:21 +0900] "PROPFIND /webdav/webdav/media/movie/ HTTP/1.1" 301 552 "-" "NetDrive 3.4.5"') #success
	
	'''
	clientIP
	clientInfo
	userID
	endTime
	method
	reqSource
	protocol
	statusCode
	size
	refererHeader
	userAgentHeader
	'''
	
	log_format = re.compile(r"(\d{0,3}[.]\d{0,3}[.]\d{0,3}[.]\d{0,3}) (\D) (\D+) (\D\d+[/]\w+[/]\d{4}[:]\d{2}[:]\d{2}[:]\d{2} \D\d{4}\D) (\D\w+) (\S*) (\S*) (\d* \d*) (\D\S*) (\D(\s?)\S*)")
	log_format_naming = re.compile(r"(?P<clientIP>\d{0,3}[.]\d{0,3}[.]\d{0,3}[.]\d{0,3}) (?P<clientInfo>\D*) (?P<userID>\D*) (?P<endTime>\D\d+[/]\w+[/]\d{4}[:]\d{2}[:]\d{2}[:]\d{2} \D\d{4}\D) (?P<method>\D\w+) (?P<reqSource>\S*) (?P<protocol>\S*) (?P<statusCode>\d*) (?P<size>\d*) (?P<refererHeader>\D\S*) (?P<userAgentHeader>\D(\s?)\S*)")
	
	
	with open('log_contents.txt','r') as f:
		parsing_file.write('clientIP, clientInfo, userID, endTime, method, reqSource, protocol, statusCode, size, refererHeader, userAgentHeader\n')
		for line in f.readlines():
			anal_log = log_format_naming.search(line)
			if anal_log:
				print anal_log.groups()
			else:
				print line
		parsing_file.close()
def main():
	os.system ("ls access.log* > log.txt")
	contents = open('log_contents.txt','w')	#for init

	with open('log.txt','rb')  as file:
		lines = file.readlines()	#lines -> list
		for a in lines:
			a = a[:-1]	#extract \n
			os.system("cp ~/anal_log/" +a+ " ~/anal_log/"+'temp.txt')
			with open('temp.txt','r') as f:
				contents = open('log_contents.txt','a')
				contents.write(f.read())
			#sys.stdout.writelines(lines[:])
			contents.close()
	os.system("rm temp.txt")
	parsing()

if __name__ == '__main__':
	main()
