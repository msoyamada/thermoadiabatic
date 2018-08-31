#!/usr/bin/python

#   return 1/(1/self.T0 + (1/self.B) * np.log(R/self.R0)) - (273.15)
import mraa

relay_pin= mraa.Gpio(0)
relay_pin.dir(mraa.DIR_OUT)
relay_pin.write(1)

