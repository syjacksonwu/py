from Tkinter import *
from tkFileDialog import askopenfilename
import xml.etree.ElementTree as ET

class ZDC_XML():

   def __init__(self):
      self.tree = None
      self.root = None

   def OpenZDC(self,zdc_path):

      tree=ET.parse(zdc_path)
      root=tree.getroot() 

   # list short family name
   def lssfam(self):
       
       for reffam in root.iter('REFFAM'):
           print reffam.find('FAMNR').text

   def lsfam(self,n):   
       n=n.upper();
       
       for reffam in root.iter('REFFAM'):
           if reffam.find('FAMNR').text == n:
               for prnr in reffam.iter('PRNR'):
                   print prnr.text,

   # list detail family name
   def lsfamall(self):  
       for reffam in root.iter('REFFAM'):
           print reffam.find('FAMNR').text,

           for prnr in reffam.iter('PRNR'):
               print prnr.text,

           print

   def importfam(self):     
            
       #f=open('d:/zdc/reffam.xml','w')
       element = root.find('IDENT')
       #tree._setroot(element)
       
       tree.write('d:/zdc/referenz.xml')
       #f.close()
       print 'import finished.'

class Application(Frame):

   def __init__(self, master=None):
      self.ZDC_Path=''
      self.ZDC = ZDC_XML()

      Frame.__init__(self, master)
      self.pack()
      self.createWidgets()
   
   
   def OpenZDC(self):
      self.ZDC_Path = askopenfilename() 
      print self.ZDC_Path
      
      self.ZDC.OpenZDC(self.ZDC_Path)

   def createWidgets(self):
      menubar = Menu(root)
      filemenu = Menu(menubar, tearoff=0)
      filemenu.add_command(label="Open", command=self.OpenZDC)
      menubar.add_cascade(label="File", menu=filemenu)
      root.config(menu=menubar)



if __name__ == '__main__' :
   root = Tk()
   app = Application(master=root)
   
   
   app.mainloop()


