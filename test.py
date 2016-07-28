import sys
import time
import unittest

import OpenHAB    

class Daylight(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.12')

    def test_daylight_on(self):
        # Start conditions
        self.openhab.postUpdate('sSunrise', 'OFF')
        self.openhab.postUpdate('sDaylight', 'OFF')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sSunrise', 'ON')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('sDaylight')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

    def test_daylight_off(self):
        # Start conditions
        self.openhab.postUpdate('sSunset', 'OFF')
        self.openhab.postUpdate('sDaylight', 'ON')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sSunset', 'ON')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('sDaylight')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

class HouseMode(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.12')

    def test_home(self):
        # Start conditions
        self.openhab.postUpdate('sHome', 'OFF')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sHome', 'ON')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to HOME')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

    def test_away(self):
        # Start conditions
        self.openhab.postUpdate('sHome', 'ON')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sHome', 'OFF')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to AWAY')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

    def test_awake(self):
        # Start conditions
        self.openhab.postUpdate('sAwake', 'OFF')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sAwake', 'ON')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to AWAKE')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

    def test_sleep(self):
        # Start conditions
        self.openhab.postUpdate('sAwake', 'ON')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sAwake', 'OFF')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('Event')['state'], 'House mode changed to SLEEP')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

class Ligthing(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.12')

    def test_outdoor_on(self):
        # Start conditions
        self.openhab.postUpdate('sDaylight', 'ON')
        self.openhab.postUpdate('S01D006_sSwitch', 'OFF')
        self.openhab.postUpdate('S01D006_sMonitor', 'OFF')
        self.openhab.postUpdate('S01D006_nPower', '0') # No power draw
        self.openhab.postUpdate('S01D007_sSwitch', 'OFF')
        self.openhab.postUpdate('S01D007_sMonitor', 'OFF')
        self.openhab.postUpdate('S01D007_nPower', '0') # No power draw        
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sDaylight', 'OFF')
        self.openhab.postUpdate('S01D006_nPower', '40') # Normal power draw
        self.openhab.postUpdate('S01D007_nPower', '32') # Normal power draw
        time.sleep(60 + 5)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('S01D006_sSwitch')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D006_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sSwitch')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

    def test_outdoor_on_lowpower(self):
        # Start conditions
        self.openhab.postUpdate('sDaylight', 'ON')
        self.openhab.postUpdate('S01D006_sSwitch', 'OFF')
        self.openhab.postUpdate('S01D006_sMonitor', 'OFF')
        self.openhab.postUpdate('S01D006_nPower', '0') # No power draw
        self.openhab.postUpdate('S01D007_sSwitch', 'OFF')
        self.openhab.postUpdate('S01D007_sMonitor', 'OFF')
        self.openhab.postUpdate('S01D007_nPower', '0') # No power draw        
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sDaylight', 'OFF')
        self.openhab.postUpdate('S01D006_nPower', '40') # Normal power draw
        self.openhab.postUpdate('S01D007_nPower', '16') # Lower than normal power draw
        time.sleep(60 + 5)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('S01D006_sSwitch')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D006_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sSwitch')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('S01D007_sMonitor')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], 'Outdoor lights (south) draw less power than normal')

    def test_outdoor_off(self):
        # Start conditions
        self.openhab.postUpdate('sDaylight', 'OFF')
        self.openhab.postUpdate('S01D006_sSwitch', 'ON')
        self.openhab.postUpdate('S01D006_sMonitor', 'ON')
        self.openhab.postUpdate('S01D006_nPower', '40') # Normal power draw
        self.openhab.postUpdate('S01D007_sSwitch', 'ON')
        self.openhab.postUpdate('S01D007_sMonitor', 'ON')
        self.openhab.postUpdate('S01D007_nPower', '32') # Normal power draw        
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.sendCommand('sDaylight', 'ON')
        self.openhab.postUpdate('S01D006_nPower', '0') # No power draw
        self.openhab.postUpdate('S01D007_nPower', '0') # No power draw
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('S01D006_sSwitch')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('S01D006_sMonitor')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('S01D007_sSwitch')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('S01D007_sMonitor')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

class Presence(unittest.TestCase):

    def setUp(self):
        self.openhab = OpenHAB.OpenHAB('192.168.100.12')

    def test_wasp_in(self):
        # Start conditions
        self.openhab.postUpdate('cDoor', 'CLOSED')
        self.openhab.postUpdate('cMotion', 'CLOSED')
        self.openhab.postUpdate('sWasp', 'OFF')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.postUpdate('cMotion', 'OPEN')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('sWasp')['state'], 'ON')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')
        
    def test_wasp_out(self):
        # Start conditions
        self.openhab.postUpdate('cDoor', 'CLOSED')
        self.openhab.postUpdate('cMotion', 'CLOSED')
        self.openhab.postUpdate('sWasp', 'ON')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.postUpdate('cDoor', 'OPEN')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('sWasp')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

    def test_wasp_in_out(self):
        # Start conditions
        self.openhab.postUpdate('cDoor', 'OPEN')
        self.openhab.postUpdate('cMotion', 'CLOSED')
        self.openhab.postUpdate('sWasp', 'OFF')
        # Give the system time to stabilize
        time.sleep(1)
        self.openhab.postUpdate('Event', '-')
        self.openhab.postUpdate('Alarm', '-')
        # Trigger
        self.openhab.postUpdate('cMotion', 'OPEN')
        time.sleep(1)
        # Exit criteria
        self.assertEqual(self.openhab.getItem('sWasp')['state'], 'OFF')
        self.assertEqual(self.openhab.getItem('Alarm')['state'], '-')

if __name__ == '__main__':
    unittest.main()
    sys.exit()
