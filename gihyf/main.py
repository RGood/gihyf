# oauth PRAW template by /u/The1RGood #
#==================================================Config stuff====================================================
import time
import praw, prawcore
import pymongo
from flask import Flask, request
from threading import Thread
import configparser
from lib.mail_handler import *

Config = configparser.ConfigParser()
Config.read('service.cfg')

client = pymongo.MongoClient(Config.get('Mongo Info','conn_str'))
db = client[Config.get('Mongo Info','database')]
coll = db[Config.get('Mongo Info','collection')]
scope = "identity privatemessages read"

#==================================================End Config======================================================
#==================================================OAUTH APPROVAL==================================================
app = Flask(__name__)

CLIENT_ID = Config.get('Reddit Access','cid')
CLIENT_SECRET = Config.get('Reddit Access','csec')
REDIRECT_URI = Config.get('Reddit Access','callback')
REFRESH_TOKEN = ''

#Kill function, to stop server once auth is granted
def kill():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return "Shutting down..."

#Callback function to receive auth code
@app.route('/authorize_callback')
def authorized():
    global REFRESH_TOKEN
    code = request.args.get('code','')
    try:
        REFRESH_TOKEN = r.auth.authorize(code)
    except:
        traceback.print_exc(file=sys.stdout)
    text = 'Bot started on /u/' + r.user.me().name
    kill()
    return text
	
r = praw.Reddit(
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	redirect_uri=REDIRECT_URI,
	user_agent='Sub Mentions general usage client',
    api_request_delay=0)
print(r.auth.url(scope.split(' '),'UniqueKey'))
app.run(host="0.0.0.0",debug=False, port=65010)
#==================================================END OAUTH APPROVAL-=============================================

def main():
	mh = MailHandler(r, coll)
	mh.read_mail()

if(__name__=='__main__'):
	main()