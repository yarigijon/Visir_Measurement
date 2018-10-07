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

from decimal import Decimal


class FunctionGenerator(object):

    def __init__(self):
        self.InstrumentID = 11  # ID del generador de funciones
        self.Function = 0
        self.Waveform = 0  # default value sine
        self.Amplitude = 0
        self.Frequency = 0
        self.DCOffSet = 0
        self.StartPhase = 0
        self.TriggerMode = 1  # Trigger modo continuo
        self.TriggerSource = 0
        self.BurstCount = 0
        self.DutyCycleHigh = 0.5  # 50% del ciclo
        self.UserDefinedWaveform = 0

    def SetFunction(self, Function):
        if Function == "setup":
            self.Function = 0
        elif Function == "fetch":
            self.Function = 1
        else:
            self.Function = -1

    def GetFunction(self):
        return self.Function

    def SetWaveform(self, Waveform):
        if Waveform == "sine":
            self.Waveform = 0
        elif Waveform == "square":
            self.Waveform = 1
        elif Waveform == "triangle":
            self.Waveform = 2
        elif Waveform == "rampup":
            self.Waveform = 3
        elif Waveform == "rampdown":
            self.Waveform == 4
        elif Waveform == "DC":
            self.Waveform = 5
        elif Waveform == "noise":
            self.Waveform == 6
        elif Waveform == "arb":
            self.Waveform == 7
        else:
            self.Waveform = -1  # Error funcion no soportada

    def GetWaveform(self):
        return self.Waveform

    def SetAmplitude(self, Amplitude):
        # La aplicacion web envia la amplitud en Vp y el equipment server la
        # necesita en Vpp por lo que se multiplica por dos mas adelante
        ValueAmplitude = float(Amplitude)
        if ValueAmplitude >= 0 and ValueAmplitude <= 5:
            self.Amplitude = ValueAmplitude
        else:
            self.Amplitude = -1

    def GetAmplitude(self):
        # Como la aplicacion web envia la amplitud en Vp y no Vpp en los
        # archivos .max se utiliza la Vp
        return self.Amplitude

    def GetAmplitudeEQ(self):
        # La aplicacion web envia la amplitud en Vp y el equipment server la
        # necesita en Vpp por lo que se multiplica por dos
        return self.Amplitude * 2

    def SetFrequency(self, Frequency):
        ValueFrequency = float(Frequency)
        # senoidal y cuadrada pueden llegar a 20Mhz el resto unicamente a 1Mhz
        if self.Waveform == 0 or self.Waveform == 1:
            if ValueFrequency <= 20000000:
                self.Frequency = ValueFrequency
            else:
                self.Frequency = -1
        elif (self.Waveform == 2 or self.Waveform == 3 or
              self.Waveform == 4 or self.Waveform == 5 or
              self.Waveform == 6 or self.Waveform == 7):
            if ValueFrequency <= 1000000:
                self.Frequency = ValueFrequency
            else:
                self.Frequency = -1
        else:
            self.Frequency = -1

    def GetFrequency(self):
        return self.Frequency

    def SetDCOffSet(self, DCOffSet):
        ValueDCOffSet = float(DCOffSet)
        if (self.Amplitude * 2 + ValueDCOffSet) <= 10:
            if ValueDCOffSet >= -5 and ValueDCOffSet <= 5:
                self.DCOffSet = ValueDCOffSet
            else:
                # como -1 esta dentro del rango valido utilizamos -10 para
                # indicar error
                self.DCOffSet = -10
        else:
            # como -1 esta dentro del rango valido utilizamos -10 para indicar
            # error
            self.DCOffSet = -10

    def GetDCOffSet(self):
        return self.DCOffSet

    def SetStartPhase(self, StartPhase):
        ValueStartPhase = float(StartPhase)
        if ValueStartPhase >= -180 and ValueStartPhase <= 180:
            self.StartPhase = ValueStartPhase
        else:
            # como -1 esta dentro del rango vaido utilizamos -1000 para indicar
            # error
            self.StartPhase = -1000

    def GetStartPhase(self):
        return self.StartPhase

    def SetTriggerMode(self, TriggerMode):
        if TriggerMode == "single":
            self.TriggerMode = 0
        elif TriggerMode == "continous":
            self.TriggerMode = 1
        elif TriggerMode == "steped":
            self.TriggerMode = 2
        elif TriggerMode == "Burst":
            self.TriggerMode = 3
        else:
            self.TriggerMode = -1

    def GetTriggerMode(self):
        return self.TriggerMode

    def SetTriggerSource(self, TriggerSource):
        if TriggerSource == "immediate":
            self.TriggerSource = 0
        elif TriggerSource == "external":
            self.TriggerSource = 1
        else:
            self.TriggerSource = -1

    def GetTriggerSource(self):
        return self.TriggerSource

    def SetBurstCount(self, BurstCount):
        ValueBurstCount = int(BurstCount)
        if ValueBurstCount >= 0:
            self.BurstCount = ValueBurstCount
        else:
            self.BurstCount = -1

    def GetBurstCount(self):
        return self.BurstCount

    def SetDutyCycleHigh(self, DutyCycleHigh):
        ValueDutyClycleHigh = float(DutyCycleHigh)
        if ValueDutyClycleHigh >= 0 and ValueDutyClycleHigh <= 1:
            self.DutyCycleHigh = ValueDutyClycleHigh
        else:
            self.DutyCycleHigh = -1

    def GetDutyCycleHigh(self):
        return self.DutyCycleHigh

    def SetUserDefinedWaveform(self, UserDefinedWaveform):
        # de momento no implementamos esta funcion, 0 por defecto
        self.UserDefinedWaveform = 0

    def GetUserDefinedWaveform(self):
        return self.UserDefinedWaveform

    def CheckValues(self):
        return (
            self.Function != -
            1 and self.Waveform != -
            1 and self.Amplitude != -
            1 and self.Frequency != -
            1 and self.DCOffSet != -
            10 and self.StartPhase != -
            1000 and self.TriggerMode != -
            1 and self.TriggerSource != -
            1 and self.BurstCount != -
            1 and self.DutyCycleHigh != -
            1 and self.UserDefinedWaveform != -
            1)

    def GetEQCommand(self):
        if self.CheckValues():
            if self.Function == 0:
                Command = str(self.InstrumentID) + "\t0" + " " + \
                    str(self.Waveform) + " " + str(self.Amplitude) + \
                    " " + str(self.Frequency) + " "
                Command += str(self.DCOffSet) + " " + \
                    str(self.StartPhase) + " " + str(self.TriggerMode) + \
                    " " + str(self.TriggerSource) + " "
                Command += str(self.BurstCount) + " " + \
                    str(self.DutyCycleHigh) + " " + \
                    str(self.UserDefinedWaveform) + "\n"
            else:
                Command = str(self.InstrumentID) + "\t1\n"
            return Command
        else:
            return -1

    def CheckSetup(self, Response):
        return Response == str(self.InstrumentID) + "\t0"

    def SetupByFetch(self, Response):
        Tab = Response.find("\t")
        InstrumentID = int(Response[:Tab])
        Space = Response.find(" ")
        TempResponse = Response[Space + 1:]
        Function = int(Response[Tab:Space])
        Space = TempResponse.find(" ")
        Waveform = int(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        Amplitude = float(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        Frequency = float(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        DCOffSet = float(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        StartPhase = float(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        TriggerMode = int(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        TriggerSource = int(TempResponse[:Space])
        TempResponse = TempResponse[Space + 1:]
        Space = TempResponse.find(" ")
        DutyCycleHigh = float(TempResponse[:Space])
        if InstrumentID == self.InstrumentID and Function == 1:
            self.Function = Function
            self.Waveform = Waveform
            self.Amplitude = Amplitude
            self.Frequency = Frequency
            self.DCOffSet = DCOffSet
            self.StartPhase = StartPhase
            self.TriggerMode = TriggerMode
            self.TriggerSource = TriggerSource
            Self.DutyCycleHigh = DutyCycleHigh
            return True
        else:
            return False

    def GetXMLResponse(self):
        if self.CheckValues():
            Waveform = [
                "sine",
                "square",
                "triangle",
                "rampup",
                "rampdown",
                "DC",
                "noise",
                "arb"]
            TriggerMode = ["single", "continous", "steped", "Burst"]
            TriggerSource = ["immediate", "external"]
            XML = '<functiongenerator>\n'
            XML += '<fg_waveform value="' + Waveform[self.Waveform] + '"/>\n'
            ScientificValue = '%.6E' % self.Amplitude
            XML += '<fg_amplitude value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' % self.Frequency
            XML += '<fg_frequency value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' % self.DCOffSet
            XML += '<fg_offset value="' + str(ScientificValue) + '"/>\n'
            ScientificValue = '%.6E' % self.StartPhase
            XML += '<fg_startphase value="' + str(ScientificValue) + '"/>\n'
            XML += '<fg_triggermode value="' + \
                TriggerMode[self.TriggerMode] + '"/>\n'
            XML += '<fg_triggersource value="' + \
                TriggerSource[self.TriggerSource] + '"/>\n'
            XML += '<fg_burstcount value="' + str(self.BurstCount) + '"/>\n'
            ScientificValue = '%.6E' % self.StartPhase
            XML += '<fg_dutycycle value="' + str(ScientificValue) + '"/>\n'
            XML += '</functiongenerator>\n'
        else:
            XML = -1
        return XML

    def ProcessResponse(self, Response):
        if Response[0] == "0":
            return True
        else:
            return False
