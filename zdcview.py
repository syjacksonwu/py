import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QListWidget, QTreeWidgetItem, \
                            QTreeWidget, QFileDialog, QHBoxLayout, \
                            QVBoxLayout, QFrame, QSplitter,QLineEdit, \
                            QPushButton, QTreeWidgetItemIterator,QMenu,QAction)
from PyQt5.QtCore import Qt, QUrl
#from PyQt5.QtGui import QPainter, QColor, QBrush,QCursor
from PyQt5.QtGui import *
#from PyQt5.QtWebEngineWidgets import QWebEngineView
import xml.etree.ElementTree as ET
from lxml import etree
from Ui_zdc import Ui_MainWindow


class Example(QMainWindow,Ui_MainWindow):
    
    def __init__(self):
        super(Example,self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.flag_org_pr = False

    def closeEvent(self, event):
        print(event)
        sys.exit(0)

    def init_ui(self):
        ''' 关联处理函数 '''

        self.openMenu.triggered.connect(self.open_zdc)
        self.btn_Update_Tree.clicked.connect(self.update_tab)
        self.btn_Update_PrNr.clicked.connect(self.update_pr)
        self.btn_Dump_pr.clicked.connect(self.dump_prnr)
        self.btn_Inject_pr.clicked.connect(self.inject_prnr)
        self.btn_Find.clicked.connect(self.on_btn_Find)

        self.cb_Tabelle.stateChanged.connect(self.on_QCheckBox_Tabelle_Change)
        self.cb_PR.stateChanged.connect(self.on_QCheckBox_PR_Change)

        # Tabbele树
        self.midleft.setColumnCount(3)   # 设置部件的列数为2
        self.midleft.setDropIndicatorShown(True)
        self.midleft.setHeaderLabels(['TAB','DID', 'Teil', 'Desc','Data'])  # 设置头部信息对应列的标识符
        self.midleft.setSortingEnabled(True)
        self.midleft.setColumnWidth(0,60)
        self.midleft.setColumnWidth(1,40)

        # 右键菜单
        self.midleft.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        self.midleft.customContextMenuRequested.connect(self.tree_tab_menu)  # 绑定事件
        self.pop_menu = QMenu()
        self.pop_menu.addAction(QAction(u'计算', self))
        self.pop_menu.addAction(QAction(u'导出', self))
        self.pop_menu.triggered.connect(self.processtrigger)

        # PRNR树
        self.botleft.setColumnCount(2)  # 设置部件的列数为2
        self.botleft.setDropIndicatorShown(True)
        self.botleft.setHeaderLabels(['FAM', 'PR'])  # 设置头部信息对应列的标识符
        self.botleft.itemChanged.connect(self.tree_pr_changed)

        ##################

        # Windows - ZDC view
        self.filename = "C:/Users/WuJianjian/.spyder-py3/V003002118DA__6C0959655Q__AIRBAG.xml"
        #self.load_zdc(self.filename)
        #self.orig_tree_tab()
        #self.orig_tree_pr()

        #self.setGeometry(600, 600, 600, 400)
        #self.setWindowTitle('ZDC-Browser, beta-1, by wujianjian')
        #self.show()

    ###########################################
    def orig_tree_tab(self):
        ''' Show Original tabelles '''

        tree = ET.parse(self.filename) #etree
        root = tree.getroot()

        tabelles = root.findall(".//TABELLE")

        # # Make a tree from Orignial ZDC
        self.midleft.clear()
        # 设置root为self.tree的子树，故root是根节点
        #tr_root = QTreeWidgetItem(self.midleft)
        #tr_root.setText(0, 'ZDC')  # 设置根节点的名称

        # 为root节点设置子结点
        # 提取Coding,Anpassung表
        print("Loading Tabelles: Coding, Anpassung, Datasets:")
        for tab in tabelles:
            print(tab.find("MODUSTEIL").text)

            child = QTreeWidgetItem(self.midleft)
            child.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)

            #加载类型
            child.setText(0, tab.find("MODUS").text)

            #加载DID
            if tab.find("RDIDENTIFIER") is not None:
                child.setText(1, tab.find("RDIDENTIFIER").text)

            child.setText(2, tab.find("MODUSTEIL").text)

            #加载描述
            if tab.find("BESCHREIBUNG") is not None:
                child.setText(3, tab.find("BESCHREIBUNG").text)
            
            child.setCheckState(0, Qt.Checked)

        # 提取参数表,DATENBEREICH
        #print("Loading ")
        #for datenbereich in root.findall(".//DATENBEREICH"):
        #    print(datenbereich.find("DATEN-NAME").text)

        self.midleft.expandAll()


    #######################

    def orig_tree_pr(self):
        ''' Get PrNr list from orignal ZDC FILE '''

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
            print(famnr.text, ":")

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

        self.botleft.expandAll()
        self.flag_org_pr = True # 完成初始pr 树建立

    #################################

    def update_tab(self):
        '''Update WebView by Tab-Tree '''

        if not os.path.exists(self.filename):
            print(self.filename + ' Not Exsit.')
            return

        tree = ET.parse(self.filename)
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


    ##############################################
    def update_pr(self): 
        ''' Update WebView by Pr-Tree '''

        if not os.path.exists(self.filename+'.tmp.xml'):
            print(self.filename+'.tmp.xml' + ' Not Exsit.')
            return

        tree = ET.parse(self.filename+'.tmp.xml')  
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

    def open_zdc(self):
        ''' 通过对话框，打开一个ZDC文件'''

        self.filename, _ = QFileDialog.getOpenFileName(self,'选择文件','','ZDC files(*.xml)')

        if self.filename:
            self.flag_org_pr = False

            #self.topleft.addItem(self.filename)
            #self.load_zdc(self.filename)
            #self.loadprs(self.filename)      
            self.load_zdc(self.filename)
            self.orig_tree_tab()
            self.orig_tree_pr()
            #self.cb_Tabelle.setChecked(True)
            #self.cb_PR.setChecked(True)

    def orgzdc(self):
        if self.filename:
            self.topright.load(QUrl("file:///" + self.filename)) # webview

    #################################

    def tree_tab_Changed(self, item, column):
        '''
        # Tab-Tree Changed
        #当check状态改变时得到他的状态。
        '''

        if item.checkState(column) == Qt.Checked:
            print("checked", item.text(1))

        if item.checkState(column) == Qt.Unchecked:
            print("unchecked", item.text(1))

    def tree_tab_menu(self,pos):
        item=self.midleft.currentItem()
        item1= self.midleft.itemAt(pos)

        if item!=None and item1!=None:
            self.pop_menu.exec_(QCursor.pos())


    def prnr_in_order(self, prnr):
        ''' 检查pr号是否在订单里面'''

        #for item in self.textEdit.toPlainText().split('+'):
        for pr in prnr.split('+'):
            print(pr)
            if '/' in pr:
                for sub_pr in pr.split('/'):
                    if sub_pr in self.textEdit.toPlainText():
                        return True
            else:
                return pr in self.textEdit.toPlainText()

        return False

    def processtrigger(self, q):
        '''#判断是项目节点还是任务节点'''

        command=q.text()
        item=self.midleft.currentItem()
        str_teil=item.text(2) #MODUSTEIL

        if command=="计算":
            self.pop_menu.close()

            # 提取所有表
            root = self.tree.getroot()
            tabelles = root.findall(".//TABELLE")
            # 查找对应的表格
            for tabelle in tabelles:
                if tabelle.find("MODUSTEIL").text == str_teil:

                    # 是参数吗？
                    if item.text(0) == 'P':
                        # 检查所有TEGUE
                        #for tegue in tabelle.findall(".//TAB//FAM//TEGUE"):
                            # 有效PR号？

                        # 有效参数
                        if tabelle.findall(".//TAB//FAM//TEGUE//KNOTEN//DATEN-NAME"):
                            for daten in tabelle.findall(".//TAB//FAM//TEGUE//KNOTEN//DATEN-NAME"):
                                print(daten.text)
                                item.setText(4, daten.text)
                        # 无效参数
                        else:
                            print("N/A")
                            item.setText(4, "N/A")

                    # 是编码和匹配吗？
                    if item.text(0) == 'K':
                        list_coding = [] # 初始编码

                        # 遍历每个字节
                        #kopf = tabelle.find("KOPF")
                        for zde in tabelle.findall(".//KOPF//ZDE"):
                            zdstelle=zde.find("ZDSTELLE").text # Byte

                            value_byte = 0
                            for zdbyte in zde.findall("ZDBYTE"): # Bit
                                #zmsb=zdbyte.find("ZMSB").text
                                zlsb=zdbyte.find("ZLSB").text

                                #寻找TEGUE->KNOTEN->WERT
                                for tegue in tabelle.findall(".//TAB//FAM//TEGUE"):

                                    print(tegue.find(".//PRNR").text)
                                    # prnr在订单里面吗？
                                    if self.prnr_in_order(tegue.find(".//PRNR").text):
                                        for knoten in tegue.findall(".//KNOTEN"):
                                            if knoten.find("STELLE").text == zdstelle: #Byte
                                                if knoten.find("LSB").text == zlsb: #Bit
                                                    wert = knoten.find("WERT").text
                                                    break

                                        value_byte = value_byte + int(wert,16)*(2**int(zlsb,16))
                                        #print("%s %s %s %s" %(zdstelle, zmsb, zlsb, wert))
                                        print("%s %02X" %(zdstelle, value_byte))
                                        list_coding.append(value_byte)

                        # 输出计算结果
                        list_hex = ['%02X' %i for i in list_coding]

                        print("%s: %s" %(str_teil," ".join(list_hex)))
                        item.setText(4, " ".join(list_hex))
                        break



        if command=="导出":
            self.pop_menu.close()
            print(item.text(3))

            file_name=""
            root = self.tree.getroot()
            for tabelle in root.findall(".//TABELLE"):
                if tabelle.find("MODUSTEIL").text == str_teil:
                    # 是参数吗？
                    if item.text(0) == 'P':
                        # 有效参数
                        if tabelle.findall(".//TAB//FAM//TEGUE//KNOTEN//DATEN-NAME"):
                            for daten in tabelle.findall(".//TAB//FAM//TEGUE//KNOTEN//DATEN-NAME"):
                                # 参数名称
                                print(daten.text)
                                file_name = daten.text

                                # 保存的文件路径
                                file_path, _ = QFileDialog.getSaveFileName(self,
                                    "Save File",file_name,"All Files(*);;XML Files(*.xml);;Text Files(*.txt)")

                                if file_path:
                                    file_out=open(file_path, 'w')

                                    for datenbereich in root.findall(".//DATENBEREICHE//DATENBEREICH"):
                                        if datenbereich.find("DATEN-NAME").text == file_name:
                                            if datenbereich.findall(".//DATEN"):  # 参数数据
                                                for xml_daten in datenbereich.findall(".//DATEN"):
                                                    print(xml_daten.text)
                                                    file_out.write(xml_daten.text)
                                                    file_out.close()
                                                    break
                                            break
                        # 无效参数
                        else:
                            print("N/A")
                            item.setText(4, "N/A")

                    # 是编码和匹配吗？
                    if item.text(0) == 'K':
                        list_coding = [] # 初始编码






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


    ##############################################

    def tree_pr_changed(self, item, column):
        ''' Pr-Tree Changed 当check状态改变时得到他的状态。'''

        # 初始PR树已经完成？
        if self.flag_org_pr :
            # 是Family?
            if item.childCount()>0 :
                if item.checkState(column) == Qt.Checked:
                    print('Family %s checked' %item.text(0))
                
                if item.checkState(column) == Qt.Unchecked:
                    print("Family %s unchecked" %item.text(0))
            
            # 是PR号?
            if item.childCount()==0 :
                if item.checkState(column) == Qt.Checked:
                    print("PR %s checked" %item.text(0))
                
                if item.checkState(column) == Qt.Unchecked:
                    print("PR %s unchecked" %item.text(0))
                
                #着色
                fam=item.parent()
                count_check = 0
                for index in range(fam.childCount()):
                    if fam.child(index).checkState(column) == Qt.Checked:
                        count_check = count_check+1

                # 当一个Family中，只有一个PR号选中，着绿色
                if count_check == 1:
                    fam.setBackground(0,QColor(0,100,0))
                # 多余一个或者没有，不着色
                else:
                    fam.setBackground(0,QColor(100,100,100))
    
    #####################################
    def updatezdc(self):
        ''' Update zdc by pr list & by  '''

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
            child.setCheckState(0, Qt.Unchecked)             
            
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

    def dump_prnr(self):
        '''从PR号树中，提取PRNR订单'''

        str_prnr_order = ''
        iterator = QTreeWidgetItemIterator(self.botleft)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) and (item.childCount()==0):
                str_prnr_order += item.text(0) + ' '
            iterator.__iadd__(1)

        #去掉首尾空格或者','
        str_prnr_order = str_prnr_order.strip(' ')
        str_prnr_order = str_prnr_order.strip(',')
        self.textEdit.setPlainText(str_prnr_order)

    def inject_prnr(self):
        '''向PR号树中，注入PRNR订单'''

        str_prnr_order = self.textEdit.toPlainText()
        str_prnr_order = str_prnr_order.strip(' ')
        str_prnr_order = str_prnr_order.strip(',')

        lst_prnr_oder = []

        if len(str_prnr_order):
            str_prnr_order = str_prnr_order.upper()

            if ', ' in str_prnr_order:
                lst_prnr_oder = str_prnr_order.split(', ')
            elif ',' in str_prnr_order:
                lst_prnr_oder = str_prnr_order.split(',')
            elif ' ' in str_prnr_order:
                lst_prnr_oder = str_prnr_order.split(' ')
            elif len(str_prnr_order)==3:    #只有一个PR号
                lst_prnr_oder.append(str_prnr_order)

        if len(lst_prnr_oder):
            # 清除 PR 树中已经选中的所有项目
            iterator = QTreeWidgetItemIterator(self.botleft)
            while iterator.value():
                item = iterator.value()
                item.setCheckState(0,Qt.Unchecked)
                iterator.__iadd__(1)

            # 安装PR订单重新勾选PR树
            for pr in lst_prnr_oder:
                iterator = QTreeWidgetItemIterator(self.botleft)
                while iterator.value():
                    item = iterator.value()
                    if (item.text(0)==pr) and (item.childCount()==0):
                        item.setCheckState(0,Qt.Checked)
                        break
                    iterator.__iadd__(1)

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


    ###############################
    #
    #
    ################################
    def load_zdc(self,filename):
        ''' 加载ZDC文件 '''

        self.topright.load(QUrl("file:///" + filename)) # webview

        self.tree = ET.parse(filename)
        root = self.tree.getroot()

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
    ui.show()
    sys.exit(app.exec_())
