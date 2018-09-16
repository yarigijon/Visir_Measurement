'''
Copyright (C) 2018  Pablo Baizan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import base64

class Oscilloscope(object):
    def __init__(self):
        self.InstrumentID = 21 # ID del oscilloscope
        self.Function = 0 #
        self.Autoscale = 0
        self.MinSampleRate = 2500
        self.SampleRate = 25000.00
        self.RefPosition = 50
        self.RecordLength = 500
        self.Channels = [Channel(), Channel()]
        self.TriggerReceived = "0"
        self.TriggerSource = 0
        self.TriggerSlope = 0
        self.TriggerCoupling = 1
        self.TriggerLevel = 0
        self.TriggerHoldoff = 0
        self.TriggerDelay = 0
        self.TriggerMode = 2 #Autolevel
        self.TriggerTimeout = 2
        self.TriggerLevelReceive = 0.0
        # Todo: las measurement se pueden meter todas en una lista
        self.Measurement1 = 0.0
        self.Measurement2 = 0.0
        self.Measurement3 = 0.0
        self.Measurement1Channel = 0 # Medida 1 con respecto al canal 1 
        self.Measurement1Selection = 4000 # Medida 1 de tipo None
        self.Measurement2Channel = 0 # Medida 2 con respecto al canal 1
        self.Measurement2Selection = 4000 # Medida 2 de tipo None
        self.Measurement3Channel = 0 # Medida 3 con respecto al canal 1
        self.Measurement3Selection = 4000 # Medida 3 de tipo None
        
    def SetFunction(self, Function):
        if Function == "setup":
            self.Function = 0
        elif Function == "fetch data":
            self.Function = 1
        elif Function == "fetch":
            self.Function = 1
        else:
            self.Function = -1

    def GetFunction(self):
        return self.Function

    def SetAutoscale(self, Autoscale):
        if Autoscale == "0":
            self.Autoscale = 0
        elif Autoscale == "1":
            self.Autoscale = 1
        else:
            self.Autoscale = -1

    def GetAutoscale(self):
        return self.Autoscale

    def SetSampleRate(self, SampleRate):
        self.SampleRate = float(SampleRate)
        if float(SampleRate) < 0.0000001:
            TimeRange = 0.0000001
        else:
            TimeRange = (1.0 / float(SampleRate))*10
        if TimeRange == 0.0:
            self.MinSampleRate = 10000.0
        elif TimeRange < 0.001:
            if TimeRange < 0.0000001:
                t = 1.0 / TimeRange
                r = int(t + 0.5)
                self.MinSampleRate = self.RecordLength * float(r)
            else:
                self.MinSampleRate = -1
        else:
            if TimeRange < 0.5:
                self.MinSampleRate = self.RecordLength / TimeRange
            else:
                self.MinSampleRate = -1
            
    def GetSampleRate(self):
        return self.MinSampleRate

    def SetRecordLength(self, RecordLength):
        if int(RecordLength) > 0 or int(RecordLength) < 20000:
            self.RecordLength = int(RecordLength)
        else:
            self.RecordLength = -1

    def GetRecordLength(self):
        return self.RecordLength

    def SetRefPosition(self, RefPosition):
        if float(RefPosition) > 0.0 or  float(RefPosition) < 100.0:
            self.RefPosition = float(RefPosition)
        else:
            self.RefPosition = -1

    def GetRefPosition(self):
        return self.RefPosition

    def SetTriggerSource(self, TriggerSource):
        if TriggerSource == "channel 1":
            self.TriggerSource = 0
        elif TriggerSource == "channel 2":
            self.TriggerSource = 1
        elif TriggerSource == "immediate":
            self.TriggerSource = 2
        elif  TriggerSource == "external trigger":
            self.TriggerSource = 3
        else:
            self.TriggerSource = -1

    def GetTriggerSource(self):
        return self.TriggerSource

    def GetTriggerSourceStr(self):
        if self.TriggerSource == 0:
            return "channel 1"
        elif self.TriggerSource == 1:
            return "channel 2"
        elif self.TriggerSource == 2:
            return "immediate"
        elif self.TriggerSource == 3:
            return "external trigger"

    def SetTriggerSlope(self, TriggerSlope):
        if TriggerSlope == "positive":
            self.TriggerSlope = 0
        elif TriggerSlope == "negative":
            self.TriggerSlope = 1
        else:
            self.TriggerSlope = -1

    def GetTriggerSlope(self):
        return self.TriggerSlope

    def GetTriggerSlopeStr(self):
        if self.TriggerSlope == 0:
            return "positive"
        elif self.TriggerSlope == 1:
            return "negative"

    def SetTriggerCoupling(self, TriggerCoupling):
        if TriggerCoupling == "ac":
            self.TriggerCoupling = 0
        elif TriggerCoupling == "dc":
            self.TriggerCoupling = 1
        else:
            self.TriggerCoupling = -1

    def GetTriggerCoupling(self):
        return self.TriggerCoupling

    def GetTriggerCouplingStr(self):
        if self.TriggerCoupling == 0:
            return "ac"
        elif self.TriggerCoupling == 1:
            return "dc"

    def SetTriggerLevel(self,TriggerLevel):
        if self.TriggerSource == 0:
            Level = float(TriggerLevel) - self.Channels[0].GetVerticalOffset()
            if Level > self.Channels[0].GetVerticalRange() / 2 or Level < self.Channels[0].GetVerticalRange() * -4:
                self.TriggerLevel = -1
            else:
                self.TriggerLevel = float(TriggerLevel)
        elif self.TriggerLevel == 1:
            Level = float(TriggerLevel) - self.Channels[1].GetVerticalOffset()
            if Level > self.Channels[1].GetVerticalRange() / 2 or Level < self.Channels[1].GetVerticalRange() * -4:
                self.TriggerLevel = -1
            else:
                self.TriggerLevel = float(TriggerLevel)
        else: # Si TriggerSource no es un canal aceptamos cualquier nivel, la web esta capada y solo permite seleccionar
        # como fuente de trigger los canales, pero se deja preparado.
            self.TriggerLevel = float(TriggerLevel)
    
    def GetTriggerLevel(self):
        return self.TriggerLevel

    def SetTriggerHoldoff(self, TriggerHoldoff):
        #no hay restricciones de tiempo, pero este valor puede ralentizar mucho el sistema
        self.TriggerHoldoff = float(TriggerHoldoff)

    def GetTriggerHoldoff(self):
        return self.TriggerHoldoff

    def SetTriggerDelay(self, TriggerDelay):
        #no hay restricciones de tiempo, pero este valor puede ralentizar mucho el sistema
        self.TriggerDelay = float(TriggerDelay)

    def GetTriggerDelay(self):
        return self.TriggerDelay

    def SetTriggerMode(self,TriggerMode):
        if TriggerMode == "normal":
            self.TriggerMode = 0
        elif TriggerMode == "auto":
            self.TriggerMode = 1
        elif TriggerMode == "autolevel":
            self.TriggerMode = 2
        else:
            self.TriggerMode = -1

    def GetTriggerMode(self):
        return self.TriggerMode

    def GetTriggerModeStr(self):
        if self.TriggerMode == 0:
            return "normal"
        elif self.TriggerMode == 1:
            return "auto"
        elif self.TriggerMode == 2:
            return "autolevel"

    def SetTriggerTimeout(self, TriggerTimeout):
        self.TriggerTimeout = float(TriggerTimeout)

    def GetTriggerTimeout(self):
        return self.TriggerTimeout

    def SetMeasurement1Channel(self, Channel):
        if Channel == "channel 1":
            self.Measurement1Channel = 0
        elif Channel == "channel 2":
            self.Measurement1Channel = 1
        else:
            self.Measurement1Channel = -1

    def GetMeasurement1Channel(self):
        return self.Measurement1Channel

    def GetMeasurement1ChannelStr(self):
        if self.Measurement1Channel == 0:
            return "channel 1"
        elif self.Measurement1Channel == 1:
            return "channel 2"

    def SetMeasurement2Channel(self, Channel):
        if Channel == "channel 1":
            self.Measurement2Channel = 0
        elif Channel == "channel 2":
            self.Measurement2Channel = 1
        else:
            self.Measurement2Channel = -1

    def GetMeasurement2Channel(self):
        return self.Measurement2Channel

    def GetMeasurement2ChannelStr(self):
        if self.Measurement1Channel == 0:
            return "channel 1"
        elif self.Measurement1Channel == 1:
            return "channel 2"

    def SetMeasurement3Channel(self, Channel):
        if Channel == "channel 1":
            self.Measurement3Channel = 0
        elif Channel == "channel 2":
            self.Measurement3Channel = 1
        else:
            self.Measurement3Channel = -1

    def GetMeasurement3Channel(self):
        return self.Measurement3Channel

    def GetMeasurement3ChannelStr(self):
        if self.Measurement1Channel == 0:
            return "channel 1"
        elif self.Measurement1Channel == 1:
            return "channel 2"

    def SetMeasurement1Selection(self, Value):
        if Value == "ac estimate":
            self.Measurement1Selection = 1012
        elif Value == "area":
            self.Measurement1Selection = 1003
        elif Value == "average frequency":
            self.Measurement1Selection = 1016
        elif Value == "average period":
            self.Measurement1Selection = 1015
        elif Value == "cycle area":
            self.Measurement1Selection = 1004
        elif Value == "dc estimate":
            self.Measurement1Selection = 1013
        elif Value == "fall time":
            self.Measurement1Selection = 1
        elif Value == "falling slew rate":
            self.Measurement1Selection = 1011
        elif Value == "ftt amplitude":
            self.Measurement1Selection = 1009
        elif Value == "ftt frequency":
            self.Measurement1Selection = 1008
        elif Value == "frequency":
            self.Measurement1Selection = 2
        elif Value == "integral":
            self.Measurement1Selection = 1005
        elif Value == "negative duty cycle":
            self.Measurement1Selection = 13
        elif Value == "negative width":
            self.Measurement1Selection = 11
        elif Value == "none":
            self.Measurement1Selection = 4000
        elif Value == "overshoot":
            self.Measurement1Selection = 18
        elif Value == "period":
            self.Measurement1Selection = 3
        elif Value == "phase delay":
            self.Measurement1Selection = 1018
        elif Value == "positive duty cycle":
            self.Measurement1Selection = 14
        elif Value == "positive width":
            self.Measurement1Selection = 12
        elif Value == "preshoot":
            self.Measurement1Selection = 19
        elif Value == "rise time":
            self.Measurement1Selection = 0
        elif Value == "rising slew rate":
            self.Measurement1Selection = 1010
        elif Value == "time delay":
            self.Measurement1Selection = 1014
        elif Value == "voltage amplitude":
            self.Measurement1Selection = 15
        elif Value == "voltage average":
            self.Measurement1Selection = 10
        elif Value == "voltage base":
            self.Measurement1Selection = 1006
        elif Value == "voltage base to top":
            self.Measurement1Selection = 1017
        elif Value == "voltage cycle average":
            self.Measurement1Selection = 17
        elif Value == "voltage cycle rms":
            self.Measurement1Selection = 16
        elif Value == "voltage high":
            self.Measurement1Selection = 8
        elif Value == "voltage low":
            self.Measurement1Selection = 9
        elif Value == "voltage max":
            self.Measurement1Selection = 6
        elif Value == "voltage min":
            self.Measurement1Selection = 7
        elif Value == "voltage peak to peak":
            self.Measurement1Selection = 5
        elif Value == "voltage rms":
            self.Measurement1Selection = 4
        elif Value == "voltage top":
            self.Measurement1Selection = 1007
        else:
            self.Measurement1Selection = -1
    
    def GetMeasurement1Selection(self):
        return self.Measurement1Selection

    def GetMeasurement1SelectionStr(self):
        if self.Measurement1Selection == 1012:
            return "ac estimate"
        elif self.Measurement1Selection == 1003: 
            return "area"  
        elif self.Measurement1Selection == 1016: 
            return "average frequency"
        elif self.Measurement1Selection == 1015: 
            return "average period"  
        elif self.Measurement1Selection == 1004: 
            return "cycle area"   
        elif self.Measurement1Selection == 1013:
            return "dc estimate" 
        elif self.Measurement1Selection == 1:
            return "fall time"  
        elif self.Measurement1Selection == 1011:
            return "falling slew rate"
        elif self.Measurement1Selection == 1009:
            return "ftt amplitude"
        elif self.Measurement1Selection == 1008:
            return "ftt frequency"
        elif self.Measurement1Selection == 2:
            return "frequency"
        elif self.Measurement1Selection == 1005:
            return "integral"
        elif self.Measurement1Selection == 13:
            return "negative duty cycle"
        elif self.Measurement1Selection == 11:
            return "negative width"
        elif self.Measurement1Selection == 4000: 
            return "none"
        elif self.Measurement1Selection == 18:
            return "overshoot" 
        elif self.Measurement1Selection == 3:
            return "period"   
        elif self.Measurement1Selection == 1018:
            return "phase delay"
        elif self.Measurement1Selection == 14:
            return "positive duty cycle"
        elif self.Measurement1Selection == 12:
            return "positive width"
        elif self.Measurement1Selection == 19:
            return "preshoot"
        elif self.Measurement1Selection == 0:
            return "rise time" 
        elif self.Measurement1Selection == 1010:
            return "rising slew rate"
        elif self.Measurement1Selection == 1014:
            return "time delay"
        elif self.Measurement1Selection == 15:
            return "voltage amplitude"
        elif self.Measurement1Selection == 10:
            return "voltage average"
        elif self.Measurement1Selection == 1006:
            return "voltage base"
        elif self.Measurement1Selection == 1017:
            return "voltage base to top"
        elif self.Measurement1Selection == 17:
            return "voltage cycle average"
        elif self.Measurement1Selection == 16:
            return"voltage cycle rms"
        elif self.Measurement1Selection == 8:
            return "voltage high"
        elif self.Measurement1Selection == 9:
            return "voltage low"
        elif self.Measurement1Selection == 6:
            return "voltage max"
        elif self.Measurement1Selection == 7:
            return "voltage min"
        elif self.Measurement1Selection == 5:
            return "voltage peak to peak"
        elif self.Measurement1Selection == 4:
            return "voltage rms"
        elif self.Measurement1Selection == 1007:
            return "voltage top"
            
    def SetMeasurement2Selection(self, Value):
        if Value == "ac estimate":
            self.Measurement2Selection = 1012
        elif Value == "area":
            self.Measurement2Selection = 1003
        elif Value == "average frequency":
            self.Measurement2Selection = 1016
        elif Value == "average period":
            self.Measurement2Selection = 1015
        elif Value == "cycle area":
            self.Measurement2Selection = 1004
        elif Value == "dc estimate":
            self.Measurement2Selection = 1013
        elif Value == "fall time":
            self.Measurement2Selection = 1
        elif Value == "falling slew rate":
            self.Measurement2Selection = 1011
        elif Value == "ftt amplitude":
            self.Measurement2Selection = 1009
        elif Value == "ftt frequency":
            self.Measurement2Selection = 1008
        elif Value == "frequency":
            self.Measurement2Selection = 2
        elif Value == "integral":
            self.Measurement2Selection = 1005
        elif Value == "negative duty cycle":
            self.Measurement2Selection = 13
        elif Value == "negative width":
            self.Measurement2Selection = 11
        elif Value == "none":
            self.Measurement2Selection = 4000
        elif Value == "overshoot":
            self.Measurement2Selection = 18
        elif Value == "period":
            self.Measurement2Selection = 3
        elif Value == "phase delay":
            self.Measurement2Selection = 1018
        elif Value == "positive duty cycle":
            self.Measurement2Selection = 14
        elif Value == "positive width":
            self.Measurement2Selection = 12
        elif Value == "preshoot":
            self.Measurement2Selection = 19
        elif Value == "rise time":
            self.Measurement2Selection = 0
        elif Value == "rising slew rate":
            self.Measurement2Selection = 1010
        elif Value == "time delay":
            self.Measurement2Selection = 1014
        elif Value == "voltage amplitude":
            self.Measurement2Selection = 15
        elif Value == "voltage average":
            self.Measurement2Selection = 10
        elif Value == "voltage base":
            self.Measurement2Selection = 1006
        elif Value == "voltage base to top":
            self.Measurement2Selection = 1017
        elif Value == "voltage cycle average":
            self.Measurement2Selection = 17
        elif Value == "voltage cycle rms":
            self.Measurement2Selection = 16
        elif Value == "voltage high":
            self.Measurement2Selection = 8
        elif Value == "voltage low":
            self.Measurement2Selection = 9
        elif Value == "voltage max":
            self.Measurement2Selection = 6
        elif Value == "voltage min":
            self.Measurement2Selection = 7
        elif Value == "voltage peak to peak":
            self.Measurement2Selection = 5
        elif Value == "voltage rms":
            self.Measurement2Selection = 4
        elif Value == "voltage top":
            self.Measurement2Selection = 1007
        else:
            self.Measurement2Selection = -1
    
    def GetMeasurement2Selection(self):
        return self.Measurement2Selection

    def GetMeasurement2SelectionStr(self):
        if self.Measurement1Selection == 1012:
            return "ac estimate"
        elif self.Measurement1Selection == 1003: 
            return "area"  
        elif self.Measurement1Selection == 1016: 
            return "average frequency"
        elif self.Measurement1Selection == 1015: 
            return "average period"  
        elif self.Measurement1Selection == 1004: 
            return "cycle area"   
        elif self.Measurement1Selection == 1013:
            return "dc estimate" 
        elif self.Measurement1Selection == 1:
            return "fall time"  
        elif self.Measurement1Selection == 1011:
            return "falling slew rate"
        elif self.Measurement1Selection == 1009:
            return "ftt amplitude"
        elif self.Measurement1Selection == 1008:
            return "ftt frequency"
        elif self.Measurement1Selection == 2:
            return "frequency"
        elif self.Measurement1Selection == 1005:
            return "integral"
        elif self.Measurement1Selection == 13:
            return "negative duty cycle"
        elif self.Measurement1Selection == 11:
            return "negative width"
        elif self.Measurement1Selection == 4000: 
            return "none"
        elif self.Measurement1Selection == 18:
            return "overshoot" 
        elif self.Measurement1Selection == 3:
            return "period"   
        elif self.Measurement1Selection == 1018:
            return "phase delay"
        elif self.Measurement1Selection == 14:
            return "positive duty cycle"
        elif self.Measurement1Selection == 12:
            return "positive width"
        elif self.Measurement1Selection == 19:
            return "preshoot"
        elif self.Measurement1Selection == 0:
            return "rise time" 
        elif self.Measurement1Selection == 1010:
            return "rising slew rate"
        elif self.Measurement1Selection == 1014:
            return "time delay"
        elif self.Measurement1Selection == 15:
            return "voltage amplitude"
        elif self.Measurement1Selection == 10:
            return "voltage average"
        elif self.Measurement1Selection == 1006:
            return "voltage base"
        elif self.Measurement1Selection == 1017:
            return "voltage base to top"
        elif self.Measurement1Selection == 17:
            return "voltage cycle average"
        elif self.Measurement1Selection == 16:
            return"voltage cycle rms"
        elif self.Measurement1Selection == 8:
            return "voltage high"
        elif self.Measurement1Selection == 9:
            return "voltage low"
        elif self.Measurement1Selection == 6:
            return "voltage max"
        elif self.Measurement1Selection == 7:
            return "voltage min"
        elif self.Measurement1Selection == 5:
            return "voltage peak to peak"
        elif self.Measurement1Selection == 4:
            return "voltage rms"
        elif self.Measurement1Selection == 1007:
            return "voltage top"

    def SetMeasurement3Selection(self, Value):
        if Value == "ac estimate":
            self.Measurement3Selection = 1012
        elif Value == "area":
            self.Measurement3Selection = 1003
        elif Value == "average frequency":
            self.Measurement3Selection = 1016
        elif Value == "average period":
            self.Measurement3Selection = 1015
        elif Value == "cycle area":
            self.Measurement3Selection = 1004
        elif Value == "dc estimate":
            self.Measurement3Selection = 1013
        elif Value == "fall time":
            self.Measurement3Selection = 1
        elif Value == "falling slew rate":
            self.Measurement3Selection = 1011
        elif Value == "ftt amplitude":
            self.Measurement3Selection = 1009
        elif Value == "ftt frequency":
            self.Measurement3Selection = 1008
        elif Value == "frequency":
            self.Measurement3Selection = 2
        elif Value == "integral":
            self.Measurement3Selection = 1005
        elif Value == "negative duty cycle":
            self.Measurement3Selection = 13
        elif Value == "negative width":
            self.Measurement3Selection = 11
        elif Value == "none":
            self.Measurement3Selection = 4000
        elif Value == "overshoot":
            self.Measurement3Selection = 18
        elif Value == "period":
            self.Measurement3Selection = 3
        elif Value == "phase delay":
            self.Measurement3Selection = 1018
        elif Value == "positive duty cycle":
            self.Measurement3Selection = 14
        elif Value == "positive width":
            self.Measurement3Selection = 12
        elif Value == "preshoot":
            self.Measurement3Selection = 19
        elif Value == "rise time":
            self.Measurement3Selection = 0
        elif Value == "rising slew rate":
            self.Measurement3Selection = 1010
        elif Value == "time delay":
            self.Measurement3Selection = 1014
        elif Value == "voltage amplitude":
            self.Measurement3Selection = 15
        elif Value == "voltage average":
            self.Measurement3Selection = 10
        elif Value == "voltage base":
            self.Measurement3Selection = 1006
        elif Value == "voltage base to top":
            self.Measurement3Selection = 1017
        elif Value == "voltage cycle average":
            self.Measurement3Selection = 17
        elif Value == "voltage cycle rms":
            self.Measurement3Selection = 16
        elif Value == "voltage high":
            self.Measurement3Selection = 8
        elif Value == "voltage low":
            self.Measurement3Selection = 9
        elif Value == "voltage max":
            self.Measurement3Selection = 6
        elif Value == "voltage min":
            self.Measurement3Selection = 7
        elif Value == "voltage peak to peak":
            self.Measurement3Selection = 5
        elif Value == "voltage rms":
            self.Measurement3Selection = 4
        elif Value == "voltage top":
            self.Measurement3Selection = 1007
        else:
            self.Measurement3Selection = -1
    
    def GetMeasurement3Selection(self):
        return self.Measurement3Selection

    def GetMeasurement3SelectionStr(self):
        if self.Measurement1Selection == 1012:
            return "ac estimate"
        elif self.Measurement1Selection == 1003: 
            return "area"  
        elif self.Measurement1Selection == 1016: 
            return "average frequency"
        elif self.Measurement1Selection == 1015: 
            return "average period"  
        elif self.Measurement1Selection == 1004: 
            return "cycle area"   
        elif self.Measurement1Selection == 1013:
            return "dc estimate" 
        elif self.Measurement1Selection == 1:
            return "fall time"  
        elif self.Measurement1Selection == 1011:
            return "falling slew rate"
        elif self.Measurement1Selection == 1009:
            return "ftt amplitude"
        elif self.Measurement1Selection == 1008:
            return "ftt frequency"
        elif self.Measurement1Selection == 2:
            return "frequency"
        elif self.Measurement1Selection == 1005:
            return "integral"
        elif self.Measurement1Selection == 13:
            return "negative duty cycle"
        elif self.Measurement1Selection == 11:
            return "negative width"
        elif self.Measurement1Selection == 4000: 
            return "none"
        elif self.Measurement1Selection == 18:
            return "overshoot" 
        elif self.Measurement1Selection == 3:
            return "period"   
        elif self.Measurement1Selection == 1018:
            return "phase delay"
        elif self.Measurement1Selection == 14:
            return "positive duty cycle"
        elif self.Measurement1Selection == 12:
            return "positive width"
        elif self.Measurement1Selection == 19:
            return "preshoot"
        elif self.Measurement1Selection == 0:
            return "rise time" 
        elif self.Measurement1Selection == 1010:
            return "rising slew rate"
        elif self.Measurement1Selection == 1014:
            return "time delay"
        elif self.Measurement1Selection == 15:
            return "voltage amplitude"
        elif self.Measurement1Selection == 10:
            return "voltage average"
        elif self.Measurement1Selection == 1006:
            return "voltage base"
        elif self.Measurement1Selection == 1017:
            return "voltage base to top"
        elif self.Measurement1Selection == 17:
            return "voltage cycle average"
        elif self.Measurement1Selection == 16:
            return"voltage cycle rms"
        elif self.Measurement1Selection == 8:
            return "voltage high"
        elif self.Measurement1Selection == 9:
            return "voltage low"
        elif self.Measurement1Selection == 6:
            return "voltage max"
        elif self.Measurement1Selection == 7:
            return "voltage min"
        elif self.Measurement1Selection == 5:
            return "voltage peak to peak"
        elif self.Measurement1Selection == 4:
            return "voltage rms"
        elif self.Measurement1Selection == 1007:
            return "voltage top"
    
    def CheckValues(self):
        return (self.Channels[0].CheckValues and self.Channels[1].CheckValues and self.Function != -1 and 
        self.Autoscale != -1 and self.MinSampleRate != -1 and self.RecordLength != -1 and self.RefPosition != -1
        and self.TriggerSource != -1 and self.TriggerSlope != -1 and self.TriggerCoupling != -1 and 
        self.TriggerLevel != -1 and self.TriggerMode != -1 and self.Measurement1Channel != -1 and 
        self.Measurement2Channel != -1 and self.Measurement3Channel != -1 and self.Measurement1Selection != -1 and
        self.Measurement2Selection != -1 and self.Measurement3Selection != -1)

    def GetEQCommand(self):
        if self.CheckValues():
            if self.Function == 0:
                Command = str(self.InstrumentID) + "\t0" + " " + str(self.Autoscale) + " " + str(self.MinSampleRate)
                Command +=  " " + str(self.RefPosition) + " " + str(self.RecordLength) + " " + str(self.Channels[0].EnableChannel)
                Command +=  " " + str(self.Channels[0].VerticalCoupling) + " " + str(self.Channels[0].VerticalRange)
                Command += " " + str(self.Channels[0].VerticalOffset) + " " + str(self.Channels[0].ProbeAttenuation)
                Command +=  " " + str(self.Channels[1].EnableChannel) + " " + str(self.Channels[1].VerticalCoupling)
                Command +=  " " + str(self.Channels[1].VerticalRange) + " " + str(self.Channels[1].VerticalOffset)
                Command += " " + str(self.Channels[1].ProbeAttenuation) + " " + str(self.TriggerSource) + " " + str(self.TriggerSlope)
                Command += " " + str(self.TriggerCoupling) + " " + str(self.TriggerLevel) + " " + str(self.TriggerHoldoff)
                Command += " " + str(self.TriggerDelay) + " " + str(self.TriggerMode) + " " + str(self.TriggerTimeout)
                Command += " " + str(self.Measurement1Channel) + " " + str(self.Measurement1Selection) + " " + str(self.Measurement2Channel)
                Command += " " + str(self.Measurement2Selection) + " " + str(self.Measurement3Channel) + " " + str(self.Measurement3Selection) + "\n"
            elif self.Function == 1:
                Command = str(self.InstrumentID) + "\t1\n"
            else:
                Command = str(self.InstrumentID) + "\t2\n"
            return Command
        else:
            return -1

    def ProcessResponse(self, Response):
        if Response[0] != "0":
            Init = Response.find("\t")
            End = Response.find(" ")
            self.Function = int(Response[Init+1:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.SampleRate = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.RecordLength = int(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            Response = Response[End+1:] # Aqui nos envia el numero de canales, sabemos que son 2 no lo guardamos
            End = Response.find(" ")
            Response = Response[End+1:] # Aqui nos indica que los datos siguientes son del canal 1
            End = Response.find(" ")
            self.Channels[0].ProbeAttenuation = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            #self.Channels[0].VerticalRange = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            #self.Channels[0].VerticalOffset = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Channels[0].Gain = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Channels[0].SetWaveForm(Response[:End], self.RecordLength)
            Response = Response[End+1:]
            End = Response.find(" ")
            Response = Response[End+1:] # Aqui nos indica que los datos siguientes son del canal 2
            End = Response.find(" ")
            self.Channels[1].ProbeAttenuation = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            #self.Channels[1].VerticalRange = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            #self.Channels[1].VerticalOffset = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Channels[1].Gain = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Channels[1].WaveForm = Response[:End]
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Measurement1 = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Measurement2 = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Measurement3 = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.TriggerReceived = Response[:End]
            Response = Response[End+1:]
            End = Response.find("\n")
            self.TriggerLevelReceive = Response[:End]

    def GetXMLResponse(self):
        ScientificValue = '%.6E' %self.SampleRate
        XML = '<oscilloscope>\n<osc_autoscale value="'+ str(self.Autoscale) +'"/>\n<horizontal>\n<horz_samplerate value="'+ str(ScientificValue) +'"/>\n'
        ScientificValue = '%.6E' %self.RefPosition
        XML += '<horz_refpos value="'+ str(ScientificValue) +'"/>\n<horz_recordlength value="' + str(self.RecordLength) +'"/>\n</horizontal>\n<channels>\n'
        ScientificValue = '%.6E' %self.Channels[0].VerticalRange
        XML += '<channel number="1">\n<chan_enabled value="'+ str(self.Channels[0].EnableChannel) +'"/>\n<chan_coupling value="'+ self.Channels[0].GetVerticalCouplingStr() +'"/>\n<chan_range value="'+ str(ScientificValue) +'"/>\n'
        ScientificValue = '%.6E' %self.Channels[0].VerticalOffset
        ScientificValue1 = '%.6E' %self.Channels[0].ProbeAttenuation
        ScientificValue2 = '%.6E' %self.Channels[0].Gain
        XML += '<chan_offset value="'+ str(ScientificValue) +'"/>\n<chan_attenuation value="'+ str(ScientificValue1) +'"/>\n<chan_gain value="'+ str(ScientificValue2) +'"/>\n'
        XML += '<chan_samples encoding="base64">\n'+ self.Channels[0].WaveForm +'\n</chan_samples>\n</channel>\n'
        Value = self.Channels[1].VerticalRange
        Value = (Value/10)*2
        ScientificValue = '%.6E' %Value
        XML += '<channel number="2">\n<chan_enabled value="'+ str(self.Channels[1].EnableChannel) +'"/>\n<chan_coupling value="'+ self.Channels[1].GetVerticalCouplingStr() +'"/>\n<chan_range value="'+ str(ScientificValue) +'"/>\n'
        ScientificValue = '%.6E' %self.Channels[1].VerticalOffset
        ScientificValue1 = '%.6E' %self.Channels[1].ProbeAttenuation
        ScientificValue2 = '%.6E' %self.Channels[1].Gain
        XML += '<chan_offset value="'+ str(ScientificValue) +'"/>\n<chan_attenuation value="'+ str(ScientificValue1) +'"/>\n<chan_gain value="'+ str(ScientificValue2) +'"/>\n'
        XML += '<chan_samples encoding="base64">\n'+ self.Channels[1].WaveForm +'\n</chan_samples>\n</channel>\n</channels>\n'
        ScientificValue = '%.6E' %self.TriggerLevel
        XML += '<trigger>\n<trig_source value="'+ self.GetTriggerSourceStr() +'"/>\n<trig_slope value="'+ self.GetTriggerSlopeStr() +'"/>\n<trig_coupling value="'+ self.GetTriggerCouplingStr() +'"/>\n<trig_level value="'+ str(ScientificValue) +'"/>\n'
        ScientificValue = '%.6E' %self.TriggerDelay
        XML += '<trig_mode value="'+ self.GetTriggerModeStr() +'"/>\n<trig_delay value="'+ str(ScientificValue) +'"/>\n<trig_received value="'+ str(self.TriggerLevelReceive) +'"/>\n</trigger>\n'
        ScientificValue = '%.6E' %self.Measurement1
        XML += '<measurements>\n<measurement number="1">\n<meas_channel value="'+ self.GetMeasurement1ChannelStr() +'"/>\n<meas_selection value="'+ self.GetMeasurement1SelectionStr() +'"/>\n<meas_result value="'+ str(ScientificValue) +'"/>\n'
        ScientificValue = '%.6E' %self.Measurement2
        XML += '<measurements>\n<measurement number="2">\n<meas_channel value="'+ self.GetMeasurement2ChannelStr() +'"/>\n<meas_selection value="'+ self.GetMeasurement2SelectionStr() +'"/>\n<meas_result value="'+ str(ScientificValue) +'"/>\n'
        ScientificValue = '%.6E' %self.Measurement3
        XML += '<measurements>\n<measurement number="3">\n<meas_channel value="'+ self.GetMeasurement3ChannelStr() +'"/>\n<meas_selection value="'+ self.GetMeasurement3SelectionStr() +'"/>\n<meas_result value="'+ str(ScientificValue) +'"/>\n'
        XML += '</measurement>\n</measurements>\n</oscilloscope>\n'
        return XML

class Channel(object):
    def __init__(self):
        self.EnableChannel = 1
        self.VerticalCoupling = 1
        self.VerticalRange = 8
        self.VerticalOffset = 0
        self.ProbeAttenuation = 1
        self.Gain = 0.0
        self.WaveForm = ""

    def SetEnableChannel(self, Value):
        if Value == "1":
            self.EnableChannel = 1
        elif Value == "0":
            self.EnableChannel = 0
        else:
            self.EnableChannel = -1

    def GetEnableChannel(self):
        return self.EnableChannel

    def SetVerticalCoupling(self, Value):
        if Value == "ac":
            self.VerticalCoupling = 0
        elif Value == "dc":
            self.VerticalCoupling = 1
        elif Value == "gnd":
            self.VerticalCoupling = 2
        else:
            self.VerticalCoupling = -1

    def GetVerticalCoupling(self):
        return self.VerticalCoupling

    def GetVerticalCouplingStr(self):
        if self.VerticalCoupling == 0:
            return "ac"
        elif self.VerticalCoupling == 1:
            return "dc"
        elif self.VerticalCoupling == 2:
            return "gnd"

    def SetVerticalRange(self, Value):
        if float(Value) > 0.00025 or float(Value) <= 5:
            self.VerticalRange = float(Value)*8
        else:
            self.VerticalRange = -1
    
    def GetVerticalRange(self):
        return self.VerticalRange

    def SetVerticalOffset(self, Value):
        #if Value > (-self.VerticalRange * 4.0) or Value < (self.VerticalRange * 4.0)):
        #En las primeras versiones de visir se ponia la resticcion "Vertical range must be between +/- half of vertical range"
        #pero en la ultima se ha comentado. Se deja aqui comentada para activar en caso de necesidad de compatibilidad 
        #con versiones antiguas.
        self.VerticalOffset = float(Value)

    def GetVerticalOffset(self):
        return self.VerticalOffset

    def SetProbeAttenuation(self, Value):
        #Limits: Any positive real number. Typical values are 1, 10 and 100
        if Value >= 0:
            self.ProbeAttenuation = float(Value)
        else:
            self.ProbeAttenuation = -1

    def GetProbeAttenuation(self):
        return self.ProbeAttenuation

    def CheckValues(self):
        return (self.EnableChannel != -1 and self.VerticalCoupling != -1 and self.VerticalRange != -1 and self.ProbeAttenuation != -1)

    def SetWaveForm(self, WaveForm, RecordLength):
        self.WaveForm = WaveForm
