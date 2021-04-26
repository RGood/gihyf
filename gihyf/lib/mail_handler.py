import yaml
from yaml import SafeLoader
from lib.subreddit_manager import *
from lib.runtime_manager import *
import re

class MailHandler:
	def __init__(self, client, collection):
		self.client = client
		self.collection = collection

	def read_mail(self):
		while(RuntimeManager().is_running()):
			try:
				for message in self.client.inbox.stream(skip_existing=True):
					if(message.subject.lower().strip()=='add'):
						to_find = self.parse_body(message.body)
						new_entries = self.subscribe(to_find, message.subreddit.display_name if message.subreddit else message.author.name)
						if(new_entries > 0):
							SubredditManager().request_refresh()
						message.reply("You will now receive notifications whenever a post is made in\n\n- {0}".format("\n- ".join(to_find)))
					elif(message.subject.lower().strip()=='remove'):
						to_find = self.parse_body(message.body)
						self.unsubscribe(to_find, message.subreddit.display_name if message.subreddit else message.author.name)
						message.reply("You will no longer receive notifications whenever a post is made in\n\n- {0}".format("\n- ".join(to_find)))
					else:
						message.reply("I only understand the subject lines `add` or `remove`")
						print('Received invalid action.')
			except:
				pass

	def subscribe(self, to_find, user):

		print("---------------------------")
		print("Action:\t\tSubscribe\nUser:\t\t{0}\nSubreddits:\t{1}".format(user, to_find))


		upserted = []

		for sub_name in filter(lambda name: self.valid_name(name), to_find):
			sub_name = self.trim_name(sub_name)
			update_res = self.collection.update({
				'subreddit': sub_name
			},{
				'$set': {
					'users.{0}'.format(user): 1
				}
			}, upsert=True)

			if('upserted' in update_res):
				upserted += [update_res['upserted']]

		print('New Entries:\t{0}'.format(upserted))
		return len(upserted)

	def unsubscribe(self, to_find, user):

		print("---------------------------")
		print("Action:\t\tUnsubscribe\nUser:\t\t{0}\nSubreddits:\t{1}".format(user, to_find))

		to_find = list(filter(lambda name: self.valid_name(name), map(lambda x: self.trim_name(x), to_find)))

		self.collection.update({
			'subreddit': {
				'$in': to_find
			}
		},{
			'$unset': { 'users.{0}'.format(user) : "" }
		}, upsert=True, multi=True)

	def parse_body(self, body):
		doc = yaml.load(body, Loader=SafeLoader)
		if(doc.__class__ == str or doc.__class__ == list):
			return self.convert_to_lower(doc)
		elif doc.__class__ == dict:
			return self.convert_to_lower(doc['subreddit'])
		elif doc.__class__ == int:
			return self.convert_to_lower(str(doc))
		else:
			print("Invalid body format")

	def convert_to_lower(self, entries):
		if(entries.__class__ == str):
			return list(map(lambda x: str(x).strip().lower(), entries.split(" ")))
		elif(entries.__class__ == list):
			return list(map(lambda x: str(x).strip().lower(), entries))
		else:
			print("Invalid entry type")

	def trim_name(self, name):
		if(name.startswith('/r/')):
			return name[3:]
		elif(name.startswith('r/')):
			return name[2:]
		else:
			return name

	def valid_name(self, name, search=re.compile(r'[^a-z0-9_]').search):
		return not bool(search(name))
