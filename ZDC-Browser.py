import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget, QTreeWidgetItem, QTreeWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QFrame, QSplitter,QLineEdit,
QPushButton, QTreeWidgetItemIterator,QCheckBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import xml.etree.ElementTree as ET
from lxml import etree
#from xml.etree.ElementTree import Element,ElementTree,tostring


class Example(QWidget):

    def __init__(self):
        super().__init__() 
        self.initUI()
 
    
  def closeEvent(self, event):
    sys.exit(0)
 
    
  def initUI(self):
  
    ####Tools Buttons 
    openButton = QPushButton("Open")
    openButton.clicked.connect(self.openzdc)

    updateButton = QPushButton("Update ZDC")
    updateButton.clicked.connect(self.updatezdc)
    
    origButton = QPushButton("Org")
    origButton.clicked.connect(self.orgzdc)
    
    btn_Orig_Tabelle = QPushButton("Org Tab")
    btn_Orig_Tabelle.clicked.connect(self.orig_tree_tab)
        
    cb_Tabelle = QCheckBox('Alle Tabelle', self)
    cb_Tabelle.stateChanged.connect(self.on_QCheckBox_Tabelle_Change)
    
    cb_PR = QCheckBox('Alle PR', self)
    cb_PR.stateChanged.connect(self.on_QCheckBox_PR_Change)
    
    btn_Update_Tree = QPushButton("Update via Tabelle")
    btn_Update_Tree.clicked.connect(self.update_tab)
    
    ###################### PR
    btn_Orig_PrNr = QPushButton("Org PR")
    btn_Orig_PrNr.clicked.connect(self.orig_tree_pr)
    
    btn_Update_PrNr = QPushButton("Update via PR")
    btn_Update_PrNr.clicked.connect(self.update_pr)
    
    self.txt_Find = QLineEdit()
    btn_Find = QPushButton("Find")
    btn_Find.clicked.connect(self.on_btn_Find)
    
    hbox = QHBoxLayout()    
    hbox.addWidget(openButton)
    #hbox.addWidget(updateButton)
    #hbox.addWidget(origButton)
    #hbox.addWidget(btn_Orig_Tabelle)
    hbox.addWidget(btn_Update_Tree)
    hbox.addWidget(cb_Tabelle)
    #hbox.addWidget(btn_Orig_PrNr)
    hbox.addWidget(btn_Update_PrNr)
    hbox.addWidget(cb_PR)
    
    hbox.addWidget(self.txt_Find)
    hbox.addWidget(btn_Find)
    
    hbox.addStretch(1)     
    vbox = QVBoxLayout() 
    
    ###########################################################################
    # Windows - zdc path lists    
    self.topleft = QListWidget(self)
    self.topleft.setFrameShape(QFrame.StyledPanel)
        
    ###########################################################################
    # Windows - Tabelle Tree view
    
    self.midleft = QTreeWidget()  # 实例化一个TreeWidget对象
    self.midleft.setColumnCount(3)  # 设置部件的列数为2
    self.midleft.setDropIndicatorShown(True)    
    self.midleft.setHeaderLabels(['TAB', 'Value','DID'])  # 设置头部信息对应列的标识符    
    self.midleft.setSortingEnabled(True)
    #self.midleft.itemChanged.connect(self.tree_tab_Changed)
    #self.midleft.itemClicked['QTreeWidgetItem*','int'].connect(self.tree_tab_onitemClicked) #点击
    
    ###############################################
    # Windows - prnr Tree view        
  
    self.botleft = QTreeWidget()  # 实例化一个TreeWidget对象
    self.botleft.setColumnCount(2)  # 设置部件的列数为2
    self.botleft.setDropIndicatorShown(True)       
    self.botleft.setHeaderLabels(['FAM', 'PR'])  # 设置头部信息对应列的标识符     
    #self.botleft.itemChanged.connect(self.tree_pr_Changed)
    
    ###########################################################################
 
    # Windows - ZDC view
    self.topright = QWebEngineView(self)  

    #self.topright = QFrame(self)
    #self.topright.setFrameShape(QFrame.StyledPanel)
         
    splitter1 = QSplitter(Qt.Vertical)
    
    splitter1.addWidget(self.topleft)
    splitter1.addWidget(self.midleft)
    
    splitter1.addWidget(self.botleft)
    splitter1.setSizes([100,300,200])
 
    splitter2 = QSplitter(Qt.Horizontal)
    splitter2.addWidget(splitter1)
    splitter2.addWidget(self.topright)
    splitter2.setSizes([150,450])
    
    vbox.addLayout(hbox)
    vbox.addWidget(splitter2)
    
    self.setLayout(vbox)    
    
    self.filename = "C:/Users/WuJianjian/.spyder-py3/V003002118DA__6C0959655Q__AIRBAG.xml"
    #self.loadzdc(self.filename)
    #self.orig_tree_tab()
    #self.orig_tree_pr()
  
    self.setGeometry(600, 600, 600, 400)
    self.setWindowTitle('ZDC-Browser, beta-1, by wujianjian')    
    self.show()

  #############################################################################
  ## Show Original tabelles
  def orig_tree_tab(self):
      
    tree = etree.parse(self.filename)  
    root = tree.getroot()
    tabelles = root.findall(".//TABELLE")
    
    # # Make a tree from Orignial ZDC
    self.midleft.clear()
    # 设置root为self.tree的子树，故root是根节点
    #tr_root = QTreeWidgetItem(self.midleft)
    #tr_root.setText(0, 'ZDC')  # 设置根节点的名称
    
    # 为root节点设置子结点
    for tab in tabelles:
        print(tab.find("MODUSTEIL").text)
        
        child = QTreeWidgetItem(self.midleft)
        child.setText(0, tab.find("MODUS").text)
        child.setText(1, tab.find("MODUSTEIL").text)
        
        if tab.find("RDIDENTIFIER") is not None:
            child.setText(2, tab.find("RDIDENTIFIER").text)
            
        child.setCheckState(0, Qt.Checked)

    self.midleft.expandAll()
      

