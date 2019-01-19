from lib.subreddit_manager import *
from lib.runtime_manager import *

header = "Author: {0}\n\nTitle: {1}\n\n____\n\n"
footer = "\n\n____\n\n[Turn Me Off](https://www.reddit.com/message/compose/?to=get_in_here_you_fuck&subject=Remove&message={0}) | [Contact My Creator](https://www.reddit.com/message/compose/?to=The1RGood&subject=GIHYF%20Bot)"

class PostNotifications:
	def __init__(self, client, collection):
		self.client = client
		self.collection = collection

	def send_notifications(self):
		self.subreddit_string = self.build_subreddit_string()
		if(self.subreddit_string == ""):
			return
		SubredditManager().fulfill_refresh()
		print(self.subreddit_string)
		for post in self.client.subreddit(self.subreddit_string).stream.submissions(skip_existing=True):
			users = self.collection.find_one({'subreddit': post.subreddit.display_name.lower()})['users'].keys()
			for user in users:
				print("---------------------------")
				print("Sending notification:\nUser:\t\t{0}\nSubreddit:\t{1}".format(user, post.subreddit.display_name))
				self.client.message(user, "A new post has been made in {0}".format(post.subreddit.display_name), header.format(post.author.name, post.title) + post.permalink + footer.format(post.subreddit.display_name.lower()))
				
				#print("---------------------------")
				#print("A new post has been made in {0}".format(post.subreddit.display_name))
				#print(post.permalink)
			if(SubredditManager().requires_refresh() or not RuntimeManager().is_running()):
				break

	def build_subreddit_string(self):
		return "+".join(map(lambda doc: doc['subreddit'], self.collection.find({})))
