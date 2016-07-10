import sys
import time
import unittest

import OpenHAB    

class General(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.15')
        self.openhab.postUpdate('Event', 'None')
        self.openhab.postUpdate('Alarm', 'None')

    def test_daylight_on(self):
        self.openhab.sendCommand('sSunrise', 'OFF')
        time.sleep(1)
        self.openhab.sendCommand('sSunrise', 'ON')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('sDaylight')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Event')['state'], 'Daylight started')

    def test_daylight_off(self):
        self.openhab.sendCommand('sSunset', 'OFF')
        time.sleep(1)
        self.openhab.sendCommand('sSunset', 'ON')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('sDaylight')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('Event')['state'], 'Daylight ended')

class HouseMode(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.15')
        self.openhab.postUpdate('Event', 'None')
        self.openhab.postUpdate('Alarm', 'None')

    def test_home(self):
        self.openhab.sendCommand('sHome', 'ON')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to HOME')

    def test_away(self):
        self.openhab.sendCommand('sHome', 'OFF')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to AWAY')

    def test_awake(self):
        self.openhab.sendCommand('sAwake', 'ON')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to AWAKE')

    def test_sleep(self):
        self.openhab.sendCommand('sAwake', 'OFF')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to SLEEP')

class Ligthing(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.15')
        self.openhab.postUpdate('Event', 'None')
        self.openhab.postUpdate('Alarm', 'None')

    def test_outdoor_on(self):
        self.openhab.sendCommand('sDaylight', 'OFF')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('S01D006_sSwitch')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sSwitch')['state'], 'ON')
        self.openhab.postUpdate('S01D006_nPower', '40') # Normal power draw
        self.openhab.postUpdate('S01D007_nPower', '32') # Normal power draw
        time.sleep(61)
        self.assertEqual(self.openhab.getItem('S01D006_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], 'None')

    def test_outdoor_on_lowpower(self):
        self.openhab.sendCommand('sDaylight', 'OFF')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('S01D006_sSwitch')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sSwitch')['state'], 'ON')
        self.openhab.postUpdate('S01D006_nPower', '40') # Normal power draw
        self.openhab.postUpdate('S01D007_nPower', '16') # Lower than normal power draw
        time.sleep(61)
        self.assertEqual(self.openhab.getItem('S01D006_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], 'Outdoor lights (south) draw less power than normal')

    def test_outdoor_off(self):
        self.openhab.sendCommand('sDaylight', 'ON')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('S01D006_sSwitch')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('S01D007_sSwitch')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('S01D006_sMonitor')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('S01D007_sMonitor')['state'], 'OFF')
        self.openhab.postUpdate('S01D006_nPower', '0') # No power draw
        self.openhab.postUpdate('S01D007_nPower', '0') # No power draw

class Presence(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.15')
        self.openhab.postUpdate('Event', 'None')
        self.openhab.postUpdate('Alarm', 'None')

    def test_wasp_in(self):
        # Initial values
        self.openhab.postUpdate('cDoor', 'CLOSED')
        self.openhab.postUpdate('cMotion', 'CLOSED')
        self.openhab.postUpdate('sWasp', 'OFF')
        time.sleep(1)
        # Trigger
        self.openhab.postUpdate('cMotion', 'OPEN')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('sWasp')['state'], 'ON')
        
    def test_wasp_out(self):
        # Initial values
        self.openhab.postUpdate('cDoor', 'CLOSED')
        self.openhab.postUpdate('cMotion', 'CLOSED')
        self.openhab.postUpdate('sWasp', 'ON')
        time.sleep(1)
        # Trigger
        self.openhab.postUpdate('cDoor', 'OPEN')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('sWasp')['state'], 'OFF')

    def test_wasp_in_out(self):
        # Initial values
        self.openhab.postUpdate('cDoor', 'OPEN')
        self.openhab.postUpdate('cMotion', 'CLOSED')
        self.openhab.postUpdate('sWasp', 'OFF')
        time.sleep(1)
        # Trigger
        self.openhab.postUpdate('cMotion', 'OPEN')
        time.sleep(1)
        self.assertEqual(self.openhab.getItem('sWasp')['state'], 'OFF')

if __name__ == '__main__':
    unittest.main()
    sys.exit()