############################################################################
  # Get PrNr list from orignal ZDC FILE    
  
  def orig_tree_pr(self):
    
    tree = ET.parse(self.filename)  
    root = tree.getroot() 
      
    # Make a PrNr tree from Orignial ZDC    
    self.botleft.clear()
    
    # 设置root为self.tree的子树，故root是根节点
    #pr_root = QTreeWidgetItem(self.botleft)
    #pr_root.setText(0, 'ZDC')  # 设置根节点的名称
          
    # 遍历所有的REFFAM标签
    for fam in root.findall(".//REFFAM"):
        famnr = fam.find("FAMNR")    
        print(famnr.tag,":",famnr.text)
        
        # 为root节点设置子结点
        child = QTreeWidgetItem(self.botleft)
        child.setText(0, famnr.text)        
  
        str_prnr = ""
        for prnr in fam.findall("PRNR"):
            str_prnr = str_prnr + prnr.text + " "        
            print("\t",prnr.text)
            
            child_pr = QTreeWidgetItem(child)
            child_pr.setText(0, prnr.text)
            child_pr.setText(1, 'Description')
            child_pr.setCheckState(0, Qt.Checked)
#            
    self.botleft.expandAll()       
    

  #############################################################################  
  # # Update WebView by Tab-Tree
  
  def update_tab(self):
    tree = etree.parse(self.filename)  
    root = tree.getroot()
    tabellen = root.find(".//TABELLEN")
    tabelles = root.findall(".//TABELLE")

    # 为root节点设置子结点
    for tab in tabelles:
        if self.tree_checked(self.midleft,tab.find("MODUSTEIL").text) == False:
            print("removed", tab.find("MODUSTEIL").text)
            tabellen.remove(tab)
            
    # reload xml
    print('relaod.....')
    tree.write(self.filename+'.tmp.xml',encoding="ISO-8859-1")
    # webview
    self.topright.load(QUrl("file:///" + self.filename+'.tmp.xml'))                
    self.topright.show()


  #############################################################################
  ## Find a text in QWebView  
  def on_btn_Find(self):
    print(self.txt_Find.text())
    self.topright.page().findText(self.txt_Find.text())


  ############################################################################
  # Update WebView by Pr-Tree    
  
  def update_pr(self): 
    
    if not os.path.exists(self.filename+'.tmp.xml'):
        print(self.filename+'.tmp.xml' + ' Not Exsit.')
        return
    
    tree = etree.parse(self.filename+'.tmp.xml')  
    root = tree.getroot()
    fams   = root.findall(".//FAM")
           
    for fam in fams:
        for tegue in fam.findall("TEGUE"):
            
            # 获取一行PR号组合数组
            prnr = tegue[0].text.split('+')
            #print(tegue[0].text)
            
            # 判断是否符合订单
            #print('------',tegue[0].text)
            res = True
            for pr in prnr:
                
                # 组合PR号，继续细分
                if '/' in pr:                                       
                    sub_res = False  # 任何一个存在，则通过
                    for subpr in pr.split('/'):
                        if self.tree_pr_checked(self.botleft,subpr) == True:
                            print(subpr,'/ +')
                            sub_res = True
                            break
                        else:
                            print(subpr,'/ o')
                    res &= sub_res                                    
                            
                # 单个PR号
                else:
                    if self.tree_pr_checked(self.botleft,pr) == True:
                        print(pr,' +')
                        res &= True
                    else:
                        print(pr,' o')
                        res &= False
                        break
            
            if res:
                print('------',tegue[0].text,'\t\t+')
                
            # remove useless tegue
            else:
                print('------',tegue[0].text,'\t\to')
                fam.remove(tegue)
        
    # reload xml
    print('relaod.....')
    tree.write(self.filename+'.prlst.xml',encoding="ISO-8859-1")
    self.topright.load(QUrl("file:///" + self.filename+'.prlst.xml')) # webview
    self.topright.show()

  def openzdc(self):
    self.filename, _ = QFileDialog.getOpenFileName(self,'选择文件','','ZDC files(*.xml)')
    if self.filename:
      self.topleft.addItem(self.filename)
      #self.loadzdc(self.filename)
      #self.loadprs(self.filename)      
      self.loadzdc(self.filename)
      self.orig_tree_tab()
      self.orig_tree_pr()


  def orgzdc(self):
    if self.filename:
        self.topright.load(QUrl("file:///" + self.filename)) # webview

  
  ############################################################################
  # Tab-Tree Changed    
  def tree_tab_Changed(self, item, column):
    #当check状态改变时得到他的状态。
    if item.checkState(column) == Qt.Checked:
        print("checked", item.text(1))
        
    if item.checkState(column) == Qt.Unchecked:
        print("unchecked", item.text(1))


  def on_QCheckBox_Tabelle_Change(self, state):
    iterator = QTreeWidgetItemIterator(self.midleft)
    
    while iterator.value():
        item = iterator.value()
        iterator.__iadd__(1)
        
        if state == Qt.Checked:
            item.setCheckState(0,Qt.Checked)
        else:
            item.setCheckState(0,Qt.Unchecked)
            

  def on_QCheckBox_PR_Change(self, state):
    iterator = QTreeWidgetItemIterator(self.botleft)
    
    while iterator.value():
        item = iterator.value()
        iterator.__iadd__(1)
        
        if state == Qt.Checked:
            item.setCheckState(0,Qt.Checked)
        else:
            item.setCheckState(0,Qt.Unchecked)


  def tree_tab_onitemClicked(self,item,column):
    print(item.text(0))      
      
    
  ############################################################################
  # Pr-Tree Changed
  
  def tree_pr_Changed(self, item, column):
    #当check状态改变时得到他的状态。
    if item.checkState(column) == Qt.Checked:
        print("checked", item.text(1))
        
    if item.checkState(column) == Qt.Unchecked:
        print("unchecked", item.text(1))
        

  ###################################################################
  #
  # Update zdc by pr list & by 
  ###################################################################
  def updatezdc(self):
    tree = etree.parse(self.filename)  
    root = tree.getroot()
    tabelles = root.findall(".//TABELLE")
    fams   = root.findall(".//FAM")
    #direkt = root.find(".//DIREKT")
    #tegues = root.findall(".//TEGUE")        
    
    # # Make a TAB tree from Orignial ZDC
    self.midleft.clear()
    # 设置root为self.tree的子树，故root是根节点
    tr_root = QTreeWidgetItem(self.midleft)
    tr_root.setText(0, 'ZDC')  # 设置根节点的名称
    
    # 为root节点设置子结点
    for tab in tabelles:
        print(tab.find("MODUSTEIL").text)
        
        child = QTreeWidgetItem(tr_root)
        child.setText(0, tab.find("MODUS").text)     # p
        child.setText(1, tab.find("MODUSTEIL").text) #
        child.setCheckState(0, Qt.Unchecked);               
        
    # reload prnr list        
    #self.lst_pr = self.botleft.toPlainText().split()
    
    for fam in fams:
        for tegue in fam.findall("TEGUE"):
            
            # 获取一行PR号组合数组
            prnr = tegue[0].text.split('+')
            #print(tegue[0].text)
            
            # 判断是否符合订单
            #print('------',tegue[0].text)
            res = True
            for pr in prnr:
                
                # 组合PR号，继续细分
                if '/' in pr:                                       
                    sub_res = False  # 任何一个存在，则通过
                    for subpr in pr.split('/'):
                        if subpr in self.lst_pr:
                            print(subpr,'/ +')
                            sub_res = True
                            break
                        else:
                            print(subpr,'/ o')
                    res &= sub_res                                    
                            
                # 单个PR号
                else:
                    if pr in self.lst_pr:                     
                        print(pr,' +')
                        res &= True
                    else:
                        print(pr,' o')
                        res &= False
                        break
            
            if res:
                print('------',tegue[0].text,'\t\t+')
                
            # remove useless tegue
            else:
                print('------',tegue[0].text,'\t\to')
                fam.remove(tegue)

    # Make a DATENBEREICHE tree
    if root.find(".//DATENBEREICHE") is not None:
        datenbereiche = root.find(".//DATENBEREICHE")
        self.dump_subzdc(self.filename,datenbereiche)
        datenbereiche.getparent().remove(datenbereiche)
        
