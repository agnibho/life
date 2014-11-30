#! /usr/bin/python
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
import Board

app=Board.Board()
app.master.title("The Game of Life")
app.mainloop()

def step():
  for i in cells:
    for j in i:
      j.makeDead()