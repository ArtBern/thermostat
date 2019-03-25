from abc import ABC, abstractmethod

class BaseRelayReader(ABC):

	def __init__(self, settings):
		print("This is the constructor method.")
		
	@abstractmethod
	def read(self):
		pass