#        root_datenbereiche = etree.Element("ZDC")
#        root_datenbereiche.addprevious(etree.PI('xml-stylesheet', 'href="ZDC0205.xsl" type="text/xsl"'))
#        e_vorschrift = etree.SubElement(root_datenbereiche,"VORSCHRIFT")
#        e_direkt = etree.SubElement(e_vorschrift,"DIREKT")
#        e_direkt.append(datenbereiche)
#        
#        # make a new tree from the new root
#        tree_datenbereiche = root_datenbereiche.getroottree()   
#        tree_datenbereiche.write(self.filename+'.DATENBEREICHE.xml',encoding="ISO-8859-1",doctype='<!DOCTYPE ZDC PUBLIC "ZDC0205.dtd" "ZDC0205.dtd">')
#        
#        # Remove DATENBEREICHE
                
    # reload xml
    print('relaod.....')
    tree.write(self.filename+'001.xml',encoding="ISO-8859-1")
    self.topright.load(QUrl("file:///" + self.filename+'001.xml')) # webview
    self.topright.show()


  # dump a subzdc from original one
  def dump_subzdc(self,filename,subzdc):
    root_new = etree.Element("ZDC")
    root_new.addprevious(etree.PI('xml-stylesheet', 'href="ZDC0205.xsl" type="text/xsl"'))
    e_vorschrift = etree.SubElement(root_new,"VORSCHRIFT")
    e_direkt = etree.SubElement(e_vorschrift,"DIREKT")
    e_direkt.append(subzdc)

    # make a new tree from the new root
    tree_new = root_new.getroottree()   
    tail_new = filename + '.' + subzdc.tag + '.xml'
    tree_new.write(tail_new,encoding="ISO-8859-1",doctype='<!DOCTYPE ZDC PUBLIC "ZDC0205.dtd" "ZDC0205.dtd">')


  # dump a tree from zdc
  #def dump_tree(self,root):
                    
  ###################################################################
  #
  #
  ###################################################################
  def loadzdc(self,filename):
    self.topright.load(QUrl("file:///" + filename)) # webview
    
    tree = ET.parse(filename)  
    root = tree.getroot()
      
    # Loading PrNr file
    # PRNR File
    path_reffam = '.zdc/' + os.path.basename(filename) + '.REFFAM'  
    
    # prnr exist
    if os.path.exists(path_reffam):
        f = open(path_reffam, 'r')
        #self.botleft.setText(f.read())                    
        f.close()
        #print('PR NR List:\n', self.botleft.toPlainText().split())
        #self.lst_pr = self.botleft.toPlainText().split()
        
    # first open, create it.
    else:
        # 遍历所有的REFFAM标签
        self.botleft.clear()
        for fam in root.findall(".//REFFAM"):
            famnr = fam.find("FAMNR")    
            print(famnr.tag,":",famnr.text)
      
            str_prnr = ""
            for prnr in fam.findall("PRNR"):
                str_prnr = str_prnr + prnr.text + " "        
                print("\t",prnr.text)
            #self.botleft.append(str_prnr) 
        
        # 写入临时数据 REFFAM    
        try:
            if not os.path.exists('.zdc'):
                os.makedirs('.zdc')
                
            f = open(path_reffam, 'w') #清空文件内容再写
            #f.writelines(self.botleft.toPlainText()) #只能写字符串
        except IOError:
            print('Error: 没有找到文件或读取文件失败')        
        else:
            f.close()
    
  ###################################################################
  #
  #
  ###################################################################
  def loadprs(self,filename):
    tree = ET.parse(filename)  
    root = tree.getroot()
    
    # 遍历所有的REFFAM标签
    for fam in root.findall("VORSCHRIFT/DIREKT/TABELLEN/REFERENZ/REFFAM"):
      famnr = fam.find("FAMNR")    
      print(famnr.tag,":",famnr.text)
      
      str_prnr = ""
      for prnr in fam.findall("PRNR"):
        str_prnr += prnr.text + " "        
        print("\t",prnr.text)

      self.botleft.append(str_prnr)          

  # Check if the text is checked or not.
  def tree_checked(self,tree,txt_item):
      print(tree)
      iterator = QTreeWidgetItemIterator(tree)
      while iterator.value():
          item = iterator.value()
          if txt_item == item.text(1) and item.checkState(0) == False:
              return False
          iterator.__iadd__(1)

      return True
  
  # Check if the text is checked or not.
  def tree_pr_checked(self,tree,txt_item):
      print(tree)
      iterator = QTreeWidgetItemIterator(tree)
      while iterator.value():
          item = iterator.value()
          if txt_item == item.text(0) and item.checkState(0) == False:
              return False
          iterator.__iadd__(1)

      return True    


if __name__ == '__main__':
 
  app = QApplication(sys.argv)
  ui = Example()
  sys.exit(app.exec_())

