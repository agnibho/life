from Tkinter import BooleanVar, StringVar
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import Cell
  
class Board(tk.Frame):
  cells=[]
  SIZE=10
  WIDTH=50
  DEPTH=50
  start_dim=[]
  Num=0
  auto={}
  timer={}
  
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.auto=BooleanVar()
    self.stepnum=StringVar()
    
  def render(self, width, depth):
    self.WIDTH=width
    self.DEPTH=depth
    self.start_dim=[width, depth]
    self.contain=tk.Canvas(self, width=self.WIDTH*self.SIZE, height=self.DEPTH*self.SIZE)
    self.contain.grid()
    for i in range(0, self.WIDTH):
      self.cells.append([])
      for j in range (0, self.DEPTH):
	self.cells[i].append(Cell.Cell(self.contain.create_rectangle(i*self.SIZE, j*self.SIZE, i*self.SIZE+self.SIZE, j*self.SIZE+self.SIZE, fill="white", outline="gray"), self.contain))
    self.startbtn=tk.Button(self, text="Start", command=self.start)
    self.autobtn=tk.Checkbutton(self, text="Automatic", command=self.run, variable=self.auto)
    self.stepbtn=tk.Button(self, text="Next Step", command=self.step)
    self.resetbtn=tk.Button(self, text="Reset", command=self.reset)
    self.openbtn=tk.Button(self, text="Open", command=self.openfile)
    self.savebtn=tk.Button(self, text="Save", command=self.savefile)
    self.steplbl=tk.Label(self, textvariable=self.stepnum)
    self.steplbl.grid(row=1)
    self.startbtn.grid(row=1, sticky="W")
    self.openbtn.grid(row=1, sticky="E")
    
  def recreate(self, width, depth):
    self.contain.destroy()
    self.cells=[]
    self.WIDTH=width
    self.DEPTH=depth
    if(self.SIZE*self.WIDTH>self.winfo_screenwidth()-100 or self.SIZE*self.DEPTH>self.winfo_screenheight()-150):
      self.SIZE=5
      self.WIDTH=(self.winfo_screenwidth()-100)/self.SIZE
      self.DEPTH=(self.winfo_screenheight()-150)/self.SIZE
    else:
      self.SIZE=10
    self.contain=tk.Canvas(self, width=self.WIDTH*self.SIZE, height=self.DEPTH*self.SIZE)
    self.contain.grid(row=0)

    for i in range(0, self.WIDTH):
      self.cells.append([])
      for j in range (0, self.DEPTH):
	self.cells[i].append(Cell.Cell(self.contain.create_rectangle(i*self.SIZE, j*self.SIZE, i*self.SIZE+self.SIZE, j*self.SIZE+self.SIZE, fill="white", outline="gray"), self.contain))
    
  def start(self):
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].freeze()
    self.startbtn.grid_remove()
    self.openbtn.grid_remove()
    self.stepbtn.grid(row=1, sticky="W")
    self.resetbtn.grid(row=1, sticky="E")
    self.autobtn.grid(row=2, sticky="W")
    self.savebtn.grid(row=2, sticky="E")
    
  def openfile(self):
    filename=tkFileDialog.askopenfilename(filetypes=[("Life 1.06", "*.life"), ("Life 1.6", "*.lif"), ("All", "*")])
    self.parsefile(filename)
    
  def savefile(self):
    filename=tkFileDialog.asksaveasfilename(filetypes=[("Life 1.06", "*.life"), ("Life 1.6", "*.lif")], defaultextension=".life")
    self.writefile(filename)
    
  def parsefile(self, filename):
    self.reset()
    arr=[]
    arr.append([])
    arr.append([])
    if(len(filename)>0):
      try:
	with open(filename) as f:
	  for line in f:
	    data=line.strip().lower()
	    if(len(data)>0):
	      if(data.startswith("#life")):
		if(data!="#life 1.06" and data!="#life 1.6"):
		  tkMessageBox.showerror("Format Error", "The file must be in Life 1.06 format.")
		  return
	      elif(data.startswith("#")):
		continue
	      else:
		arr[0].append([])
		arr[1].append([])
		try:
		  arr[0][-1]=int(data.split()[0])
		  arr[1][-1]=int(data.split()[1])
		except ValueError:
		  tkMessageBox.showerror("Format Error", "Failed to open. The file has formatting error.")
		  print "Failed to open file\nFormat error near: "+line
		  return
      except IOError:
	tkMessageBox.showerror("File not found", "Failed to open the specified file. Make sure the file exists and is readable.")
	return
      except Exception, e:
	tkMessageBox.showerror("Error", "Failed to open the specified file.")
	print e
	return
    else:
      return
    if((max(arr[0])-min(arr[0]))>self.WIDTH/2 or (max(arr[1])-min(arr[1]))>self.DEPTH/2):
      width=(max(arr[0])-min(arr[0]))*2
      depth=(max(arr[1])-min(arr[1]))*2
      self.recreate(width, depth)
    
    if(min(arr[0])<=0):
      for i in range(0, len(arr[0])):
	arr[0][i]+=self.WIDTH/2
    if(min(arr[1])<=0):
      for i in range(0, len(arr[1])):
	arr[1][i]+=self.DEPTH/2
    for i in range(0, len(arr[0])):
      while(arr[0][i]<0):
	arr[0][i]+=self.WIDTH
      while(arr[0][i]>self.WIDTH):
	arr[0][i]-=self.WIDTH
    for i in range(0, len(arr[0])):
      while(arr[1][i]<0):
	arr[1][i]+=self.DEPTH
      while(arr[1][i]>self.DEPTH):
	arr[1][i]-=self.DEPTH
    for i in range(0, len(arr[0])):
      self.cells[arr[0][i]][arr[1][i]].makeLive()
      self.cells[arr[0][i]][arr[1][i]].commit()
      
  def writefile(self, filename):
    if(len(filename)>0):
      f=open(filename, "w")
      f.write("#Life 1.06\r\n")
      for i in range(0, self.WIDTH):
	for j in range (0, self.DEPTH):
	  if(self.cells[i][j].getState()=="live"):
	    f.write(str(i)+" "+str(j)+"\r\n")
      f.close()
    
  def reset(self):
    self.Num=0
    self.stepnum.set("")
    if(self.WIDTH==self.start_dim[0] and self.DEPTH==self.start_dim[1]):
      for i in range(0, self.WIDTH):
	for j in range (0, self.DEPTH):
	  self.cells[i][j].makeDead()
	  self.cells[i][j].commit()
	  self.cells[i][j].unfreeze()
    else:
      self.recreate(self.start_dim[0], self.start_dim[1])
    self.stepbtn.grid_remove()
    self.resetbtn.grid_remove()
    self.autobtn.grid_remove()
    self.savebtn.grid_remove()
    self.startbtn.grid()
    self.openbtn.grid()
    if(self.auto.get()):
      self.autobtn.invoke()
    
  def step(self):
    self.Num+=1
    if(self.WIDTH>30):
      self.stepnum.set("Generation: "+str(self.Num))
    else:
      self.stepnum.set(str(self.Num))
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