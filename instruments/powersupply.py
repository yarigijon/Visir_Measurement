'''
Copyright (C) 2018  Pablo Baizan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

class PowerSupply(object):
    def __init__(self):
        self.InstrumentID = 12 # ID de la fuente de alimentacion
        self.Function = 0 #
        self.PowerSupplyEnable = 1
        self.Out6VEnable = 0
        self.Out6VVoltage = 0
        self.Out6VCurrentLimit = 0.5
        self.OutPlus25VEnable = 0
        self.OutPlus25VVoltage = 0
        self.OutPlus25VCurrentLimit = 0.5
        self.OutMinus25VEnable = 0
        self.OutMinus25VVoltage = 0
        self.OutMinus25VCurrentLimit = 0.5
        self.Out6VVoltageMeasurement = 0.0
        self.Out6VCurrentMeasurement = 0.0
        self.OutPlus25VVoltagetMeasurement = 0.0
        self.OutPlus25VCurrentMeasurement = 0.0
        self.OutMinus25VVoltageMeasurement = 0.0
        self.OutMinus25VCurrentMeasurement = 0.0
        self.OutPlus25VCurrentLimitFlat = 0
        self.OutMinus25VCurrentLimitFlat = 0
        self.Out6VCurrentLimitFlat = 0

    def SetFunction(self, Function):
        if Function == "setup":
            self.Function = 0
        elif Function == "fetch":
            self.Function = 1
        else:
            self.Function = -1

    def GetFunction(self):
        return self.Function

    def SetPowerSupplyEnable(self, PowerSupplyEnable):
        if PowerSupplyEnable == False:
            self.PowerSupplyEnable = 0
        elif PowerSupplyEnable == True:
            self.PowerSupplyEnable = 1
        else:
            self.PowerSupplyEnable = -1

    def SetOut6VEnable(self, Out6VEnable):
        if Out6VEnable == False:
            self.Out6VEnable = 0
        elif Out6VEnable == True:
            self.Out6VEnable = 1
        else:
            self.Out6VEnable = -1

    def GetOut6VEnable(self):
        return self.Out6VEnable

    def SetOut6VVoltage(self, Out6VVoltage):
        if float(Out6VVoltage) <= 6 or float(Out6VVoltage) >= 0:
            self.Out6VVoltage = float(Out6VVoltage)
        else:
            self.Out6VVoltage = -1

    def GetOut6VVoltage(self):
        return self.Out6VVoltage

    def SetOut6VCurrentLimit(self, Out6VCurrentLimit):
        if float(Out6VCurrentLimit) <= 1 or float(Out6VCurrentLimit) >= 0:
            self.Out6VCurrentLimit = float(Out6VCurrentLimit)
        else:
            self.Out6VCurrentLimit = -1

    def GetOut6VCurrentLimit(self):
        return self.Out6VCurrentLimit

    def SetOutPlus25VEnable(self, OutPlus25VEnable):
        if OutPlus25VEnable == False:
            self.OutPlus25VEnable = 0
        elif OutPlus25VEnable == True:
            self.OutPlus25VEnable = 1
        else:
            self.OutPlus25VEnable = -1

    def GetOutPlus25VEnable(self):
        return self.OutPlus25VEnable

    def SetOutPlus25VVoltage(self,OutPlus25VVoltage):
        if float(OutPlus25VVoltage) <= 25 or float(OutPlus25VVoltage) >= 0:
            self.OutPlus25VVoltage = float(OutPlus25VVoltage)
        else:
            self.OutPlus25VVoltage = -1

    def GetOutPlus25VVoltage(self):
        return self.OutPlus25VVoltage

    def SetOutPlus25VCurrentLimit(self, OutPlus25VCurrentLimit):
        if float(OutPlus25VCurrentLimit) <= 1 or float(OutPlus25VCurrentLimit) >= 0:
            self.OutPlus25VCurrentLimit = float(OutPlus25VCurrentLimit)
        else:
            self.OutPlus25VCurrentLimit = -1

    def GetOutPlus25VCurrentLimit(self):
        return self.OutPlus25VCurrentLimit

    def SetOutMinus25VEnable(self, OutMinus25VEnable):
        if OutMinus25VEnable == False:
            self.OutMinus25VEnable = 0
        elif OutMinus25VEnable == True:
            self.OutMinus25VEnable = 1
        else:
            self.OutMinus25VEnable = -1

    def GetOutMinus25VEnable(self):
        return self.OutMinus25VEnable

    def SetOutMinus25VVoltage(self,OutMinus25VVoltage):
        if float(OutMinus25VVoltage) <= 25 or float(OutMinus25VVoltage) >= 0:
            self.OutMinus25VVoltage = float(OutMinus25VVoltage)
        else:
            self.OutMinus25VVoltage = -1

    def GetOutMinus25VVoltage(self):
        return self.OutMinus25VVoltage

    def SetOutMinus25VCurrentLimit(self, OutMinus25VCurrentLimit):
        if float(OutMinus25VCurrentLimit) <= 1 or float(OutMinus25VCurrentLimit) >= 0:
            self.OutMinus25VCurrentLimit = float(OutMinus25VCurrentLimit)
        else:
            self.OutMinus25VCurrentLimit = -1

    def GetOutMinus25VCurrentLimit(self):
        return self.OutMinus25VCurrentLimit

    def CheckValues(self):
        return (self.Function != -1 and self.PowerSupplyEnable != -1 and self.Out6VEnable != -1 and self.Out6VVoltage != -1 and self.Out6VCurrentLimit != -1
                and self.OutPlus25VEnable != -1 and self.OutPlus25VVoltage != -1 and self.OutPlus25VCurrentLimit != -1 and
                self.OutMinus25VEnable != -1 and self.OutMinus25VVoltage != -1 and self.OutMinus25VCurrentLimit != 1)

    def GetEQCommand(self):
        if self.CheckValues():
            if self.Function == 0:
                Command = str(self.InstrumentID) + "\t0" + " " + str(self.PowerSupplyEnable) + " " + str(self.Out6VEnable) + " " + str(self.Out6VVoltage) + " "
                Command += str(self.Out6VCurrentLimit) + " " + str(self.OutPlus25VEnable) + " " + str(self.OutPlus25VVoltage) + " "
                Command += str(self.OutPlus25VCurrentLimit) + " " + str(self.OutMinus25VEnable) + " " + str(self.OutMinus25VVoltage) + " "
                Command += str(self.OutMinus25VCurrentLimit*-1) + "\n"
            else:
                Command = str(self.InstrumentID) + "\t1\n"
            return Command
        else:
            return -1

    def GetXMLResponse(self):
        if self.CheckValues():
            ScientificValue = '%.6E' %self.Out6VVoltage
            XML = '<dcpower>\n<dc_outputs>\n<dc_output channel="6V+">\n<dc_voltage value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.Out6VCurrentLimit
            XML += '<dc_current value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.Out6VVoltageMeasurement
            XML += '<dc_voltage_actual value="'+str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.Out6VCurrentMeasurement
            XML += '<dc_current_actual value="' + str(ScientificValue) +'"/>\n'
            XML += '<dc_output_enabled value="1"/>\n'
            XML += '<dc_output_limited value="' +str(self.Out6VCurrentLimitFlat) + '"/>\n' + '</dc_output>\n'
            ScientificValue = '%.6E' %self.OutPlus25VVoltage
            XML += '<dc_output channel="25V+">\n<dc_voltage value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.OutPlus25VCurrentLimit
            XML += '<dc_current value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.OutPlus25VVoltagetMeasurement
            XML += '<dc_voltage_actual value="'+str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.OutPlus25VCurrentMeasurement
            XML += '<dc_current_actual value="' + str(ScientificValue) +'"/>\n'
            XML += '<dc_output_enabled value="1"/>\n'
            XML += '<dc_output_limited value="' +str(self.OutPlus25VCurrentLimitFlat) + '"/>\n' + '</dc_output>\n'
            ScientificValue = '%.6E' %self.OutMinus25VVoltage
            XML += '<dc_output channel="25V-">\n<dc_voltage value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.OutMinus25VCurrentLimit
            XML += '<dc_current value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.OutMinus25VVoltageMeasurement
            XML += '<dc_voltage_actual value="'+str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' %self.OutMinus25VCurrentMeasurement
            XML += '<dc_current_actual value="' + str(ScientificValue) +'"/>\n'
            XML += '<dc_output_enabled value="1"/>\n'
            XML += '<dc_output_limited value="' +str(self.OutMinus25VCurrentLimitFlat) + '"/>\n' + '</dc_output>\n'
            XML += '</dc_outputs>\n</dcpower>\n'
            return XML
    
    def ProcessResponse(self, Response):
        if Response[0] == "0":
            return True
        elif Response[0] == "1":
            Init = Response.find("\t")
            End = Response.find(" ")
            self.Out6VVoltageMeasurement = float(Response[Init+1:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Out6VCurrentMeasurement = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.Out6VCurrentLimitFlat = int(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.OutPlus25VVoltagetMeasurement = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.OutPlus25VCurrentMeasurement = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.OutPlus25VCurrentLimitFlat = int(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.OutMinus25VVoltageMeasurement = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.OutMinus25VCurrentMeasurement = float(Response[:End])
            Response = Response[End+1:]
            End = Response.find(" ")
            self.OutMinus25VCurrentLimitFlat = int(Response[:End])
            return True
        else:
			return False