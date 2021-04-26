# oauth PRAW template by /u/The1RGood #
#==================================================Config stuff====================================================
import time
import praw, prawcore, prawdditions
import pymongo
from flask import Flask, request
from threading import Thread
import configparser
from lib.mail_handler import *
from lib.post_notifications import *
from lib.runtime_manager import *
import sys

Config = configparser.ConfigParser()
Config.read('service.cfg')

client = pymongo.MongoClient(Config.get('Mongo Info','conn_str'))
db = client[Config.get('Mongo Info','database')]
coll = db[Config.get('Mongo Info','collection')]
scope = "identity privatemessages read"

acc_name = Config.get('Reddit Access','username')
acc_pass = Config.get('Reddit Access','password')

#==================================================End Config======================================================
#==================================================OAUTH APPROVAL==================================================
app = Flask(__name__)

CLIENT_ID = Config.get('Reddit Access','cid')
CLIENT_SECRET = Config.get('Reddit Access','csec')

r = praw.Reddit(
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	user_agent='GIHYF Notification Client',
    username=acc_name,
	password=acc_pass)
#==================================================END OAUTH APPROVAL-=============================================

def main():
	print("Bot starting!")
	mh = MailHandler(r, coll)
	pn = PostNotifications(r, coll)

	mail_thread = Thread(target=mh.read_mail, args=())
	mail_thread.setDaemon(True)
	mail_thread.start()

	while(RuntimeManager().is_running()):
		try:
			pn.send_notifications()
		except KeyboardInterrupt:
			RuntimeManager().halt()
		except:
			print(sys.exc_info()[0])

if(__name__=='__main__'):
	main()
