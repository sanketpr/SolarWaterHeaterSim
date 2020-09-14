from time import sleep
from enum import Enum
from pubsub import pub

class Water:

	SpecificHeat = 4.2	#J/Kg°C

	# TODO: Integrate density chart of water for obtaining precise density of water at specific temprature
	# def getDensity(atTempratuer: int) -> float
	Density = 999.1

class Panel:

	def __init__(self, height = 1, width = 1, efficiency = 0.18):
		self.height = height
		self.width = width
		self.efficiency = efficiency

	def tempObtainedFrom(self, solarEnergy: int, mass: float, temprature: float) -> float:
		# Energy per meter sqr times the effeciency of the panel
		Q = solarEnergy * self.height * self.width * self.efficiency
		return Panel.heatEnergy(Q, mass, Water.SpecificHeat, temprature)

	# Calculating increased temprature using Fouriers law of Thermal Conduction [Q = mc(dT)]
	def heatEnergy(energy: float, mass: float, specificHeat: float, temprature) -> float:
		return (energy/(mass * specificHeat)) + temprature

class SolarHeater:

	MAX_HEAT = 60
	panels = []			# List of Solar Panel

	"""
		args:
		numberOfPanels: Define the number of panels required
		customPanels: Any number of custom panels if wanted, remaning number of panels will be created with default spec
	"""
	def __init__(self, numberOfPanels: int, customSpec: tuple() = ()) :
		self.buildSolarPanels(numberOfPanels, customSpec)
		self.incidentEnergy = -1

	def changePanelAt(index: int, height: int, width: int, efficiency: float):
		if(index >= len(self.panels)):
			return
		self.panels[index] = Panel(height=height, width=width, efficiency=efficiency)

	def buildSolarPanels(self, number, customSpec: tuple()) -> [Panel]:
		if(len(customSpec) != 0 and len(customSpec) != 3): 
			raise ValueError

		h, w, e = customSpec if (len(customSpec) == 3) else (1,1,0.18) 
		for _ in range(number):
			self.panels.append(Panel(height=h, width=w, efficiency=e))


	def getIncidentEnergy() -> int:
		if(self.incidentEnergy == 0):
			print("Incident energy on solar panel needs to be non-negative")
			raise ValueError

		return self.incidentEnergy

	def setIncidentEnergy(self, energy):
		self.incidentEnergy = energy

	def heatWater(self, volume: int, initialTemp: float) -> float:
		if(initialTemp >= self.MAX_HEAT): return self.MAX_HEAT		# Restricting heating over the max temp

		numberOfPanels = len(self.panels)
		volumePerPanel = volume/numberOfPanels
		massPerPanel = volumePerPanel * Water.Density

		tempObtainedFromPanels = []
		for panel in self.panels:
			tempObtainedFromPanels.append(panel.tempObtainedFrom(self.incidentEnergy, massPerPanel, initialTemp) * massPerPanel)

		# Weighted avegare of water tempratures obtained from all panels
		# Since weighted avg can be different for panels of different dimensions
		totalMass = volume * Water.Density
		finalTemp = sum(tempObtainedFromPanels)/(totalMass)

		return finalTemp


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

	def __init__(self, panel: SolarHeater, tank: Tank, pumpStatus: bool = False, pumpingRate: int = 1):
		self.panel = panel
		self.tank = tank
		self.pumpingRate = pumpingRate		# Liters per second

	def setPumpingRateLitersPerSec(self, rate):
		self.pumpingRate = rate

	def feedWaterToPanel(self) -> int:
		return self.panel.heatWater(self.pumpingRate, self.tank.waterTemp)	# Water out from the panel after heating

	def drawWaterFromTank(self):
		self.tank.releaseWaterVolume(self.pumpingRate)

	def feedWaterToTank(self, waterTemperature: int):
		self.tank.addWater(self.pumpingRate, waterTemperature)


class Controller:

	SOLAR_PANEL = 1
	TANK = 2
	PUMPING_SYSTEM = 3

	def __init__(self):
		self.panel = self.componentFactory(self.SOLAR_PANEL)
		self.tank = self.componentFactory(self.TANK)
		self.pump = self.componentFactory(self.PUMPING_SYSTEM, self.panel, self.tank)
		self.targetTemp = self.panel.MAX_HEAT

	def __simulateSystemForSeconds(self, time: int):
		timeTaken = 0
		for timeTaken in range(time):
			self.__performOneCycle()
			if(self.tank.waterTemp >= self.targetTemp):
				break
		return timeTaken

	def __performOneCycle(self):
		self.pump.drawWaterFromTank()
		newWaterTemp = self.pump.feedWaterToPanel()
		self.pump.feedWaterToTank(newWaterTemp)

	def simulateSystemForSeconds(self, second: int):
		timeTaken = self.__simulateSystemForSeconds(second)
		print("Temp of water after running the heater for ", timeTaken+1,"sec ",self.tank.waterTemp,"°C")

	def simulateSystemForHours(self, hours: int):
		timeTaken = self.__simulateSystemForSeconds(hours*3600)
		hoursTaken = timeTaken/3600
		print("Temp of water after running the heater for ", hours,"Hours ",self.tank.waterTemp,"°C")

	def componentFactory(self, type, *spec):
		if(type == self.SOLAR_PANEL):
			panel = SolarHeater(numberOfPanels = 2)
			panel.setIncidentEnergy(300)
			return panel
		elif(type == self.TANK):
			return Tank(capacity = 300, waterVol = 50, waterTemp = 15)
		elif(type == self.PUMPING_SYSTEM):
			pump = PumpingSystem(spec[0], spec[1])
			pump.setPumpingRateLitersPerSec(1)
			return pump
		else:
			raise Error("Please provide a valid option")

def main():
	controller = Controller()
	controller.simulateSystemForHours(1)
	
if __name__ == "__main__":
	main()
