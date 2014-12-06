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