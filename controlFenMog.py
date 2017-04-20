# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:21:02 2017

@author: Pedro Mogollon, Thomas Fenner
"""
import pyb
import enFenMog
import moFenMog
import micropython

micropython.alloc_emergency_exception_buf(1000)

callback_tim = pyb.Timer(7)

encoder = enFenMog.EncoderReader()
motordriver = moFenMog.MotorDriver()

class controller:
    '''This class will perform closed loop proportional control for the encoder position.'''
    def __init__(self, K_p = 11, setpoint = 0, CB_timer = callback_tim):
        '''This constructs the variables used by the controller.'''
        ##Kp is the proportional gain of the controller.
        self.Kp = K_p
        ##setpoint is the reference position for the controller.
        self.setpoint = setpoint
        self.actualposition = 0
        self.error = 0
        self.actsignal = 0
        
        self.CB_timer = CB_timer
        self.CB_timer.init(freq=90)
        self.CB_timer.callback(self.control)
        
        
    def control(self, tim):
        '''This method runs the control algorithm in which the error is calculated and an actuation signal sent to the motor driver.'''
        self.actualposition = encoder.get_position()
        
        self.error = self.setpoint - self.actualposition
        #self.actsignal = self.Kp * self.error
        self.actsignal = self.Kp*self.error
        
        motordriver.set_duty_cycle(self.actsignal)