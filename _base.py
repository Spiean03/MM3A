import serial
import time
import sys
import _defines as d

class NanoControl():
   # _initialx = 0
   # _initialy = 0

    def __init__(self, port=None):
        print "Now initializing"
        try:
            print "Trying hard"
            if port is None:
                self._serial = serial.Serial(d.DEFAULT_SERIAL, d.DEFAULT_BAUDRATE, parity = 'N', stopbits = 1, timeout=0.1)
                print self._serial.name
            else:
                print "tried"
                self._serial = serial.Serial(port = 'COM20', baudrate = 115200, parity = 'N', stopbits = 1, timeout = 0.1)
        except:
            self._serial.close()
            raise RuntimeError('Could not open serial connection')

        if self._serial is None:
            raise RuntimeError('Could not open serial connection')
            print "did not work"
        print('NanoControl initialized on port %s' %self._serial.name)
        self._serial.write('version\r')
        print('Firmware Version: ' + self._read_return_status())
        #self._initialx, self._initialy = self._counterread()
        self._serial.write('speed ?\r')
        self._serial.readline()

    def _read_return_status(self):
        #buf = self._serial.readline()
        buf = self._serial.read(512)
        buf = buf.split("\t")
        if buf[0] == 'e':
           raise RuntimeError('Return Status reported an error')
           return buf
        if len(buf) > 1:
            return buf[1]
        else:
            return buf[0]
            
    def _get_speed(self):
        self._serial.write('speed ?\r')
        speed = self._read_return_status()
        speed = speed.split(' ')
        self.speed0 = speed[0]
        self.speed1 = speed[1]
        self.speed2 = speed[2]
        self.speed3 = speed[3]
        #print(speed)
        #for index in range(0,5):
            #print('Speed%d: ' + speed[index]) %(index)
        
        return self._read_return_status()
        #print(speed)
        #return self._read_return_status()
        
    def _speed(self, speed):
        self._serial.write('speed '+ str(speed) + '\r')
        time.sleep(0.2)
        
        print speed
        self._serial.write('speed ?\r')
        speed = self._read_return_status()
        speed = speed.split(' ')
        self.speed0 = speed[0]
        self.speed1 = speed[1]
        self.speed2 = speed[2]
        self.speed3 = speed[3]
        print(speed)
        for index in range(0,5):
            print('Speed%d: ' + speed[index]) %(index)
        
        return self._read_return_status()
        #print(speed)
        #return self._read_return_status()
        
    def _coarse(self, channel, steps):
        if channel in ('A','B','C'):
            if (steps >= -65520) & (steps <= 65520):
                self._serial.write('coarse '+channel+' '+str(steps)+'\r')
                return self._read_return_status()
        raise RuntimeError('illegal parameters in _coarse(channel, steps)')

    def _get_coarse_counter(self):
        print('Test A')
        self._serial.write('coarse ?\r')
        print('Test B')
        #return self._serial.read(512)
        position=self._read_return_status()
        position=position.split(' ')
        self.position0 = position[0]
        self.position1 = position[1]
        self.position2 = position[2]
        self.position3 = position[3]
        for index in range(0,4):
            print('Position%d: ' + position[index]) %(index)
        
        #print('Coarse Counter: ' + self._read_return_status())
        return 

    def _coarse_reset(self):
        self._serial.write('coarsereset\r')
        return
    

    def _fine(self, channel, steps):
        if channel in ('A','B'):
            if (steps >= -2048) & (steps <= 2047):
                self._serial.write('fine '+channel+' '+str(int(steps))+'\r')
                return self._read_return_status()
        raise RuntimeError('illegal parameters in _fine(channel, steps)')

    def _get_fine_counter(self):
        """
        :return:
        """
        print('Test A')
        self._serial.write('fine ?\r')
        print("Test B")
        return self._read_return_status()
        position=self._read_return_status()
        position=position.split(' ')
        self.position0 = position[0]
        self.position1 = position[1]
        self.position2 = position[2]
        self.position3 = position[3]
        for index in range(0,4):
            print('Position%d: ' + position[index]) %(index)
        print("Test C")
        #print('Fine: '+ self._read_return_status())
        return 

    def _relax(self):
        """
        relax all channels (no voltage on the piezos)

        :return: return status
        """
        self._serial.write('relax\r')
        return self._read_return_status()

    def _moveabs(self, x=None, y=None, channel=None, pos=None):
        """
        move stage to absolute coordinates (only when stage has encoders !)

        :param x: move x-axis to the x position in nanometers
        :param y: move y-axis to the y position in nanometers
        :param channel: if you only want to move one channel/axis, define channel here (A=x,B=y)
        :param pos: position in nm the channel is moved to
        :return: return status
        """
        if (x is not None) & (y is not None):
            self._serial.write('moveabs '+str(x)+' '+str(y)+'\r')
        elif (channel in ('A','B')) & (pos is not None):
            self._serial.write('moveabs '+channel+' '+str(pos)+'\r')
        return self._read_return_status

    def _moverel(self, dx=None, dy=None):
        """
        move the stage by dx and dy [nm]

        :param dx: move x-axis by dx nanometers
        :param dy: move y-axis by dy nanometers
        :return: return status, values of the counters
        """
        x, y = self._counterread()
        self._moveabs(x=x+dx,y=y+dy)
        return self._read_return_status()

    def _counterread(self):
        """
        return position in nm
        """
        self._serial.write('counterread\r')
        buf = self._read_return_status()
        buf = buf.split(' ')
        return int(buf[0]), int(buf[1])

    def _counterreset(self):
        """
        resets all position counters

        :return: return status, values of the counters
        """
        self._serial.write('counterreset\r')
        return self._read_return_status()


    def home(self):
        """
        homes both axes of the stage

        :return: returns counter values after homing
        """
        self._moveabs(x=-200000,y=-200000)
        self._counterreset()
        self._moveabs(x=1000,y=1000)
        time.sleep(0.2)
        self._relax()
        time.sleep(0.2)
        return self._counterreset()



class NanoControl_Dummy(object):
    _x = 0
    _y = 0

    def __init__(self, port=None):
        pass

    def _read_return_status(self):
        time.sleep(0.1)
        return 'o\r'

    def _coarse(self, channel, steps):
        time.sleep(0.1)
        return 0

    def _get_coarse_counter(self, channel):
        time.sleep(0.1)
        return 0
        print('test')

    def _coarse_reset(self):
        time.sleep(0.1)
        return 0

    def _fine(self, channel, steps):
        time.sleep(0.1)
        return 0

    def _get_fine_counter(self):
        time.sleep(0.1)
        return 0

    def _relax(self):
        time.sleep(0.1)
        return 0

    def _moveabs(self, x=None, y=None, channel=None, pos=None):
        time.sleep(0.1)
        return 0

    def _moverel(self, dx=None, dy=None):
        time.sleep(0.1)
        return 0

    def _counterread(self):
        time.sleep(0.1)
        return (0,0)

    def _counterreset(self):
        time.sleep(0.1)
        return 0

    def home(self):
        time.sleep(0.1)
        return 0

# Example how to read the Steps in A B C D
#NanoControl()._counterread()
# Example how to read the Steps in A B C D
#NanoControl()._get_coarse_counter()
#Example how to send 100 Steps to channel A:
#time.sleep(5)
#NanoControl()._coarse('A', 100)
#time.sleep(5)
#NanoControl()._coarse('A', 100)

#n  = NanoControl()
#a._get_speed()
#print(a.speed0)

#print(NanoControl()._counterread())