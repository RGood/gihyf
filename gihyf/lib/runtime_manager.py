class RuntimeManager:
	class __RuntimeManager:
		def __init__(self):
			self.running = True

		def is_running(self):
			return self.running

		def halt(self):
			self.running = False

	instance = None
	def __init__(self):
		if not RuntimeManager.instance:
			RuntimeManager.instance = RuntimeManager.__RuntimeManager()
	def halt(self):
		self.instance.halt()

	def is_running(self):
		return self.instance.is_running()