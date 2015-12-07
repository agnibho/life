# Agnibho's Game of Life - Python implementation of Conway's Game of Life
# Copyright (C) 2014  Agnibho Mondal

# This file is part of Agnibho's Game of Life

# Agnibho's Game of Life is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Agnibho's Game of Life is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Agnibho's Game of Life.  If not, see <http://www.gnu.org/licenses/>.

import Tkinter as tk

class Cell():
  __obj={}
  __parent={}
  __state="dead"
  __buff="dead"
  __original="dead"
  
  def __init__(self, item, parent):
    self.__obj=item
    self.__parent=parent
    self.__parent.tag_bind(self.__obj, '<ButtonPress-1>', self.toggle)
  
  def getState(self):
    return self.__state
  
  def makeLive(self):
    self.__buff="live"
    
  def makeDead(self):
    self.__buff="dead"
    
  def commit(self):
    self.__state=self.__buff
    if(self.__state=="live"):
      self.__parent.itemconfig(self.__obj, fill="green")
    elif(self.__state=="dead"):
      self.__parent.itemconfig(self.__obj, fill="white")
	 
    
  def toggle(self, event=False):
    if(self.__state=="live"):
      self.__state="dead"
      self.__buff="dead"
      self.__original="dead"
      self.__parent.itemconfig(self.__obj, fill="white")
    elif(self.__state=="dead"):
      self.__state="live"
      self.__buff="live"
      self.__original="live"
      self.__parent.itemconfig(self.__obj, fill="green")
      
  def freeze(self):
    self.__parent.tag_unbind(self.__obj, '<ButtonPress-1>')
  
  def unfreeze(self):
    self.__parent.tag_bind(self.__obj, '<ButtonPress-1>', self.toggle)
    
  def revert(self):
    self.__buff=self.__original
    self.commit()
    self.unfreeze()
    
  def clear(self):
    self.__buff="dead"
    self.__original="dead"
    self.commit()
    self.unfreeze()
