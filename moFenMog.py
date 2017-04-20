''' 
    ME - 405 - 05
    Pedro Mogollon & Tom Fenner
    April 12th, 2017
'''

import pyb

class MotorDriver:
    ''' This class implements a motordriver for the ME405 board.'''
    def __init__ (self):
        ''' Creates a motor driver by initializing GPIO pins and turning
        the motor off for safety. '''
        pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
        pinIN_1 = pyb.Pin(pyb.Pin.board.PB4, mode = pyb.Pin.AF_PP, af = 2)
        pinIN_2 = pyb.Pin(pyb.Pin.board.PB5, mode = pyb.Pin.AF_PP, af = 2)
        tim3 = pyb.Timer (3, freq = 20000)
        
        self.ch1 = tim3.channel (1, pyb.Timer.PWM, pin = pinIN_1)
        self.ch2 = tim3.channel (2, pyb.Timer.PWM, pin = pinIN_2)
        
        self.ch1.pulse_width_percent (0)
        self.ch2.pulse_width_percent (0)
        
        print ('Creating a motor driver')
    def set_duty_cycle (self, level):
        ''' This method sets the duty cycle to be sent to the motor to the
        given level. Positive values cause torque in one direction, 
        negative values in the opposite direction.
        @param level A signed interger holding the duty cycle of the
            voltage sent to the motor
        '''
        if level >= 100:
            self.ch1.pulse_width_percent (100)
            self.ch2.pulse_width_percent (0)           
        else:
            if 0 < level <100:
                self.ch1.pulse_width_percent (level)
                self.ch2.pulse_width_percent (0)
            #print ('Clockwise motion at ' + str(level) + ' duty cycle.')
            else:
                if -100 < level < 0:
                    self.ch1.pulse_width_percent (0)
                    self.ch2.pulse_width_percent (level*-1)
                #print ('Counterclockwise motion at ' + str(level*-1) + ' duty cycle.')
                else:
                    if level <= -100:
                        self.ch1.pulse_width_percent (0)
                        self.ch2.pulse_width_percent (100)
                    #else:
                        #self.ch1.pulse_width_percent (0)
                        #self.ch2.pulse_width_percent (0)
                #print ('Duty cycle set to 0.')
