import praw
import configparser
import os
import mistune
import re
import sys
import time
import struct
import urllib.parse, urllib.request

def construct_request_body(timestamp, itunes_identifier):
	hex = "61 6a 43 41 00 00 00 45 6d 73 74 63 00 00 00 04 55 94 17 a3 6d 6c 69 64 00 00 00 04 00 00 00 00 6d 75 73 72 00 00 00 04 00 00 00 81 6d 69 6b 64 00 00 00 01 02 6d 69 64 61 00 00 00 10 61 65 41 69 00 00 00 08 00 00 00 00 11 8c d9 2c 00" 

	body = bytearray.fromhex(hex);
	body[16:20] = struct.pack('>I', timestamp)
	body[-5:] = struct.pack('>I', itunes_identifier)
	return body

def add_song(itunes_identifier):
	data = construct_request_body(int(time.time()), itunes_identifier)
	
	headers = {
		"X-Apple-Store-Front" : "143455-6,32",
		"Client-iTunes-Sharing-Version" : "3.12",
		"Accept-Language" : "en-CA;q=1.0",
		"Client-Cloud-DAAP-Version" : "1.3/iTunes-12.6.0.100",
		"Accept-Encoding" : "gzip",
		"X-Apple-itre" : "0",
		"Client-DAAP-Version" : "3.13",
		"User-Agent" : "iTunes/12.6 (Macintosh; OS X 10.12.4) AppleWebKit/603.1.30.0.34",
		"Connection" : "keep-alive",
		"Content-Type" : "application/x-dmap-tagged",
		# Replace the values of the next three headers with the values you intercepted
		"X-Dsid" : Config.get('itunes', 'x-dsid'),
		#"Cookie" : "amia-175535499=ohuJv6iPtwWupnwoWh9tx+6MgqL7q9Es6d/tB7/l9eaf9VIHvWiWJe0YQSyUfm6qaYa/ITjMr2/ilzqzj6/how==; amp=5NFqKEsrbRqTFJ95phYHM7gJAtIv4cZCBiwOfFDRrKubXngEhYTrUHo8JNuiU3zuFup4PE1wbp6LkqvStqLNwvHZzrBlFOdFwrwUblx84l9L15OPSLdSIiz4r6YeShq9zhwrqlaRFw5ya6cVSXrACevtopZ8bxkN7uOShOizObGUGzvZCbOE7dnyb3LORJbrJC3N4uMllywkpZSMKt98lhg39vm1lLIKZGqJ9y580u8gIugTlvWh0wlBRy7N2cVc; mt-asn-175535499=5; mt-tkn-175535499=AmSdRPUFmlC7ksEj8wCozvhQ8vzxp8GUWZTBF8chzqoKeIyGF82iSqVcyydejfuFaOhAcEmlUCjDFowboUKxIGwq4/R2GlaE+PL6a3hLXzX3fDUOE76FNd3lrE0M10vuIr8Z1o89pw/6kzdznboDh6c/BJ4Rq3hX7k8DnMMqrvFyg4XWQ9nNjpbpfPEJrzH1vzZkirY=; mzf_in=172493; TrPod=5; itspod=17; mz_at_ssl-175535499=AwUAAAEBAAHXGAAAAABZC4HlYhg6IiUF3kppD+3JkF1wtdPEmTE=; xp_ci=3zGZrNmz681z51ezCw2z1O1TmLO8D; mz_at0-175535499=AwQAAAEBAAHWuQAAAABYtD47sLzBp8Zq+yyZRL/Vn2U7tYYz7Es=; X-Dsid=175535499; pldfltcid=c7177e05af2748deaba6440a6830eb35017", 
		"Cookie" : Config.get('itunes', 'cookie'),
		"X-Guid" : Config.get('itunes', 'x-guid'),
		"Content-Length" : "77"
	}

	request = urllib.request.Request("https://ld-5.itunes.apple.com/WebObjects/MZDaap.woa/daap/databases/1/cloud-add", data, headers)
	try:
		urllib.request.urlopen(request)
	except urllib.error.HTTPError as e:
		print(e.code)
		return
	except urllib.error.URLError as e:
		print('URLError')
	
    
