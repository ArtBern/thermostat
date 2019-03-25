from abc import ABC, abstractmethod

class BaseRelaySetter(ABC):

	def __init__(self, settings):
		print("This is the constructor method.")
		
	@abstractmethod
	def set(self, state):
		pass