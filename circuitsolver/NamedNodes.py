#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

# -*- coding: utf-8 -*-
# namespace NamedNodes
# este modulo debe ser llamado siempre a la vez que
# listcomponent en nodeinterpreter y en circuit solver3
# para llamarlo import NamedNodes y para acceder a un objeto en particular
# x NamedNodes.x

# Nodos generadores de funciones
FGenA = "VFGENA"
FGenB = "VFGENB"
# Nodos Fuente de alimentacion
DCPlus25 = "VDC+25V"
DCMinus25 = "VDC-25V"
DCPlus6 = "VDC+6V"
DC_COM = "VDCCOM"
# Nodos multimetro
Dmm = "DMM"
DmmIProbe = "IPROBE"
# Nodos osciloscopio
OscProbe = "PROBE"
OscProbe1 = "PROBE1"
OscProbe2 = "PROBE2"
OscProbe3 = "PROBE3"
OscProbe4 = "PROBE4"
# Nodos de componentes
Shortcut = "SHORTCUT"
# Nodos viejos que podria no volver a ser usados
DC_A = "VDCA"
DC_B = "VDCB"
DC_5VA = "5VA"
DC_5VB = "5VB"
# apartir de aqui se añadiran nuevos nodos si son necesarios
