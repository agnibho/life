#! /usr/bin/python
import sys
import Board

width=50
depth=50
filename=""
app=Board.Board()
app.master.title("Conway's Game of Life - Agnibho.com")

if(len(sys.argv)>1):
  if(len(sys.argv)==3):
    try:
      width=int(sys.argv[1])
      depth=int(sys.argv[2])
    except Exception:
      print "Dimensions must be integer"
      sys.exit()
  elif(len(sys.argv)==2):
    filename=sys.argv[1]
  else:
    print "Argument not recognized"
    sys.exit()
if(width<10 or depth<10):
  width=50
  depth=50
  print "Dimensions must be more than 10x10"
  sys.exit()
elif(width>app.winfo_screenwidth()/10 or depth>(app.winfo_screenheight()-150)/10):
  width=50
  depth=50
  print "Dimensions are too large to fit in the screen. Maximum allowed dimension "+str(app.winfo_screenwidth()/10)+"x"+str((app.winfo_screenheight()-150)/10)
  sys.exit()

app.render(width, depth)
if(len(filename)>0):
  app.parsefile(filename)
app.mainloop()