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


class MaxFilesRegistry (object):

    def __new__(cls):
        # Implementacion especial del singleton
        if not hasattr(cls, 'instance'):  # Si no existe el atributo 'instance'
            cls.instance = super(
                MaxFilesRegistry,
                cls).__new__(cls)  # lo creamos
        return cls.instance

    def Register(self):
        self.Maxfiles = []

    def AddMaxFile(self, MaxFile):
        self.Maxfiles.append(MaxFile)

    def GetMaxFiles(self):
        return self.Maxfiles
