class SubredditManager:
	class __SubredditManager:
		def __init__(self):
			self.needs_refresh = False

		def request_refresh(self):
			print("Refresh Requested")
			self.needs_refresh = True

		def fulfill_refresh(self):
			print("Refresh being fulfilled")
			self.needs_refresh = False

		def requires_refresh(self):
			return self.needs_refresh
	instance = None
	def __init__(self):
		if not SubredditManager.instance:
			SubredditManager.instance = SubredditManager.__SubredditManager()

	def request_refresh(self):
		self.instance.request_refresh()

	def fulfill_refresh(self):
		self.instance.fulfill_refresh()

	def requires_refresh(self):
		return self.instance.requires_refresh()