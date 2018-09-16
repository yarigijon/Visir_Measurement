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

from xmlserver.xmlparser import XMLParser
from authenticator.authenticator import Authentication
from authenticator.client import ClientRegistry
from circuitsolver.maxfilesregistry import MaxFilesRegistry
from circuitsolver.listparser import ListParser
from circuitsolver.compdefreader import *
from circuitsolver.circuitsolver3 import CircuitSolver3
from instruments.circuit import Circuit
from instruments.powersupply import PowerSupply
from instruments.functiongenerator import FunctionGenerator
from instruments.oscilloscope import Oscilloscope
from instruments.dmm import DMM
from eqcom.eqcom import EQCom

class Transation (object):

    def __init__(self):
        self.VisirXMLParser = XMLParser()
        self.Authentication = Authentication()
        self.MaxFilesRegistry = MaxFilesRegistry()
        self.ComponentDefinitionRegistry = ComponentDefinitionRegistry()
        self.ListParser = ListParser(self.ComponentDefinitionRegistry.GetComponentDefinition())
        self.CircuitSolver = CircuitSolver3()
        self.EQCom = EQCom()
        self.FunctionGeneratorHandler = None
    
    def ProcessRequest(self, XMLRequest):
        self.VisirXMLParser.ParserRoot(XMLRequest)
        if self.VisirXMLParser.IsLogin:
            LoginValue = self.VisirXMLParser.ParserLogin()
            Cookie = LoginValue[1]
            if LoginValue[0] == 1:
                KeepLive = True
            else:
                KeepLive = False
            return self.CreateKeySession(Cookie, KeepLive)
        else:
            SessionKey = self.VisirXMLParser.ParserRequest()
            if not self.CheckSessionKey(SessionKey):
                print "\t\033[31mError:\033[0m Invalid SessionKey"
                return '<protocol version="1.3">\n<error>Invalid SessionKey\n</error>\n</protocol>'
            if self.VisirXMLParser.ParserCircuit() == []:
                return '<protocol version="1.3">\n<error>Empty circuit\n</error>\n</protocol>'
            CircuitParser = self.VisirXMLParser.ParserCircuit()[0]
            self.ListParser.Parse(CircuitParser)
            for MaxFile in self.MaxFilesRegistry.GetMaxFiles():
                Solved = self.CircuitSolver.Solve(self.ListParser.GetList(),MaxFile)
                if Solved:
                    CircuitHandler = Circuit()
                    Solution = self.CircuitSolver.GetSolution()
                    EnablePowerSupply = False
                    EnableFunctionGenerator = False
                    EnableOscilloscope = False
                    EnableDMM = False
                    EnableOut6V = False
                    EnableOutPlus25V = False
                    EnableOutMinus25V = False
                    Out6VVmax = None
                    Out6VImax = None
                    Outplus25VVmax = None
                    Outplus25VImax = None
                    OutMinus25VVmax = None
                    OutMinus25VImax = None
                    FuctionGeneratorVmax = None
                    for Item in Solution:
                        if Item.GetType() == "VDC+6V":
                            EnablePowerSupply = True
                            EnableOut6V = True
                            if Item.GetSpecial() != "":
                                Max = Item.GetSpecialToken("VMAX:")
                                if Max == "":
                                    Max = Item.GetSpecialToken("MAX:")
                                if Max != "":
                                    Out6VVmax = float(Max[:Max.find("\t")])
                                Max = Item.GetSpecialToken("IMAX:")
                                if Max != "":
                                    Out6VImax = float(Max)
                        elif Item.GetType() == "VDC+25V":
                            EnablePowerSupply = True
                            EnableOutPlus25V = True
                            if Item.GetSpecial() != "":
                                Max = Item.GetSpecialToken("VMAX:")
                                if Max == "":
                                    Max = Item.GetSpecialToken("MAX:")
                                if Max != "":
                                    Outplus25VVmax = float(Max[:Max.find("\t")])
                                Max = Item.GetSpecialToken("IMAX:")
                                if Max != "":
                                    Outplus25VImax = float(Max)
                        elif Item.GetType() == "VDC-25V":
                            EnablePowerSupply = True
                            EnableOutMinus25V = True
                            if Item.GetSpecial() != "":
                                Max = Item.GetSpecialToken("VMAX:")
                                if Max == "":
                                    Max = Item.GetSpecialToken("MAX:")
                                if Max != "":
                                    OutMinus25VVmax = float(Max[:Max.find("\t")])
                                Max = Item.GetSpecialToken("IMAX:")
                                if Max != "":
                                    OutMinus25VImax = float(Max)
                        elif Item.GetType() == "VFGENA":
                            EnableFunctionGenerator = True
                            if Item.GetSpecial() != "":
                                Max = Item.GetSpecialToken("VMAX:")
                                if Max == "":
                                    Max = Item.GetSpecialToken("MAX:")
                                if Max != "":
                                    FuctionGeneratorVmax = float(Max)
                        elif Item.GetType() == "DMM" or Item.GetType() == "IPROBE":
                            EnableDMM = True
                        elif Item.GetType() == "PROBE1" or Item.GetType() == "PROBE2":
                            EnableOscilloscope = True
                    Out = ""
                    Out = CircuitHandler.CircuitBuild(Solution)
                    Out += CircuitHandler.InstrumentBuild(Solution)
                    if EnablePowerSupply:
                        PowerSupplyRequest = self.VisirXMLParser.ParserDCPower()
                        PowerSupplyConfig = PowerSupplyRequest[0] # XML puede soportar mas de una fuente de alimentacion pero el EQ no
                        self.PowerSupplyHandler = PowerSupply()
                        self.PowerSupplyHandler.SetFunction("setup")
                        self.PowerSupplyHandler.SetPowerSupplyEnable(EnablePowerSupply)
                        self.PowerSupplyHandler.SetOut6VEnable(EnableOut6V)
                        self.PowerSupplyHandler.SetOut6VVoltage(PowerSupplyConfig["6V+_dc_voltage"])
                        self.PowerSupplyHandler.SetOut6VCurrentLimit(PowerSupplyConfig["6V+_dc_current"])
                        self.PowerSupplyHandler.SetOutPlus25VEnable(EnableOutPlus25V)
                        self.PowerSupplyHandler.SetOutPlus25VVoltage(PowerSupplyConfig["25V+_dc_voltage"])
                        self.PowerSupplyHandler.SetOutPlus25VCurrentLimit(PowerSupplyConfig["25V+_dc_current"])
                        self.PowerSupplyHandler.SetOutMinus25VEnable(EnableOutMinus25V)
                        self.PowerSupplyHandler.SetOutMinus25VVoltage(PowerSupplyConfig["25V-_dc_voltage"])
                        self.PowerSupplyHandler.SetOutMinus25VCurrentLimit(PowerSupplyConfig["25V-_dc_current"])
                        PowerSupplyEQ = self.PowerSupplyHandler.GetEQCommand()
                        if PowerSupplyEQ == -1:
                            return '<protocol version="1.3">\n<error>Power Supply config Error\n</error>\n</protocol>'
                        else:
                            if EnableOut6V:
                                if Out6VVmax != None:
                                    if self.PowerSupplyHandler.GetOut6VVoltage() > Out6VVmax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                                if Out6VImax != None:
                                    if self.PowerSupplyHandler.GetOut6VCurrentLimit() > Out6VImax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                            if EnableOutPlus25V:
                                if Outplus25VVmax != None:
                                    if self.PowerSupplyHandler.GetOutPlus25VVoltage() > Outplus25VVmax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                                if Outplus25VImax != None:
                                    if self.PowerSupplyHandler.GetOutPlus25VCurrentLimit() > Outplus25VImax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                            if EnableOutMinus25V:
                                if OutMinus25VVmax != None:
                                    if self.PowerSupplyHandler.GetOutMinus25VVoltage() < OutMinus25VVmax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                                if OutMinus25VImax != None:
                                    if self.PowerSupplyHandler.GetOutMinus25VCurrentLimit() > OutMinus25VImax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                            Out += PowerSupplyEQ
                    elif EnableFunctionGenerator:
                        FunctionGeneratorRequest = self.VisirXMLParser.ParserFunctionGenerator()
                        FunctionGeneratorConfig = FunctionGeneratorRequest[0] # XML soporta mas de un Function Generator pero EQ no
                        self.FunctionGeneratorHandler =  FunctionGenerator()
                        self.FunctionGeneratorHandler.SetFunction("setup")
                        self.FunctionGeneratorHandler.SetWaveform(FunctionGeneratorConfig["waveform"])
                        self.FunctionGeneratorHandler.SetAmplitude(FunctionGeneratorConfig["amplitude"]) # falta chequear que la aplitud no supera la del maxlist
                        self.FunctionGeneratorHandler.SetFrequency(FunctionGeneratorConfig["frequency"])
                        self.FunctionGeneratorHandler.SetDCOffSet(FunctionGeneratorConfig["offset"])
                        FunctionGeneratorEQ = self.FunctionGeneratorHandler.GetEQCommand()
                        if FunctionGeneratorEQ == -1:
                            return '<protocol version="1.3">\n<error>Function Generator config Error\n</error>\n</protocol>'
                        else:
                            if FuctionGeneratorVmax != None:
                                    if self.FunctionGeneratorHandler.GetAmplitude() > FuctionGeneratorVmax:
                                        return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
                            Out += FunctionGeneratorEQ
                    Out += "31\t0 25\n"
                    if EnableDMM:
                        DMMRequest = self.VisirXMLParser.ParserMultimeter()
                        for DMMConfig in DMMRequest:
                            self.DMMHandler = DMM()
                            self.DMMHandler.SetOption("measure")
                            self.DMMHandler.SetFunction(DMMConfig["function"])
                            self.DMMHandler.SetId(DMMConfig["id"])
                            self.DMMHandler.SetResolution(DMMConfig["resolution"])
                            self.DMMHandler.SetRange(DMMConfig["range"])
                            #self.DMMHandler.SetAutoZero(DMMConfig["autozero"]) # Se comenta porque measurement original lo ignora y pone a 0
                            DMMEQ = self.DMMHandler.GetEQCommand()
                            if DMMEQ == -1:
                                return '<protocol version="1.3">\n<error>Multimeter config Error\n</error>\n</protocol>'
                            else:
                                Out += DMMEQ
                    if EnableOscilloscope:
                        OscilloscopeRequest = self.VisirXMLParser.ParserOscilloscope()
                        OscilloscopeConfig = OscilloscopeRequest[0] # XML soporta mas de un Osciloscopio pero EQ no
                        self.OscilloscopeHandler = Oscilloscope()
                        self.OscilloscopeHandler.SetFunction("setup")
                        self.OscilloscopeHandler.SetAutoscale(OscilloscopeConfig["osc_autoscale"])
                        # RecordLength debe ir antes de samplerate por que se utiliza para los calculos del minsamplerate
                        self.OscilloscopeHandler.SetRecordLength(OscilloscopeConfig["horz_recordlength"])
                        self.OscilloscopeHandler.SetSampleRate(OscilloscopeConfig["samplerate"])
                        self.OscilloscopeHandler.SetRefPosition(OscilloscopeConfig["refpos"])
                        self.OscilloscopeHandler.Channels[0].SetEnableChannel(OscilloscopeConfig["chan1_enabled"])
                        self.OscilloscopeHandler.Channels[0].SetVerticalCoupling(OscilloscopeConfig["chan1_coupling"])
                        self.OscilloscopeHandler.Channels[0].SetVerticalRange(OscilloscopeConfig["chan1_range"])
                        self.OscilloscopeHandler.Channels[0].SetVerticalOffset(OscilloscopeConfig["chan1_offset"])
                        self.OscilloscopeHandler.Channels[0].SetProbeAttenuation(OscilloscopeConfig["chan1_attenuation"])
                        self.OscilloscopeHandler.Channels[1].SetEnableChannel(OscilloscopeConfig["chan2_enabled"])
                        self.OscilloscopeHandler.Channels[1].SetVerticalCoupling(OscilloscopeConfig["chan2_coupling"])
                        self.OscilloscopeHandler.Channels[1].SetVerticalRange(OscilloscopeConfig["chan2_range"])
                        self.OscilloscopeHandler.Channels[1].SetVerticalOffset(OscilloscopeConfig["chan2_offset"])
                        self.OscilloscopeHandler.Channels[1].SetProbeAttenuation(OscilloscopeConfig["chan2_attenuation"])
                        self.OscilloscopeHandler.SetTriggerSource(OscilloscopeConfig["trig_source"])
                        self.OscilloscopeHandler.SetTriggerSlope(OscilloscopeConfig["trig_slope"])
                        self.OscilloscopeHandler.SetTriggerCoupling(OscilloscopeConfig["trig_coupling"])
                        self.OscilloscopeHandler.SetTriggerLevel(OscilloscopeConfig["trig_level"])
                        # Aqui se deberia seleccionar el valor del triggerholdoff pero xml no lo soporta
                        #por lo que no se selecciona y toma el valor por defecto del contructor del objeto oscilloscope
                        self.OscilloscopeHandler.SetTriggerDelay(OscilloscopeConfig["trig_delay"])
                        self.OscilloscopeHandler.SetTriggerMode(OscilloscopeConfig["trig_mode"])
                        #self.OscilloscopeHandler.SetTriggerTimeout(OscilloscopeConfig["trig_timeout"]) # En measurement original ignora valor y siempre a 2
                        self.OscilloscopeHandler.SetMeasurement1Channel(OscilloscopeConfig["meas1_channel"])
                        self.OscilloscopeHandler.SetMeasurement1Selection(OscilloscopeConfig["meas1_selection"])
                        self.OscilloscopeHandler.SetMeasurement2Channel(OscilloscopeConfig["meas2_channel"])
                        self.OscilloscopeHandler.SetMeasurement2Selection(OscilloscopeConfig["meas2_selection"])
                        self.OscilloscopeHandler.SetMeasurement3Channel(OscilloscopeConfig["meas3_channel"])
                        self.OscilloscopeHandler.SetMeasurement3Selection(OscilloscopeConfig["meas3_selection"])
                        OscilloscopeEQ = self.OscilloscopeHandler.GetEQCommand()
                        if OscilloscopeEQ == -1:
                            return '<protocol version="1.3">\n<error>Oscilloscope config Error\n</error>\n</protocol>'
                        else:
                            Out += OscilloscopeEQ
                        self.OscilloscopeHandler.SetFunction("fetch data")
                        OscilloscopeEQ = self.OscilloscopeHandler.GetEQCommand()
                        if OscilloscopeEQ == -1:
                            return '<protocol version="1.3">\n<error>Oscilloscope config Error\n</error>\n</protocol>'
                        else:
                            Out += OscilloscopeEQ
                    if EnablePowerSupply:
                        Out += "12\t1\n"
                    Out = "data\n" + Out
                    Len = str(len(Out))
                    while len(Len)<6:
                        Len = "0"+ Len
                    Out = Len + "\n" + Out
                    self.EQCom.SendComand(SessionKey, Out)
                    Response = self.EQCom.GetResponse(SessionKey)
                    XML =  self.ProcessResponse(Response)
                    return XML
            return '<protocol version="1.3">\n<error>\nThe circuit cannot be constructed. Either it is unsafe or the current set of rules validating the circuit' + " can't find a suitable solution.</error>\n</protocol>"
    
    def CreateKeySession(self, Cookie, KeepLive):
        self.ClientList = ClientRegistry()
        for Client in self.ClientList.ClientList:
            Boolean, SessionKey = self.Authentication.Authenticate(Client, Cookie, KeepLive)
            if Boolean:
                XML = '<protocol version="1.3">\n<login sessionkey="' + SessionKey.GetKey() + '">\n</login>\n</protocol>\n'
                return XML
            else:
                XML = '<protocol version="1.3">\n<error>Cookie not found</error>\n</protocol>\n'
        return XML

    def ProcessResponse(self, Response):
        ObjectFinish = Response.find("\n")
        Length = Response[:ObjectFinish]
        ResponseLength = len(Response)
        if int(Length) == ResponseLength - 6 or int(Length) == ResponseLength - 7:
            Response = Response[ObjectFinish + 1:]
            ObjectFinish = Response.find("\n")
            Function = Response[:ObjectFinish]
            Response = Response[ObjectFinish + 1:]
            if Function == "error":
                print "\033[31mError:\033[0m " + Response
                return '<protocol version="1.3"><error>' + Response + '</error>\n</protocol>'
            Comands = False
            XML = '<protocol version="1.3">\n<response>\n'
            XMLResponse = {'DMM':None, 'FunctionGenerator':None, 'Oscilloscope':None, 'PowerSupply':None}
            Response += "\n"
            while not Comands:
                ObjectFinish = Response.find("\n")
                Comand = Response[:ObjectFinish+1]
                Response = Response[ObjectFinish + 1:]
                if ObjectFinish == -1:
                    Comands = True
                    Response = ""
                ObjectFinish = Comand.find(" ")
                InstrumentId = Comand[:ObjectFinish]
                ComandData = Comand[ObjectFinish + 1:]
                if InstrumentId == "21":
                    self.OscilloscopeHandler.ProcessResponse(ComandData)
                    XMLResponse['Oscilloscope'] = self.OscilloscopeHandler.GetXMLResponse()
                elif InstrumentId == "12":
                    self.PowerSupplyHandler.ProcessResponse(ComandData)
                    XMLResponse['PowerSupply']= self.PowerSupplyHandler.GetXMLResponse()
                elif InstrumentId == "11":
                    Boolean = self.FunctionGeneratorHandler.ProcessResponse(ComandData)
                    if Boolean:
                        XMLResponse['FunctionGenerator']= self.FunctionGeneratorHandler.GetXMLResponse()
                    else:
                        return '<protocol version="1.3">\n<error>'+ ComandData +'\n</error>\n</protocol>'
                elif InstrumentId[:2] == "22":
                    self.DMMHandler.ProcessResponse(ComandData, InstrumentId[3])
                    XMLResponse['DMM']= self.DMMHandler.GetXMLResponse()
            if XMLResponse['DMM'] != None:
                XML += XMLResponse['DMM']
            else:
                XML += '<multimeter id="1">\n<dmm_function value="ac volts"/>\n<dmm_resolution value="3.5"/>\n'
                XML += '<dmm_range value="-1.000000e+000"/>\n<dmm_result value="0.000000e+000"/>\n</multimeter>\n'
            if XMLResponse['FunctionGenerator']:
                XML += XMLResponse['FunctionGenerator']
            else:
                XML += '<functiongenerator>\n<fg_waveform value="sine"/>\n<fg_amplitude value="5.000000e-001"/>\n<fg_frequency value="1.000000e+003"/>\n'
                XML += '<fg_offset value="0.000000e+000"/>\n<fg_startphase value="0.000000e+000"/>\n<fg_triggermode value="continous"/>\n'
                XML += '<fg_triggersource value="immediate"/>\n<fg_burstcount value="0"/>\n<fg_dutycycle value="5.000000e-001"/>\n</functiongenerator>\n'
            if XMLResponse['Oscilloscope']:
                XML += XMLResponse['Oscilloscope']
            else:
                XML += '<oscilloscope>\n<osc_autoscale value="0"/>\n<horizontal>\n<horz_samplerate value="2.500000e+004"/>\n'
                XML += '<horz_refpos value="5.000000e+001"/>\n<horz_recordlength value="500"/>\n</horizontal>\n<channels>\n'
                XML += '<channel number="1">\n<chan_enabled value="1"/>\n<chan_coupling value="dc"/>\n<chan_range value="8.000000e+000"/>\n'
                XML += '<chan_offset value="0.000000e+000"/>\n<chan_attenuation value="1.000000e+000"/>\n<chan_gain value="0.000000e+000"/>\n'
                XML += '<chan_samples encoding="base64">\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\n</chan_samples>\n'
                XML += '</channel>\n<channel number="2">\n<chan_enabled value="1"/>\n<chan_coupling value="dc"/>\n<chan_range value="8.000000e+000"/>\n'
                XML += '<chan_offset value="0.000000e+000"/>\n<chan_attenuation value="1.000000e+000"/>\n<chan_gain value="0.000000e+000"/>\n<chan_samples encoding="base64">\n'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                XML += 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\n</chan_samples>\n</channel>\n</channels>\n<trigger>\n'
                XML += '<trig_source value="channel 1"/>\n<trig_slope value="positive"/>\n<trig_coupling value="dc"/>\n<trig_level value="0.000000e+000"/>\n'
                XML += '<trig_mode value="autolevel"/>\n<trig_delay value="0.000000e+000"/>\n<trig_received value="32"/>\n</trigger>\n'
                XML += '<measurements>\n<measurement number="1">\n<meas_channel value="channel 1"/>\n<meas_selection value="none"/>\n<meas_result value="0.000000e+000"/>\n'
                XML += '</measurement>\n<measurement number="2">\n<meas_channel value="channel 1"/>\n<meas_selection value="none"/>\n<meas_result value="0.000000e+000"/>\n'
                XML += '</measurement>\n<measurement number="3">\n<meas_channel value="channel 1"/>\n<meas_selection value="none"/>\n<meas_result value="0.000000e+000"/>\n'
                XML += '</measurement>\n</measurements>\n</oscilloscope>\n'
            if XMLResponse['PowerSupply']:
                XML += XMLResponse['PowerSupply']
            else:
                XML += '<dcpower>\n<dc_outputs>\n<dc_output channel="6V+">\n<dc_voltage value="0.000000e+000"/>\n<dc_current value="5.000000e-001"/>\n'
                XML += '<dc_voltage_actual value="-1.110000e-004"/>\n<dc_current_actual value="4.100000e-005"/>\n<dc_output_enabled value="1"/>\n'
                XML += '<dc_output_limited value="0"/>\n</dc_output>\n<dc_output channel="25V+">\n<dc_voltage value="5.000000e+000"/>\n'
                XML += '<dc_current value="5.000000e-001"/>\n<dc_voltage_actual value="4.996699e+000"/>\n<dc_current_actual value="-2.700000e-004"/>\n'
            XML += '</response>\n</protocol>\n'
            return XML
        else:
            return '<protocol version="1.3">\n<error>Equipment Server response length incorrect</error>\n</protocol>\n'

    def CheckSessionKey(self, SessionKey):
        self.ClientList = ClientRegistry()
        for Client in self.ClientList.ClientList:
            Session = Client.GetSession()
            if Session == None:
                return False
            if Session.GetKey() == SessionKey:
                return True
        return False

                
