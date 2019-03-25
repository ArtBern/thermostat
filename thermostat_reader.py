from abc import ABC, abstractmethod

class BaseReader(ABC):

	def __init__(self):
		print("This is the constructor method.")
		
	@abstractmethod
	def read(self):
		pass
		#return dict(temp=25,humi=30,co2=800)