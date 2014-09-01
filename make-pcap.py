#@auther:daijainjun
#use for make http request pcap
#Note:  python version must >= 2.7

#!/usr/bin/python2.7
import httplib
import urllib
import time
import socket
import string
import sys
import os

con = ""
body = ""

def ConstructBody():
	print "Http request Body,end by input submit"
	global body
	data = raw_input()
	while data != "submit":
		body += data[0:]
		data = raw_input()
	body += "\r\n"
	return 0

def ConstructHeader():
	print "input the method you what to use in http request"
	print "Like GET , POST etc"
	global con
	global body
	method = raw_input()
	print "input the uri(exclude params) you want to request"
	uri = raw_input()
	uri = urllib.quote(uri)
	print "any params?yes/no?"
	opt = raw_input()
	if opt == "yes":
		print "please input params one by one,fomate must like this: key=value"
		print "input submit to end params"
		params = {}
		one_param = raw_input()
		while one_param != "submit":
			key = one_param[:one_param.find('=')]
			value = one_param[one_param.find('=')+1:]
			params[key] = value
			one_param = raw_input()
		encoded_params = urllib.urlencode(params)
		uri = uri + '?'+ encoded_params
	con.putrequest(method,uri)
	print "input the headers and theirs values you need"
	print "when you input headers over,input \"submit\" to add them to http request"
	print "Example "
	print "Host: 192.168.1.1"
	print "Content-Type: text/html"
	print "submit"
	head = raw_input()
	while head != "submit":
		name = head[:head.find(":")]
		value = head[head.find(':')+1:]
		con.putheader(name,value)
		head = raw_input()
	ConstructBody()
	try:
	    con.endheaders(body)  #version >= python 2.7 
	except:
		print "endheaders error!"
	#con.send(body)

def ConstructHttpRequestFromFile():
	global con
	global body
	print "input file name :"
	filename = raw_input()
	fileHandle = open(filename,'r')
	cmdline = fileHandle.readline(1024)  #first line:  GET /uri HTTP/1.1
	method = cmdline[:cmdline.find(' ')]
	cmdline = cmdline[cmdline.find(' ')+1:]
	uri = cmdline[:cmdline.find(' ')]
	uri = urllib.quote(uri)
	pos = uri.find('?')
	if pos != -1:
		uri_left = uri[pos+1:]
		uri = uri[:pos+1]
		params = {}
		uri_left_use_len = 0
		while len(uri_left) > uri_left_use_len:
			name = uri_left[uri_left_use_len:uri_left.find('=')]
			uri_left_use_len += len(name) + 1
			value = uri_left[uri_left_use_len:uri_left.find('&')]
			uri_left_use_len += len(value) + 1
			params[name] = value
		params_encoded = urllib.urlencode(params)
		uri = uri + params_encoded
	con.putrequest(method,uri)
	entity = fileHandle.readline(1024)
	while entity != "\n":
		name = entity[:entity.find(':')]
		value = entity[entity.find(':')+1:len(entity)-1] #delete line end '\n'
		con.putheader(name,value)
		entity = fileHandle.readline(1024)
	body = fileHandle.read()
	fileHandle.close()
	try:
	    con.endheaders(body)
	except:
		print "endheaders error!"
	#con.send(body)

if __name__ == '__main__':
	print "input the host you want to request,exp:127.0.0.1"
	global con
	global body
	host = raw_input()
	try:
		con = httplib.HTTPConnection(host)
	except:
		print "Connection error!"
		sys.exit(1)
	print "input through the teminal or read from file"
	print "press 0 : through teminal"
	print "press 1 : from file"
	select = input()
	if select == 0:
	    ConstructHeader()
	elif select == 1:
		ConstructHttpRequestFromFile()
	else:
		print "Error press"
		sys.exit(1)
	try:
		resp = con.getresponse()
		print(resp.status,resp.reason)
	except:
		print "No server response you!"
		print "do you want continue? yes/no?"
	print "do you want send again,yes/no?"
	packet = 0
	if raw_input() == "yes":
		while packet <= 5:
			try:
				con = httplib.HTTPConnection(host)
			except:
				print "Connection Error!"
				continue
			#con.endheaders(body)
			#con.send(body)
			ConstructHeader()
			try:
				resp = con.getresponse()
			except:
				print "NO Server response you!"
			packet += 1
	con.close()
	print "Done Over!"
