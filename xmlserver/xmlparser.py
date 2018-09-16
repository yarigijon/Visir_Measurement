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

import xml.etree.cElementTree as ET # por compatibilid de codigo con el nativo de python le cambio el nombre

class XMLParser(object):
    def __init__(self):
        self.__mProtocol = None
        self.__mRequest = None
        self.__mLogin = None
        self.IsLogin = False
        self.__mCircuit = []
        self.__mMultimeter = []
        self.__mFunctionGenerator = []
        self.__mOscilloscope = []
        self.__mDCPower = []

    def ParserRoot(self, XMLStream):
        Root = ET.fromstring(XMLStream)
        Iter = Root.getiterator()
        for Element in Iter:
            if Element.tag == "protocol":
                self.__mProtocol = Element
            elif Element.tag == "login":
                self.IsLogin = True
                self.__mLogin = Element
            elif Element.tag == "request":
                self.IsLogin = False
                self.__mRequest = Element
            elif Element.tag == "circuit":
                self.__mCircuit = Element
            elif Element.tag == "multimeter":
                self.__mMultimeter.append(Element)
            elif Element.tag == "functiongenerator":
                self.__mFunctionGenerator.append(Element)
            elif Element.tag == "oscilloscope":
                self.__mOscilloscope.append(Element)
            elif Element.tag == "dcpower":
                self.__mDCPower.append(Element)
    
    def ParserProtocol(self):
        return float(self.__mProtocol.items()[0][1]) # retorno valor de version

    def ParserRequest(self):
        #return hex(int(self.__mRequest.items()[0][1], 16)) # retorno valor sesionkey (como int hex, ver si es mas interesante como string)
        return self.__mRequest.items()[0][1] # retorno valor sessionkey (como string, ver si es mas interesante como int hex)

    def ParserCircuit(self):
        Iter = self.__mCircuit.getiterator()
        CircuitList = [] # lo pasamos como un array por si circuit incluye mas de un CircuitList
        for Element in Iter:
            if Element.text:
                CircuitList.append(Element.text)
        return CircuitList # retorno array con cicuitlists que hay en circuit

    def ParserMultimeter(self):
        Multimeter = []
        for it in self.__mMultimeter:
            Iter = it.getiterator()
            MultimeterDict = {"id": None, "function": None, "resolution": None, "range": None, "autozero": None}
            for Element in Iter:
                if Element.tag == "multimeter":
                    MultimeterDict["id"] = int(Element.items()[0][1])
                elif Element.tag == "dmm_function":
                    MultimeterDict["function"] = Element.items()[0][1]
                elif Element.tag == "dmm_resolution":
                    MultimeterDict["resolution"] = Element.items()[0][1]
                elif Element.tag == "dmm_range":
                    MultimeterDict["range"] = Element.items()[0][1] # todo: lo dejo como string ver si tienen que ser int
                elif Element.tag == "dmm_autozero":
                    MultimeterDict["autozero"] = Element.items()[0][1] # todo: lo dejo como string ver si tienen que ser int
            Multimeter.append(MultimeterDict)
        return Multimeter # retornamos un array con los diccionarios correspondientes a cada uno de los multimetros

    def ParserFunctionGenerator(self):
        FunctionGenerator = []
        for it in self.__mFunctionGenerator:
            Iter = it.getiterator()
            FunctionGeneratorDict = {"id": None, "waveform": None, "frequency": None, "amplitude": None, "offset": None}
            for Element in Iter:
                if Element.tag == "functiongenerator":
                    FunctionGeneratorDict["id"] = int(Element.items()[0][1])
                elif Element.tag == "fg_waveform":
                    FunctionGeneratorDict["waveform"] = Element.items()[0][1]
                elif Element.tag == "fg_frequency":
                    FunctionGeneratorDict["frequency"] = Element.items()[0][1] # todo: lo dejo como string ver si tiene que ser int/float
                elif Element.tag == "fg_amplitude":
                    FunctionGeneratorDict["amplitude"] = Element.items()[0][1] # todo: lo dejo como string ver si tienen que ser float
                elif Element.tag == "fg_offset":
                    FunctionGeneratorDict["offset"] = Element.items()[0][1] # todo: lo dejo como string ver si tienen que ser int/float
            FunctionGenerator.append(FunctionGeneratorDict)
        return FunctionGenerator # retornamos un array con los diccionarios correspindientes a cada uno de los generadores de funcion

    def ParserLogin(self):
        #return int(self.__mLogin.items()[1][1]), hex(int(self.__mLogin.items()[0][1], 16)) # retorno valor keepalive en entero y cockie en hex
        return int(self.__mLogin.items()[1][1]), self.__mLogin.items()[0][1] # retorno valor keeplive como entero y cockie como string 

    def ParserOscilloscope(self):
        Oscilloscope = []
        for it in self.__mOscilloscope:
            Iter = it.getiterator()
            OscilloscopeDict = {
                "id": None,
                "samplerate": None, 
                "refpos": None, 
                "horz_recordlength": None, 
                "chan1_enabled": None, 
                "chan1_coupling": None, 
                "chan1_range": None, 
                "chan1_offset": None, 
                "chan1_attenuation": None, 
                "chan2_enabled": None, 
                "chan2_coupling": None, 
                "chan2_range": None, 
                "chan2_offset": None, 
                "chan2_attenuation": None, 
                "trig_source": None, 
                "trig_slope": None, 
                "trig_coupling": None, 
                "trig_level": None, 
                "trig_mode": None, 
                "trig_timeout": None, 
                "trig_delay": None,
                "meas1_channel": None,
                "meas1_selection": None,
                "meas2_channel": None,
                "meas2_selection": None,
                "meas3_channel": None,
                "meas3_selection": None,
                "osc_autoscale": None}
            ChannelEnable = False
            ChannelCoupling = False
            ChannelRange = False
            ChannelOffset = False
            ChannelAttenuation = False
            MeasChannel = 0
            MeasSelection = 0
            for Element in Iter:
                if Element.tag == "oscilloscope":
                   OscilloscopeDict["id"] = Element.items()[0][1]
                elif Element.tag == "horz_samplerate":
                    OscilloscopeDict["samplerate"] = Element.items()[0][1]
                elif Element.tag == "horz_refpos":
                    OscilloscopeDict["refpos"] = Element.items()[0][1]
                elif Element.tag == "horz_recordlength":
                    OscilloscopeDict["horz_recordlength"] = Element.items()[0][1]
                elif Element.tag == "chan_enabled":
                    if ChannelEnable == False: # miro si es la primer pasada (channel 1) o la segunda (channel2)
                        OscilloscopeDict["chan1_enabled"] = Element.items()[0][1]  
                    else:
                        OscilloscopeDict["chan2_enabled"] = Element.items()[0][1]
                    ChannelEnable = True
                elif Element.tag == "chan_coupling":
                    if ChannelCoupling == False: # miro si es la primer pasada (channel 1) o la segunda (channel2)
                        OscilloscopeDict["chan1_coupling"] = Element.items()[0][1]
                    else:
                        OscilloscopeDict["chan2_coupling"] = Element.items()[0][1]
                    ChannelCoupling = True
                elif Element.tag == "chan_range":
                    if ChannelRange == False: # miro si es la primer pasada (channel 1) o la segunda (channel2)
                        OscilloscopeDict["chan1_range"] = Element.items()[0][1]
                    else:
                        OscilloscopeDict["chan2_range"] = Element.items()[0][1]
                    ChannelRange = True
                elif Element.tag == "chan_offset":
                    if ChannelOffset == False: # miro si es la primer pasada (channel 1) o la segunda (channel2)
                        OscilloscopeDict["chan1_offset"] = Element.items()[0][1]
                    else:
                        OscilloscopeDict["chan2_offset"] = Element.items()[0][1]
                    ChannelOffset = True
                elif Element.tag == "chan_attenuation":
                    if ChannelAttenuation == False: # miro si es la primer pasada (channel 1) o la segunda (channel2)
                        OscilloscopeDict["chan1_attenuation"] = Element.items()[0][1]
                    else:
                        OscilloscopeDict["chan2_attenuation"] = Element.items()[0][1]
                    ChannelAttenuation = True
                elif Element.tag == "trig_source":
                    OscilloscopeDict["trig_source"] = Element.items()[0][1]
                elif Element.tag == "trig_slope":
                    OscilloscopeDict["trig_slope"] = Element.items()[0][1]
                elif Element.tag == "trig_coupling":
                    OscilloscopeDict["trig_coupling"] = Element.items()[0][1]
                elif Element.tag == "trig_level":
                    OscilloscopeDict["trig_level"] = Element.items()[0][1]
                elif Element.tag == "trig_mode":
                    OscilloscopeDict["trig_mode"] = Element.items()[0][1]
                elif Element.tag == "trig_timeout":
                    OscilloscopeDict["trig_timeout"] = Element.items()[0][1]
                elif Element.tag == "trig_delay":
                    OscilloscopeDict["trig_delay"] = Element.items()[0][1]
                elif Element.tag == "meas_channel":
                    if MeasChannel == 0:
                        OscilloscopeDict["meas1_channel"] = Element.items()[0][1]
                        MeasChannel +=1
                    elif MeasChannel == 1:
                        OscilloscopeDict["meas2_channel"] = Element.items()[0][1]
                        MeasChannel +=1
                    else:
                        OscilloscopeDict["meas3_channel"] = Element.items()[0][1]
                        MeasChannel = 0
                elif Element.tag == "meas_selection":
                    if MeasSelection == 0:
                        OscilloscopeDict["meas1_selection"] = Element.items()[0][1]
                        MeasSelection +=1
                    elif MeasSelection == 1:
                        OscilloscopeDict["meas2_selection"] = Element.items()[0][1]
                        MeasSelection +=1
                    else:
                        OscilloscopeDict["meas3_selection"] = Element.items()[0][1]
                        MeasSelection = 0
                elif Element.tag == "osc_autoscale":
                    OscilloscopeDict["osc_autoscale"] = Element.items()[0][1]
            Oscilloscope.append(OscilloscopeDict)
        return Oscilloscope

    def ParserDCPower(self):
        DCPower = []
        for it in self.__mDCPower:
            Iter = it.getiterator()
            DCPowerDict = {"id": None, "6V+_dc_voltage": None, "6V+_dc_current": None, "25V+_dc_voltage": None, "25V+_dc_current": None, "25V-_dc_voltage": None, "25V-_dc_current": None}
            DCOutputVoltage = 0
            DCOutputCurrent = 0
            for Element in Iter:
                if Element.tag == "dcpower":
                   DCPowerDict["id"] = int(Element.items()[0][1])
                elif Element.tag == "dc_voltage":
                    if DCOutputVoltage == 0:
                        DCPowerDict["6V+_dc_voltage"] = float(Element.items()[0][1])
                        DCOutputVoltage += 1
                    elif DCOutputVoltage == 1:
                        DCPowerDict["25V+_dc_voltage"] = float(Element.items()[0][1])
                        DCOutputVoltage += 1
                    else:
                        DCPowerDict["25V-_dc_voltage"] = float(Element.items()[0][1])
                        DCOutputVoltage = 0
                elif Element.tag == "dc_current":
                    if DCOutputCurrent == 0:
                        DCPowerDict["6V+_dc_current"] = float(Element.items()[0][1])
                        DCOutputCurrent += 1
                    elif DCOutputCurrent == 1:
                        DCPowerDict["25V+_dc_current"] = float(Element.items()[0][1])
                        DCOutputCurrent += 1
                    else:
                        DCPowerDict["25V-_dc_current"] = float(Element.items()[0][1])
                        DCOutputCurrent = 0
            DCPower.append(DCPowerDict)
        return DCPower