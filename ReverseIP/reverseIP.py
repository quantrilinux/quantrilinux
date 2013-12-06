#!/usr/bin/python2

from sys import argv
import re
import httplib
import socket


def GenerateSearchString(input, count):
	return "/search?q=ip%3a"+input+"&count=50&first="+str(count)

def ParseResponse(data, listDomain):
	pattern = r'<h3><a href="http://(?:www\.)?([^/]+)'
	result = re.findall(pattern, data)
	for link in result:
		if link not in listDomain:
			listDomain.append(link)
			print "http://" + link

def ProcessUserInput(input):
	ip = socket.gethostbyname(input)
	pattern = r'^(?:(?:25[0-5]|2[0-4]\d|1?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|1?\d\d?)$'
	reObj = re.compile(pattern)
	result = reObj.match(ip)
	if result:
		return ip
	else:
		exit("Input '%s' is invalid" % input)

# Main
if __name__ == "__main__":
	if len(argv) != 2:
		exit("Usage: %s [IP|Hostname]" % argv[0])

	targetIP = ProcessUserInput(argv[1])
	print "Resolved IP: ", targetIP
	
	count = 0
	previousDataLength = 0
	listDomain = []

	while True:
		conn = httplib.HTTPConnection("www.bing.com", timeout=300)
		searchString = GenerateSearchString(targetIP, count)
		conn.request("GET", searchString)
		currentData = conn.getresponse().read()
		currentDataLength = len(currentData)
		ParseResponse(currentData, listDomain)


		if currentDataLength == previousDataLength:
		# If previous result and current result have the same length, it "maybe" have same content =>  finish reverse ip.
#			for i in range(0,len(listDomain)):
#				print "%d: %s" %(i+1, listDomain[i])
			
			print "There are %d site on server %s" %(len(listDomain), targetIP)
			break;
		else:
			previousDataLength = currentDataLength
			count += 50
			#print "Processing %d results" %(count)

		conn.close()