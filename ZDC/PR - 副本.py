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


class PRNR:
    def __init__(self, widget,strfam):
        self.widget = widget
        self.strfam = strfam
        
    def __call__(self):
        print(self.strfam, self.widget['text'])


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
            if(c1>30):
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

    B1 = Button(root, text="Generate", command=Generate).grid(row=r,column=c)   # 
    B2 = Button(root, text="Output",command=OutputZDC).grid(row=r,column=c+1)

    r=r+1
    c=0
    troot=tree.getroot()
    
    # below is CODIERUNG
    lbl = Label(root, text="CODIERUNG", borderwidth=1 ).grid(row=r,column=c+1)
    r=r+1
    c=0
    for table in troot.iter('TABELLE'):
        Modus=table.find('MODUS')
        if Modus.text == "C":
            ModusTeil = table.find('MODUSTEIL')
            
            lbl = Label(root, text=ModusTeil.text, borderwidth=1 )
            lbl.grid(row=r,column=c)
            #print(ModusTeil.text)

            ent = Entry(root)
            ent.grid(row=r, column=c+1)
                    
            r=r+1
            
    

    # below is PROGRAMMIERUNG
    lbl = Label(root, text="PROGRAMMIERUNG", borderwidth=1 ).grid(row=r,column=c+1)
    r=r+1
    c=0
    
    for table in troot.iter('TABELLE'):
        Modus=table.find('MODUS')
        if Modus.text == "P":
            #print(Modus.text)
            ModusTeil = table.find('MODUSTEIL')
            
            lbl = Label(root, text=ModusTeil.text, borderwidth=1 )
            lbl.grid(row=r,column=c)
            #print(ModusTeil.text)

            ent = Entry(root)
            ent.grid(row=r, column=c+1)
                    
            r=r+1
        

def PrnrIsValid(prnrs):
# PrnrIsValid: Check if this prnr line is inside the order. 
    # L0L+1ZF/1ZE/1ZP
    
    print('this prnr is valid')
    return True
    
      
# buil up a new ZDC file.
def OutputZDC():
    
    #tree = ET.parse("C:\ZDC\ESP.xml")
    order_pr = Generate()
    troot=tree.getroot()
    
    for table in troot.iter('TABELLE'):
        modus=table.find('MODUS').text
        print(modus)

        tab=table.find('TAB')

        for fam in tab.findall('FAM'):
            for tegue in fam.findall('TEGUE'):
                prnr = tegue.find('PRNR').text
                #print(prnrs)
                lst_pr=re.split('\++',prnr)

                for p in lst_pr:
                    #pr nr with /
                    if re.search('\/',p):
                        lst_or_pr=re.split('\/',p)
                        flag_or_pr=0

                        for or_pr in lst_or_pr:
                            if re.search(or_pr,order_pr):
                                flag_or_pr=1
                                print("multi: ",p,"---------Y")
                                break

                        if flag_or_pr==0:
                            print("multi: ",p,"---------N, delete TEGUE")
                            fam.remove(tegue)
                            break
                    # signle pr
                    else:
                        if re.search(p,order_pr):
                            print("single: ",p,"---------Y")
                        else:
                            print("single: ",p,"---------N, delete TEGUE")
                            fam.remove(tegue)
                            break
                            
                            
                

    tree.write('output._')
    f=open("output._",'r')
    f_content=f.read()
    
    fhead='''<?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE ZDC PUBLIC "ZDC020401.dtd" "ZDC020401.dtd">
    <?xml-stylesheet href="ZDC020401.xsl" type="text/xsl"?>
    <!--SWS added by process-->'''

    filenewname=""
    fadd=open("Output.xml",'w')
    fadd.write(fhead)
    fadd.write(f_content)
    f.close()


def Generate():
    str_oder=""
    for e in lst:
        if e[1].get() == "":
            print("error, one pr nr is not assigned.")
            showinfo(title="error",message="one pr nr is not assigned.")
            return
        print(e[0]['text'],e[1].get())
        str_oder=str_oder+"+"+e[1].get()

    print(str_oder)
    return str_oder

    
       
def OpenFile():
    #File_Path="C:\ZDC\BCM.xml" 
    global tree
    global troot
    global FileName
    
    
    #if(File_Path == None):
    File_Path = askopenfilename()
    #FileName = 
      
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
    root.mainloop()


