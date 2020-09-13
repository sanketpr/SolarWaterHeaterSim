from time import sleep
from enum import Enum
from pubsub import pub

class Water:

	SpecificHeat = 4.2	#J/Kg°C

	# TODO: Integrate density chart of water for obtaining precise density of water at specific temprature
	# def getDensity(atTempratuer: int) -> float
	Density = 999.1		# Kg/m3


class SolarPanel:

	MAX_HEAT = 99
	ConversionEfficiency = 0.18		# A typical solar panel has efficiency between 17% to 19%

	def __init__(self, height: int = 1, width: int = 1) :
		self.height = 0
		self.width = 0
		self.incidentEnergy = -1

	def getIncidentEnergy() -> int:
		if(self.incidentEnergy == 0):
			print("Incident energy on solar panel needs to be non-negative")
			raise ValueError

		return self.incidentEnergy

	def setIncidentEnergy(self, energy):
		self.incidentEnergy = energy

	def heatWater(self, volume: int, temprature: int) -> int:
		if(temprature >= self.MAX_HEAT): return self.MAX_HEAT		# Restricting heating over the max temp
		
		mass = Water.Density/volume
		absorbedHeat = SolarPanel.heatTransfer(self.incidentEnergy*self.ConversionEfficiency, mass, Water.SpecificHeat, temprature)
		return absorbedHeat

	# Calculating increased temprature using Fouriers law of Thermal Conduction [Q = mc(dT)]
	def heatTransfer(energy: int, mass: float, specificHeat: float, initialTemp: int) -> float:
		return (energy/(mass * specificHeat)) + initialTemp

class Tank:

	def __init__(self, capacity: int = 500, waterVol: int = 100, waterTemp: float = 20):
		self.capacity = capacity	# Volume of tank in Liters
		self.waterVol = waterVol	# Volume of water in Liters
		self.waterTemp = waterTemp			# Uniform water temprature in C

	def setWaterVol(self, volume):
		self.waterVol = volume

	def getWaterVol(self) -> int:
		return self.waterVol

	# TODO: Should be able to fill the tank and overflow the extra water. Is it a valid approach?
	def addWater(self, volume: int, temprature: int):
		if(volume > self.capacity - self.waterVol):
			print("Cannot add more water than the overall tank capacity")
		self.mixWater(volume, temprature)

	def mixWater(self,volume, temprature):
		self.waterTemp = ((volume*temprature)+(self.waterTemp*self.waterVol))/(volume+self.waterVol)
		self.waterVol += volume

	def releaseWaterVolume(self, volume):
		if volume > self.waterVol:
			print("Sepcify volume not more than current volume of water\nCurrent Volume of Water:",self.waterCap," Kg/m3")
			return
		self.waterVol -= volume

class PumpingSystem:

	def __init__(self, panel: SolarPanel, tank: Tank, pumpStatus: bool = False, pumpingRate: int = 1):
		self.panel = panel
		self.tank = tank
		self.isPumpActive = pumpStatus
		self.pumpingRate = pumpingRate		# Liters per second

	def setIsPumpActive(self, status):
		self.isPumpActive = status

	def setPumpingRateLitersPerSec(self, rate):
		self.pumpingRate = rate

	def feedWaterToPanel(self) -> int:
		if(not self.isPumpActive): return
		return self.panel.heatWater(self.pumpingRate, self.tank.waterTemp)	# Water out from the panel after heating

	def drawWaterFromTank(self):
		if(not self.isPumpActive): return
		self.tank.releaseWaterVolume(self.pumpingRate)

	def feedWaterToTank(self, waterTemperature: int):
		if(not self.isPumpActive): return
		self.tank.addWater(self.pumpingRate, waterTemperature)

class Controller:

	SOLAR_PANEL = 1
	TANK = 2
	PUMPING_SYSTEM = 3

	def __init__(self):
		self.panel = self.componentFactory(self.SOLAR_PANEL)
		self.tank = self.componentFactory(self.TANK)
		self.pump = self.componentFactory(self.PUMPING_SYSTEM, self.panel, self.tank)

	def simulateSystemForSeconds(self, time: int):
		for _ in range(time):
			self.performOneCycle()

	def performOneCycle(self):
		self.pump.drawWaterFromTank()
		newWaterTemp = self.pump.feedWaterToPanel()
		self.pump.feedWaterToTank(newWaterTemp)

	def componentFactory(self, type, *spec):
		if(type == self.SOLAR_PANEL):
			panel = SolarPanel()
			panel.setIncidentEnergy(300)
			return panel
		elif(type == self.TANK):
			return Tank()
		elif(type == self.PUMPING_SYSTEM):
			pump = PumpingSystem(spec[0], spec[1])
			pump.setIsPumpActive(True)
			pump.setPumpingRateLitersPerSec(5)
			return pump
		else:
			raise Error("Please provide a valid option")

def main():
	controller = Controller()
	controller.simulateSystemForSeconds(7200)
	print("Temp of water after running the heater for 1hr:",controller.tank.waterTemp,"°C")
	
if __name__ == "__main__":
	main()