def add_song_to_playlist(itunes_identifier):
	data = construct_request_body(int(time.time()), itunes_identifier)
	
	headers = {
		"X-Apple-Store-Front" : "143455-6,32",
		"Client-iTunes-Sharing-Version" : "3.12",
		"Accept-Language" : "en-CA;q=1.0",
		"Client-Cloud-DAAP-Version" : "1.3/iTunes-12.6.0.100",
		"Accept-Encoding" : "gzip",
		"X-Apple-itre" : "0",
		"Client-DAAP-Version" : "3.13",
		"User-Agent" : "iTunes/12.6 (Macintosh; OS X 10.12.4) AppleWebKit/603.1.30.0.34",
		"Connection" : "keep-alive",
		"Content-Type" : "application/x-dmap-tagged",
		# Replace the values of the next three headers with the values you intercepted
		"X-Dsid" : Config.get('itunes', 'x-dsid'),
		#"Cookie" : "amia-175535499=ohuJv6iPtwWupnwoWh9tx+6MgqL7q9Es6d/tB7/l9eaf9VIHvWiWJe0YQSyUfm6qaYa/ITjMr2/ilzqzj6/how==; amp=5NFqKEsrbRqTFJ95phYHM7gJAtIv4cZCBiwOfFDRrKubXngEhYTrUHo8JNuiU3zuFup4PE1wbp6LkqvStqLNwvHZzrBlFOdFwrwUblx84l9L15OPSLdSIiz4r6YeShq9zhwrqlaRFw5ya6cVSXrACevtopZ8bxkN7uOShOizObGUGzvZCbOE7dnyb3LORJbrJC3N4uMllywkpZSMKt98lhg39vm1lLIKZGqJ9y580u8gIugTlvWh0wlBRy7N2cVc; mt-asn-175535499=5; mt-tkn-175535499=AmSdRPUFmlC7ksEj8wCozvhQ8vzxp8GUWZTBF8chzqoKeIyGF82iSqVcyydejfuFaOhAcEmlUCjDFowboUKxIGwq4/R2GlaE+PL6a3hLXzX3fDUOE76FNd3lrE0M10vuIr8Z1o89pw/6kzdznboDh6c/BJ4Rq3hX7k8DnMMqrvFyg4XWQ9nNjpbpfPEJrzH1vzZkirY=; mzf_in=172493; TrPod=5; itspod=17; mz_at_ssl-175535499=AwUAAAEBAAHXGAAAAABZC4HlYhg6IiUF3kppD+3JkF1wtdPEmTE=; xp_ci=3zGZrNmz681z51ezCw2z1O1TmLO8D; mz_at0-175535499=AwQAAAEBAAHWuQAAAABYtD47sLzBp8Zq+yyZRL/Vn2U7tYYz7Es=; X-Dsid=175535499; pldfltcid=c7177e05af2748deaba6440a6830eb35017", 
		"Cookie" : Config.get('itunes', 'cookie'),
		"X-Guid" : Config.get('itunes', 'x-guid'),
		"Content-Length" : "77"
	}
		
	request = urllib.request.Request("https://ld-5.itunes.apple.com/WebObjects/MZDaap.woa/daap/databases/1/edit", data, headers)
	urllib.request.urlopen(request)
    
Config = configparser.ConfigParser()
Config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

user_agent = Config.get('reddit', 'agent')
my_client_id = Config.get('reddit', 'client_id')
my_client_secret = Config.get('reddit', 'secret')
user_to_grab = Config.get('reddit', 'username')

r = praw.Reddit(user_agent=user_agent,
        client_id=my_client_id,
        client_secret=my_client_secret)

user = r.redditor(user_to_grab)

for comment in user.comments.new():
	
	if comment.subreddit != "hiphopheads":
		continue
	
	
	#sys.exit()
	
	urls = re.findall('http[s]?://itunes.apple.com/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment.body)
	
	if len(urls) == 0:
		continue
	

		
	url = urls[0].rstrip('\)')
	itunes_ids = re.findall("i=(\d+)", url)

	if len(itunes_ids) == 0:
		continue
	itunes_id = int(itunes_ids[0])
	print("Adding: " + comment.link_title + " -- " + itunes_ids[0])

	add_song(itunes_id)
