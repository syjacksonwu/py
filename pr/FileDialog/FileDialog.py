from Tkinter import *
from FileDialog import *

root = Tk()
fd = LoadFileDialog(root)
filename = fd.go()

print filename
root.mainloop()
