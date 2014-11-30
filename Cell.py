'''
    Agnibho's Game of Life - Python implementation
    Copyright (C) 2014  Agnibho Mondal
    
    This file is part of .Agnibho's Game of Life

    Agnibho's Game of Life is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Agnibho's Game of Life is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Agnibho's Game of Life.  If not, see <http://www.gnu.org/licenses/>.
'''

import Tkinter as tk

class Cell(tk.Canvas):
  __state="dead"
  __buff="dead"
  __obj={}
  
  def __init__(self, master=None):
    tk.Canvas.__init__(self, master, height=10, width=10)
    self.__obj=self.create_rectangle(0, 0, 10, 10, fill="white")
    self.tag_bind(self.__obj, '<ButtonPress-1>', self.toggle)
  
  def getState(self):
    return self.__state
  
  def makeLive(self):
    self.__buff="live"
    
  def makeDead(self):
    self.__buff="dead"
    
  def commit(self):
    self.__state=self.__buff
    if(self.__state=="live"):
      self.itemconfig(self.__obj, fill="black")
    elif(self.__state=="dead"):
      self.itemconfig(self.__obj, fill="white")
	 
    
  def toggle(self, event):
    if(self.__state=="live"):
      self.__state="dead"
      self.itemconfig(self.__obj, fill="white")
    elif(self.__state=="dead"):
      self.__state="live"
      self.itemconfig(self.__obj, fill="black")
      
  def freeze(self):
    self.tag_unbind(self.__obj, '<ButtonPress-1>')