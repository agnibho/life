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
import Cell

WIDTH=20
DEPTH=20

Num=0
  
class Board(tk.Frame):
  cells=[]
  
  def __init__(self, master=None):
    global WIDTH
    global DEPTH
    tk.Frame.__init__(self, master)
    self.grid()
    self.contain=tk.Frame(self)
    self.contain.grid()
    for i in range(0, WIDTH):
      self.cells.append([])
      for j in range (0, DEPTH):
	self.cells[i].append(Cell.Cell(self.contain))
	self.cells[i][j].grid(row=i, column=j)
    self.launch=tk.Button(self, text="Start", command=self.start)
    self.launch.grid()
    
  def start(self):
    global WIDTH
    global DEPTH
    for i in range(0, WIDTH):
      for j in range (0, DEPTH):
	self.cells[i][j].freeze()
    self.launch.grid_remove()
    self.btn=tk.Button(self, text="Next Step", command=self.step)
    self.btn.grid()
    
  def step(self):
    global WIDTH
    global DEPTH
    global Num
    #print str(Num)+" step"
    Num+=1
    for i in range(0, WIDTH):
      for j in range (0, DEPTH):
	z=self.count(i, j)
	if(self.cells[i][j].getState()=="live"):
	  #print str(Num)+" "+str(i)+" "+str(j)+" "+str(z)+" "+self.cells[i][j].getState()
	  if(z<2 or z>3):
	    self.cells[i][j].makeDead()
	elif(self.cells[i][j].getState()=="dead"):
	  if(z==3):
	    self.cells[i][j].makeLive()
    for i in range(0, WIDTH):
      for j in range (0, DEPTH):
	self.cells[i][j].commit()
	
  def count(self, i, j):
    z=0
    for cl in [self.getCell(i-1, j-1), self.getCell(i-1, j), self.getCell(i, j-1), self.getCell(i+1, j+1), self.getCell(i+1, j), self.getCell(i, j+1), self.getCell(i-1, j+1), self.getCell(i+1, j-1)]:
      if(cl.getState()=="live"):
	z+=1
    return z
    
  def getCell(self, x, y):
    global WIDTH
    global DEPTH
    if(x==-1):
      x=WIDTH-1
    elif(x>=WIDTH):
      x=0
    if(y==-1):
      y=DEPTH-1
    elif(y>=DEPTH):
      y=0
    return self.cells[x][y]