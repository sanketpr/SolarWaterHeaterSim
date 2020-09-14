from unittest import TestCase, TestLoader
from SolarSimulation import Tank, SolarHeater, PumpingSystem
import unittest

class TankTest(TestCase):

	tank = Tank()
	
	def setUp(self):
		self.tank = Tank(capacity = 500, waterVol = 200, waterTemp = 20)


	def test_releaseWater(self):
		releaseWaterVol = 25
		expectedWaterVol = 175
		self.tank.releaseWaterVolume(25)

		error_msg = "Expected "+str(expectedWaterVol)+"L of water in tank after releasing "+str(releaseWaterVol)+"L of water"
		self.assertEqual(self.tank.waterVol, expectedWaterVol, error_msg)

	def test_addHotWater(self):
		self.tank.releaseWaterVolume(20) 
		additionalWaterVol = 10
		additionalWaterTemp = 50

		expectedWaterVol = 190
		expectedWaterTemp = 21.578
		self.tank.addWater(additionalWaterVol, additionalWaterTemp)

		error_msg_vol = "Expected volume of water does not match the actual volume of water in tank"
		self.assertEqual(self.tank.getWaterVol(), expectedWaterVol, error_msg_vol)

		error_msg_temp = "Expected total temperature of water does not match the actual temperature of water in tank"
		self.assertTrue(abs(self.tank.waterTemp - expectedWaterTemp) <= 0.01, error_msg_temp)


class SolarPanelTest(TestCase):

	heater = SolarHeater(numberOfPanels=2)

	def setUp(self):
		self.heater.setIncidentEnergy(300)

	def test_waterHeatingPerCycle(self):
		pumpedWaterVolume = 2
		pumpedWaterTemperature = 15
		expectedRaisedWaterTemp = 15.01

		raisedWaterTemp = self.heater.heatWater(pumpedWaterVolume, pumpedWaterTemperature)

		error_msg = "Expected raised water temperature doesn't match the actual obtained temperature"
		self.assertTrue(abs(expectedRaisedWaterTemp-raisedWaterTemp) <=0.01, error_msg)
		

def main():
	tankTestSuite = unittest.TestLoader().loadTestsFromTestCase(TankTest)
	unittest.TextTestRunner(verbosity=2).run(tankTestSuite)

	panelTestSuite = tankTestSuite = unittest.TestLoader().loadTestsFromTestCase(SolarPanelTest)
	unittest.TextTestRunner(verbosity=2).run(tankTestSuite)

if __name__ == "__main__":
	main()