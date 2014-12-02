#! /usr/bin/python
import sys
import Board

width=20
depth=20
app=Board.Board()
app.master.title("The Game of Life")

if(len(sys.argv)>1):
  if(len(sys.argv)==3):
    try:
      width=int(sys.argv[1])
      depth=int(sys.argv[2])
    except Exception:
      print "Dimensions must be integer"
      sys.exit()
  else:
    print "Argument not recognized"
    sys.exit()
if(width<5 or depth<5):
  width=20
  depth=20
  print "Dimensions must be more than 5x5"
  sys.exit()
elif(width>app.winfo_screenwidth()/10 or depth>app.winfo_screenheight()/10-10):
  width=20
  depth=20
  print "Dimensions are too large to fit in the screen. Maximum allowed dimension "+str(app.winfo_screenwidth()/10)+"x"+str(app.winfo_screenheight()/10-10)
  sys.exit()

app.render(width, depth)
app.mainloop()