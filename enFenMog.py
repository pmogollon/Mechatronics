# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 17:10:07 2017

@author: Pedro Mogollon, Thomas Fenner
"""

import pyb   

CB_tim = pyb.Timer(6)
tim8 = pyb.Timer(8, prescaler = 0, period = 65535)
pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.AF_OD, af = 3) # Channel A
pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.AF_OD, af = 3) # Channel B 
        
class EncoderReader:
    '''This class encapsulates the operation of the timer to read encoders.'''
    ## The constructor
    def __init__(self, CB_timer = CB_tim, timer_N = tim8, pinCh_A = pinC6, pinCh_B = pinC7):
        '''Creates objects for the pins, timers and channels.
        @param CB_timer The timer to call back the read function at a given frequency.
        @param timer_N  The timer used for the encoder, pertaining to channel 1 and 2.
        @param pinCh_A  The pin to which encoder channel A is connected to. 
        @param pinCh_B  The pin to which encoder channel A is connected to.'''      
        ## A variable containing the last encoder count
        self.last_cnt = 0
        ## The current encoder count
        self.cur_cnt = 0
        ## The instantaneous change in encoder count
        self.delta = 0
        ## The absolute position of the encoder
        self.position = 0    
        ## Encoder timer
        self.tim = timer_N
        ## Encoder Channel A
        self.ch1 = timer_N.channel (1, pyb.Timer.ENC_A, pin=pinCh_A)
        ## Encoder Channel B
        self.ch2 = timer_N.channel (2, pyb.Timer.ENC_B, pin=pinCh_B)
        ## Callback timer
        self.CB_timer = CB_timer
        self.CB_timer.init(freq=100)
        self.CB_timer.callback(self.read)
        
    def read(self, tim):
        '''This method calculates the current position of the encoder.'''
        self.last_cnt = self.cur_cnt
        self.cur_cnt = self.tim.counter()
        self.delta = (self.cur_cnt - self.last_cnt) & 0x0000FFFF
        if self.delta > 32767:
            self.delta -= 65535
        self.position += self.delta
        
    def get_position(self):
        '''This method returns the current position of the encoder.'''
        return self.position
        
    def get_delta(self):
        '''This method returns the current speed of the encoder.'''
        return self.delta
          
    def set_position(self, value):
        '''This method resets the encoder position to zero.
        @param value Variable used to calibrate the position to a user defined value.'''
        self.tim.counter(value)
        self.position = value
        self.last_cnt = value - self.delta
        self.cur_cnt = value
        print('The position of the encoder has been set to ' + str(value))
        
        
    
        
        