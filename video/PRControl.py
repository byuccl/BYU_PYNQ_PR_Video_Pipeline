#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from pynq import MMIO
from pynq import PL

__author__ = "Graham Schelle"
__copyright__ = "Copyright 2016, Xilinx"
__email__ = "pynq_support@xilinx.com"





class PRControl(object):
    """This class controls the onboard RGB LEDs.

    Attributes
    ----------
    index : int
        The index of the RGB LED, from 4 (LD4) to 5 (LD5).
    _axiSwitch : MMIO
        Shared memory map for the RGBLED GPIO controller.
    _rgbleds_val : int
        Global value of the RGBLED GPIO pins.
        
    """
    _axiSwitch = None
    _PRSettings = None
    output_map = {'HDMI_IN':0,'VDMA':1,'MUX_1':2,'MUX_2':3,'L0':4,'M0':5,'M1':6,'M2':7,'S0':8,'S1':9,'S2':0xA,'S3':0xB,'S4':0xC,'S5':0XD,
       'B_1':0xE,'B_2':0xF,'NULL':0x80000000}
    address_map = {'HDMI_OUT':0x44,'VDMA':0x40,'MUX_A':0x48,'MUX_B':0x4C,'L0':0x50,'M0':0x54,'M1':0x58,'M2':0x5C,'S0':0x60,'S1':0x64,'S2':0x68,'S3':0x6C,'S4':0x70,'S5':0X74,
       'B':0x78}
    array_map = {'HDMI_OUT':1,'VDMA':0,'MUX_A':2,'MUX_B':3,'L0':4,'M0':5,'M1':6,'M2':7,'S0':8,'S1':9,'S2':0xA,'S3':0xB,'S4':0xc,'S5':0XD,
       'B':0xE}
    control_map = {'MUX' : 0,'L0':1,'M0':2,'M1':3,'M2':4,'S0':5,'S1':6,'S2':7,'S3':8,'S4':9,'S5':10}
    switch_values = [output_map["NULL"]]*15
    def __init__(self):
        """Create a new RGB LED object.
        
        Parameters
        ----------
        index : int
            Index of the RGBLED, from 4 (LD4) to 5 (LD5).
        
        """
        hdmi_in_enable = MMIO(0x41220000,256)
        hdmi_in_enable.write(0,0xFFFFFFFF)
        hdmi_in_enable.write(8,0xFFFFFFFF)
        if PRControl._axiSwitch is None:
            base_addr = 0x43C00000#add location
            PRControl._axiSwitch = MMIO(base_addr, 256)
        if PRControl._PRSettings is None:
            base_addr = 0x43c80000#add location
            PRControl._PRSettings = MMIO(base_addr, 256)
        PRControl.connect(self,"HDMI_IN","VDMA")
        PRControl.connect(self,"VDMA","HDMI_OUT")

    def connect(self, input_stream,output_stream):
        """Turn on a single RGB LED with a color value (see color constants).
        
        Parameters
        ----------
        color : int
           Color of RGB specified by a 3-bit RGB integer value.
        
        Returns
        -------
        None
        
        """
#         print (input_stream)
#         print (output_stream)
#         print (PRControl.output_map[input_stream])
#         print (PRControl.address_map[output_stream])
        for i in range(len(PRControl.switch_values)):
            if(PRControl.switch_values[i] == PRControl.output_map[input_stream]):
                #print(PRControl.switch_values[i])
                PRControl.switch_values[i] = 0x80000000
        PRControl.switch_values[PRControl.array_map[output_stream]] = PRControl.output_map[input_stream]
        PRControl._axiSwitch.write(0x40,PRControl.switch_values[0]) 
        PRControl._axiSwitch.write(0x44,PRControl.switch_values[1]) #0x40 is M0 0x0 is S0
        PRControl._axiSwitch.write(0x48,PRControl.switch_values[2]) #2
        PRControl._axiSwitch.write(0x4C,PRControl.switch_values[3]) #3
        PRControl._axiSwitch.write(0x50,PRControl.switch_values[4]) #4 /0
        PRControl._axiSwitch.write(0x54,PRControl.switch_values[5]) #5 /1
        PRControl._axiSwitch.write(0x58,PRControl.switch_values[6]) #6 /2
        PRControl._axiSwitch.write(0x5C,PRControl.switch_values[7]) #7 /3
        PRControl._axiSwitch.write(0x60,PRControl.switch_values[8]) #8 /4
        PRControl._axiSwitch.write(0x64,PRControl.switch_values[9]) #9 /5
        PRControl._axiSwitch.write(0x68,PRControl.switch_values[0xA]) #A /6
        PRControl._axiSwitch.write(0x6C,PRControl.switch_values[0xB]) #B /7
        PRControl._axiSwitch.write(0x70,PRControl.switch_values[0xC]) #C /8
        PRControl._axiSwitch.write(0x74,PRControl.switch_values[0xD]) #D /9
        PRControl._axiSwitch.write(0x78,PRControl.switch_values[0xE]) #E/F
        PRControl._axiSwitch.write(0x0,0x2)  #commit changes
#         print (format(PRControl._axiSwitch.read(0x40),'08X'))
#         print (format(PRControl._axiSwitch.read(0x44),'08X'))
#         print (format(PRControl._axiSwitch.read(0x48),'08X'))
#         print (format(PRControl._axiSwitch.read(0x4C),'08X'))
        
#         print (format(PRControl._axiSwitch.read(0x50),'08X'))
#         print (format(PRControl._axiSwitch.read(0x54),'08X'))
#         print (format(PRControl._axiSwitch.read(0x58),'08X'))
#         print (format(PRControl._axiSwitch.read(0x5C),'08X'))
        
        
#         print (format(PRControl._axiSwitch.read(0x60),'08X'))
#         print (format(PRControl._axiSwitch.read(0x64),'08X'))
#         print (format(PRControl._axiSwitch.read(0x68),'08X'))
#         print (format(PRControl._axiSwitch.read(0x6C),'08X'))
        
        
#         print (format(PRControl._axiSwitch.read(0x70),'08X'))
#         print (format(PRControl._axiSwitch.read(0x74),'08X'))
#         print (format(PRControl._axiSwitch.read(0x78),'08X'))
    def filter_cmd(self, filter,cmd,data):
        PRControl._PRSettings.write(0,PRControl.control_map[filter])
        PRControl._PRSettings.write(4,cmd)
        PRControl._PRSettings.write(8,data)

