from Tkinter import *
from ttk import *
from tkFileDialog import askopenfilename
from FileDialog import *




import xml.etree.ElementTree as ET
import re

root = Tk()

tree = None
troot= None
FileName = None

r=0
r0=0
c=0
var = []
lst_lbl= [] #list for Entry
lst_ent= []
lst =[]


def CombiPr():
    
    global var
    ss = ''

    for e in var:
        if(e.get() != None):
            if(ss == None):
                ss = e.get()
            else:
                ss = ss + ', ' + e.get()

    print ss

class PRNR:
    def __init__(self, widget,strfam):
        self.widget = widget
        self.strfam = strfam
        
    def __call__(self):
        print (self.strfam, self.widget['text'])
        CombiPr()



def LoadZDC(tree,troot):
    global r
    global r0
    global c
    global var
    global lst_lbl #list for Entry
    global lst_ent
    global lst
    
    for reffam in troot.iter('REFFAM'):
        strfam=reffam.find('FAMNR').text
        
        #print(reffam.find('FAMNR').text,end='\n')

        v = StringVar()
        v.set('')
        var.append(v)
        #print(v.get())

        #lable
        lbl = Label(root, text=strfam, borderwidth=1 )
        lbl.grid(row=r,column=c)
        #print(lbl['text'])
        
        #entery
        ent = Entry(root,textvariable=v)
        #print(ent)
        ent.grid(row=r, column=c+1)

        #append into list.
        lst_lbl.append(lbl)
        lst_ent.append(v)
        lst.append([lbl,v])
        
        c=2
        c1=0
        for prnr in reffam.iter('PRNR'):
            if(c1>20): #30
                c1=0
                c=2
                r=r+1
                
            c1 = c1+1
            
            R1 = Radiobutton(root, text=prnr.text, indicatoron=0, variable=v, value=prnr.text)
            R1.configure(command=PRNR(R1,strfam))
            R1.grid(row=r,column=c)
            
            c=c+1
            
        r = r+1
        c=0    
        r=r+1
        r0=r0+1
        
    r=r+1
    c=0


    r=r+1
    c=0
    troot=tree.getroot()


    # Below is output of PR list.
    lbl = Label(root, text="PR List", borderwidth=1 ).grid(row=r,column=c+1)
    ent = Entry(root,textvariable=prlist).grid(row=r,column=c+2)
            
    

        

def PrnrIsValid(prnrs):
# PrnrIsValid: Check if this prnr line is inside the order. 
    # L0L+1ZF/1ZE/1ZP
    
    print('this prnr is valid')
    return True
        
       
def OpenFile(path):
    #File_Path="C:\ZDC\BCM.xml" 
    global tree
    global troot
    global FileName
     
    
    if(path == None):
        File_Path = askopenfilename()
    else:
        File_Path = path
      
    #print(File_Path)
    #root.title=File_Path
      
    tree = ET.parse(File_Path)
    troot=tree.getroot()
    LoadZDC(tree,troot)
    

if __name__ == '__main__' :
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=OpenFile)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    var = []
    s = StringVar()
    prlist = StringVar()
    
    OpenFile('C:/ZDC/ESP.xml')
    root.mainloop()


