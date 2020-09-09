import time

class SolarPanel:
	def __init__(self) :
		self.height = 0
		self.width = 0
		self.incidentBeam = 0

class HeatingSystem:
	def __init__(self):
		self.heatingCoil = HeatingCoil()
		self.isPumping = False

	def startPumping(self):
		return

	def stopPumping(self):
		return

class HeatingCoil:
	def __init__(self):
		self.temp = 0
		self.isInSteadyState = False

	# Amount of heat exchange per min
	def descipateHeate(self) -> int:
		return

	def heatup(self):
		return

class Tank:
	def __init__(self):
		self.height = 0
		self.width = 0
		self.depth = 0
		self.heatingCoil = HeatingCoil()
		self.waterTemp = 0

	def heatWater(self):
		while(self.heatingCoil.isInSteadyState):
			self.waterTemp += self.heatingCoil.descipateHeate(self.waterTemp)
			time.sleep(60)
		return

	def releaseHotWater(self, amount):
		return

def main():
