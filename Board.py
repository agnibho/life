from Tkinter import BooleanVar
import Tkinter as tk
import Cell
  
class Board(tk.Frame):
  cells=[]
  WIDTH=20
  DEPTH=20
  Num=0
  auto={}
  timer={}
  
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.auto=BooleanVar()
    
  def render(self, width, depth,):
    self.WIDTH=width
    self.DEPTH=depth
    self.contain=tk.Canvas(self, width=self.WIDTH*10, height=self.DEPTH*10)
    self.contain.grid()
    for i in range(0, self.WIDTH):
      self.cells.append([])
      for j in range (0, self.DEPTH):
	self.cells[i].append(Cell.Cell(self.contain.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="white", outline="gray"), self.contain))
    self.startbtn=tk.Button(self, text="Start", command=self.start)
    self.autobtn=tk.Checkbutton(self, text="Automatic", command=self.run, variable=self.auto)
    self.stepbtn=tk.Button(self, text="Next Step", command=self.step)
    self.resetbtn=tk.Button(self, text="Reset", command=self.reset)
    self.startbtn.grid()
    
  def setdim(w, h):
    self.WIDTH=w
    self.DEPTH=h
    
  def start(self):
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].freeze()
    self.startbtn.grid_remove()
    if(self.WIDTH>30):
      self.stepbtn.grid(row=1)
      self.resetbtn.grid(row=1, sticky="E")
      self.autobtn.grid(row=1, sticky="W")
    elif(self.WIDTH>10):
      self.stepbtn.grid(row=1, sticky="W")
      self.resetbtn.grid(row=1, sticky="E")
      self.autobtn.grid(row=2)
    else:
      self.stepbtn.grid()
      self.resetbtn.grid()
      self.autobtn.grid()
    
  def reset(self):
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].makeDead()
	self.cells[i][j].commit()
	self.cells[i][j].unfreeze()
    self.stepbtn.grid_remove()
    self.resetbtn.grid_remove()
    self.autobtn.grid_remove()
    self.startbtn.grid()
    if(self.auto.get()):
      self.autobtn.invoke()
    
  def step(self):
    self.Num+=1
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	z=self.count(i, j)
	if(self.cells[i][j].getState()=="live"):
	  if(z<2 or z>3):
	    self.cells[i][j].makeDead()
	elif(self.cells[i][j].getState()=="dead"):
	  if(z==3):
	    self.cells[i][j].makeLive()
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].commit()
    if(self.auto.get()):
      self.timer=self.after(1000, self.step)
	
  def run(self):
    if(self.auto.get()):
      self.stepbtn["state"]="disabled"
      self.timer=self.after(1000, self.step)
    else:
      self.stepbtn["state"]="normal"
      self.after_cancel(self.timer)
	
  def count(self, i, j):
    z=0
    for cl in [self.getCell(i-1, j-1), self.getCell(i-1, j), self.getCell(i, j-1), self.getCell(i+1, j+1), self.getCell(i+1, j), self.getCell(i, j+1), self.getCell(i-1, j+1), self.getCell(i+1, j-1)]:
      if(cl.getState()=="live"):
	z+=1
    return z
    
  def getCell(self, x, y):
    if(x==-1):
      x=self.WIDTH-1
    elif(x>=self.WIDTH):
      x=0
    if(y==-1):
      y=self.DEPTH-1
    elif(y>=self.DEPTH):
      y=0
    return self.cells[x][y]