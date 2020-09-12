from time import sleep
from pubsub import pub

class Water:
	SpecificHeat = 4.2

	# TODO: Integrate density chart of water for obtaining precise density of water at specific temprature
	# def getDensity(atTempratuer: int) -> float
	Density = 999.1		# Kg/m3

class SolarPanel:
	def __init__(self) :
		self.height = 0
		self.width = 0
		self.incidentBeam = 0

	def heatWater(self, volume: int, temprature: int):
		mass = Water.Density/volume
		return SolarPanel.heatTransfer(self.incidentBeam, mass, WATER.SpecificHeat, temprature)

	# Calculating increased temprature using Q = mc(dT)
	def heatTransfer(energy: int, mass: int, specificHeat: float, initialTemp: int) -> int:
		return (energy/(mass * specificHeat)) + initialTemp

class PumpingSystem:
	def __init__(self, panel: SolarPanel, pumpStatus: bool, pumpingRate: int):
		self.panel = panel
		self.isPumpActive = False
		self.pumpingRate = 0		# Kg per second

	def setIsPumpActive(self, status):
		self.isPumpActive = status

	def setPumpingRate(self, rate):
		self.pumpingRate = rate

	def pumpInPanel(self, temprature: int) -> int:
		self.panel.heatWater(self.pumpingRate, temprature)

class Tank:
	def __init__(self, capacity: int, waterCap: int):
		self.capacity = capacity	# Volume of tank in Liters
		self.waterCap = waterCap	# Volume of water in Liters
		self.waterTemp = 0			# Uniform water temprature in C

	# TODO: Should be able to fill the tank and overflow the extra water. Is it a valid approach?
	def addHotWater(self, volume: int, temprature: int):
		if(volume > self.capacity - self.waterCap):
			print("Cannot add more water than the overall tank capacity")
		self.mixWater(volume, temprature)

	def mixWater(self,volume, temprature):
		self.waterTemp = ((volume*temprature)+(self.waterTemp*self.waterCap))/(volume+self.waterCap)
		self.waterCap += volume

	def releaseWater(self, volume):
		if amount > self.waterCap:
			print("Sepcify volume not more than current volume of water\nCurrent Volume of Water:",self.waterCap," Kg/m3")
			return
		self.waterCap -= volume

class Controller:
	def __init__(self):


def main():
