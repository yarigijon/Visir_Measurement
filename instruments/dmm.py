class DMM (object):
    def __init__(self):
        self.Id = 1
        self.Option = 0
        self.InstrumentID = 22 # ID del generador de funciones
        self.Function = 0 #
        self.Resolution = 0
        self.Range = -1 #Autorange
        self.Autozero = 0 #Autorange
        self.MeasurementValue = 0.0

    def SetOption(self, Option):
        if Option == "measure":
            self.Option = 0
        elif Option == "fetch":
            self.Option = 1
        else:
            self.Option = -1
    
    def GetOption(self):
        return self.Option

    def SetId(self, Id):
        self.Id = int(Id)

    def GetId(self):
        return self.Id

    def SetFunction(self, Function):
        if Function == "dc volts":
            self.Function = 0
        elif Function == "ac volts":
            self.Function = 1
        elif Function == "dc current":
            self.Function = 2
        elif Function == "ac current":
            self.Function = 3
        elif Function == "resistance":
            self.Function = 4
        else:
            self.Function = -1

    def GetFunction(self):
        return self.Function

    def SetResolution(self, Resolution):
        if Resolution == "3.5":
            self.Resolution = 0
        elif Resolution == "4.5":
            self.Resolution = 1
        elif Resolution == "5.5":
            self.Resolution = 2
        elif Resolution == "6.5":
            self.Resolution = 3
        else:
            self.Resolution = -1

    def GetResolution(self):
        return self.Resolution

    def SetRange(self, Range):
        if range == "-1":
            self.range = -1
        else:
            range == -1 #como la aplicacion web simula un fluke con autorange este siempre sera autorange
    
    def GetRange(self):
        return self.Range

    def SetAutoZero(self, Autozero):
        if Autozero == "-1":
            self.Autozero = -1
        elif Autozero == "0":
            self.Autozero = 0
        elif Autozero == "1":
            self.Autozero = 1
        elif Autozero == "2":
            self.Autozero = 2
        else:
            self.Autozero = -2 #Normalmente utilizo -1 pero en este caso el EQCom tiene implementado este valor

    def GetAutoZero(self):
        return self.Autozero

    def CheckValues(self):
        return (self.Option != -1 and self.Function != -1 and self.Resolution != -1 and self.Autozero != -2)

    def GetEQCommand(self):
        if self.CheckValues():
            if self.Option == 0:
                Command = str(self.InstrumentID) + "#" + str(self.Id)  + "\t0" + " " + str(self.Function) + " " + str(self.Resolution)
                Command += " " + str(self.Range) + " " + str(self.Autozero) + "\n"
            elif self.Option == 1:
                Command = str(self.InstrumentID) + "\t1\n"
            return Command
        else:
			return -1

    def ProcessResponse(self, ComandData, Id):
        self.SetId(Id)
        Init = ComandData.find("\t")
        End = ComandData.find(" ")
        Value = float(ComandData[Init+1:End])
        self.MeasurementValue = Value

    def GetXMLResponse(self):
        XML = '<multimeter id="' + str(self.Id) + '">\n<dmm_function value="' + self.GetFunctionStr() + '"/>\n'
        ScientificValue = '%.6E' %self.Range
        XML += '<dmm_resolution value="' + self.GetResolutionStr() + '"/>\n<dmm_range value="' + str(ScientificValue) + '"/>\n'
        ScientificValue = '%.6E' %self.MeasurementValue
        XML += '<dmm_result value="' + str(ScientificValue) + '"/>\n</multimeter>\n'
        return XML

    def GetFunctionStr(self):
        if self.Function == 0:
            return "dc volts"
        elif self.Function == 1:
            return "ac volts"
        elif self.Function == 2:
            return "dc current"
        elif self.Function == 3:
            return "ac current"
        elif self.Function == 4:
            return "resistance"

    def GetResolutionStr(self):
        if self.Resolution == 0:
            return "3.5"
        elif self.Resolution == 1:
            return "4.5"
        elif self.Resolution == 2:
            return "5.5"
        elif self.Resolution == 3:
            return "6.5"