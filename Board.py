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
  Pop=-1
  Max=0
  mode="edit"
  timer={}
  original={}
  
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.stepnum=StringVar()
    self.steppop=StringVar()
    
  def render(self, width, depth):
    self.WIDTH=width
    self.DEPTH=depth
    self.start_dim=[width, depth]
    self.statusbar=tk.Frame(self)
    self.steplbl=tk.Label(self.statusbar, textvariable=self.stepnum, padx=10)
    self.poplbl=tk.Label(self.statusbar, textvariable=self.steppop, padx=10)
    self.contain=tk.Canvas(self, width=self.WIDTH*self.SIZE, height=self.DEPTH*self.SIZE)
    self.toolbar=tk.Frame(self)
    self.startbtn=tk.Button(self.toolbar, text="Start", command=self.auto)
    self.pausebtn=tk.Button(self.toolbar, text="Pause", state="disabled", command=self.pause)
    self.stepbtn=tk.Button(self.toolbar, text="Next Step", command=self.step)
    self.resetbtn=tk.Button(self.toolbar, text="Reset", command=self.reset)
    self.revertbtn=tk.Button(self.toolbar, text="Revert", state="disabled", command=self.revert)
    self.openbtn=tk.Button(self.toolbar, text="Open", command=self.openfile)
    self.savebtn=tk.Button(self.toolbar, text="Save", command=self.savefile)
    self.aboutbtn=tk.Button(self.toolbar, text="About", command=self.about)
    self.statusbar.grid(row=0)
    self.steplbl.grid(row=0, column=0)
    self.poplbl.grid(row=0, column=1)
    self.contain.grid(row=1)
    self.toolbar.grid(row=2)
    self.startbtn.grid(row=0, column=0)
    self.pausebtn.grid(row=0, column=1)
    self.stepbtn.grid(row=0, column=2)
    self.resetbtn.grid(row=0, column=3)
    self.openbtn.grid(row=1, column=0)
    self.savebtn.grid(row=1, column=1)
    self.revertbtn.grid(row=1, column=2)
    self.aboutbtn.grid(row=1, column=3)
    
    for i in range(0, self.WIDTH):
      self.cells.append([])
      for j in range (0, self.DEPTH):
	self.cells[i].append(Cell.Cell(self.contain.create_rectangle(i*self.SIZE, j*self.SIZE, i*self.SIZE+self.SIZE, j*self.SIZE+self.SIZE, fill="white", outline="gray"), self.contain))
    
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
    self.contain.grid(row=1)

    for i in range(0, self.WIDTH):
      self.cells.append([])
      for j in range (0, self.DEPTH):
	self.cells[i].append(Cell.Cell(self.contain.create_rectangle(i*self.SIZE, j*self.SIZE, i*self.SIZE+self.SIZE, j*self.SIZE+self.SIZE, fill="white", outline="gray"), self.contain))
    
  def run(self):
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].freeze()
    self.original=self.cells
    self.mode="man"
    self.revertbtn["state"]="normal"
    
  def step(self):
    if(self.Pop==0):
      tkMessageBox.showwarning("Game over", "All life forms have been terminated")
      return
    if(self.mode=="edit"):
      self.run()
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	z=self.count(i, j)
	if(self.cells[i][j].getState()=="live"):
	  if(z<2 or z>3):
	    self.cells[i][j].makeDead()
	elif(self.cells[i][j].getState()=="dead"):
	  if(z==3):
	    self.cells[i][j].makeLive()
    self.Pop=0
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].commit()
	if(self.cells[i][j].getState()=="live"):
	  self.Pop+=1
	  if(self.Pop>self.Max):
	    self.Max=self.Pop
    if(self.Pop>0):
      self.Num+=1
    else:
      tkMessageBox.showwarning("Game over", "All life forms have been terminated\nMaximun polpulation reached: "+str(self.Max))
      self.pause()
      self.startbtn["state"]="disabled"
      self.stepbtn["state"]="disabled"
    if(self.WIDTH>30):
      self.stepnum.set("Generation: "+str(self.Num))
      self.steppop.set("Population: "+str(self.Pop))
    else:
      self.stepnum.set(str("Gen:"+str(self.Num)))
      self.steppop.set("Pop:"+str(self.Pop))
    if(self.mode=="auto"):
      self.timer=self.after(1000, self.step)
	
  def auto(self):
    self.startbtn["state"]="disabled"
    self.stepbtn["state"]="disabled"
    self.pausebtn["state"]="normal"
    if(self.mode=="edit"):
      self.run()
    self.mode="auto"
    self.timer=self.after(1000, self.step)
      
  def pause(self):
    self.startbtn["state"]="normal"
    self.stepbtn["state"]="normal"
    self.pausebtn["state"]="disabled"
    self.mode="man"
    self.after_cancel(self.timer)
    
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
      if((max(arr[0])-min(arr[0]))>self.WIDTH/2):
	width=(max(arr[0])-min(arr[0]))*2
	depth=self.DEPTH
      if((max(arr[1])-min(arr[1]))>self.DEPTH/2):
	depth=(max(arr[1])-min(arr[1]))*2
	width=self.WIDTH
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
      self.cells[arr[0][i]][arr[1][i]].toggle()
      
  def writefile(self, filename):
    if(len(filename)>0):
      f=open(filename, "w")
      f.write("#Life 1.06\r\n")
      for i in range(0, self.WIDTH):
	for j in range (0, self.DEPTH):
	  if(self.cells[i][j].getState()=="live"):
	    f.write(str(i)+" "+str(j)+"\r\n")
      f.close()
    
  def reset(self, full=True):
    self.Pop=0
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	if(self.cells[i][j].getState()=="live"):
	  self.Pop+=1
    if(self.Pop>0):
      flag=tkMessageBox.askokcancel("Confirm Reset", "This action will erase all the cells from current board. Are you sure to continue?")
    else:
      flag=True
    if(flag):
      self.pause()
      self.mode="edit"
      self.Num=0
      self.Pop=-1
      self.Max=0
      self.stepnum.set("")
      self.steppop.set("")
      if(full):
	if(self.WIDTH==self.start_dim[0] and self.DEPTH==self.start_dim[1]):
	  for i in range(0, self.WIDTH):
	    for j in range (0, self.DEPTH):
	      self.cells[i][j].clear()
	else:
	  self.recreate(self.start_dim[0], self.start_dim[1])
    self.revertbtn["state"]="disabled"
    
  def revert(self):
    self.reset(False)
    for i in range(0, self.WIDTH):
      for j in range (0, self.DEPTH):
	self.cells[i][j].revert()
    
  def about(self):
    tkMessageBox.showinfo("About Life", "Life 1.03 by Agnibho Mondal\nBased on Conway's Game of Life\nhttp://code.agnibho.com/life")
    
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