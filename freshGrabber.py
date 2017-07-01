import praw
import ConfigParser
import os
import mistune
import re
import sys
import time
import pymysql.cursors
import pymysql
import datetime
import struct
import itunes

Config = ConfigParser.ConfigParser()
Config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

user_agent = Config.get('reddit', 'agent')
my_client_id = Config.get('reddit', 'client_id')
my_client_secret = Config.get('reddit', 'secret')
user_to_grab = Config.get('reddit', 'username')
reddit_sources = Config.get('reddit', 'sources')

r = praw.Reddit(user_agent=user_agent,
        client_id=my_client_id,
        client_secret=my_client_secret)


connection = pymysql.connect(host = Config.get('db', 'host'),
							user = Config.get('db', 'user'),
							password = Config.get('db', 'password'),
							db = Config.get('db', 'name'),
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)

submissions = r.subreddit(reddit_sources).top(time_filter='day', limit=500)

for submission in submissions:

	#print(submission.subreddit_name)
	title = submission.title.upper()

	if "[FRESH]"  not in title.upper():
		continue

	
	title = title.replace('[FRESH]', '').strip().title()

	items = itunes.search(query=title)
	itunes_url = ""
	for item in items:
		#print '[' + item.type + ']', item.get_artist(), item.get_name(), item.get_url(), item.get_release_date()
		itunes_url = item.get_url()
		break

	#title = title.tite()

	print title + " -- " + submission.shortlink
	created = datetime.datetime.fromtimestamp(submission.created)

	try:
		with connection.cursor() as cursor:
			sql = "SELECT `id` FROM `posts` WHERE `id`=%s"
			cursor.execute(sql, submission.id)
			result = cursor.fetchone()
			count = cursor.rowcount

		if count > 0:
			with connection.cursor() as cursor:
				sql = "update posts set points=%s, itunes=%s where id=%s"
				cursor.execute(sql, (submission.ups, itunes_url, submission.id))

		if count == 0:
			with connection.cursor() as cursor:
				sql = "insert into posts (id, title, url, status, points, created, submitted, itunes) values (%s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (submission.id, title, submission.shortlink, "new", submission.ups, time.strftime('%Y-%m-%d %H:%M:%S'), created, itunes_url))

		connection.commit()
		#print str(submission.id) + " - " + str(submission.ups) + " - " + str(submission.title) + " - " + str(submission.url)
	finally:
		#connection.close()
		print "Imported " + submission.id