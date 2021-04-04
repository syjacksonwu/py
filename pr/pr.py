# from Tkinter import *
#from tkFileDialog import *
from ttk import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from FileDialog import *
import xml.etree.ElementTree as ET
# import re

root = Tk()
tree = None
troot = None
FileName = None

r = 0
r0 = 0
c = 0
var = []
lst_lbl = []  # list for Entry
lst_ent = []
lst = []

def save_to_file():
    s_name = asksaveasfilename(filetypes=[("text","*.txt")])
    print s_name
    if s_name:
        ofp=open(s_name+'.txt','w')
        ofp.write(pr_list.get())
        ofp.flush()
        ofp.close()

def combination_pr():
    global pr_list
    global var
    ss = ''
    for e in var:
        if e.get():
            if(ss == ''):
                ss = e.get().split(' ')[0]
            else:
                ss = ss + ', ' + e.get().split(' ')[0]

    print ss
    pr_list.set(ss)

def select_change(event):
    #print '---------'
    #print event.widget.get()
    combination_pr()

def LoadZDC(tree,troot):
    global r
    global r0
    global c
    global var
    global lst_lbl #list for Entry
    global lst_ent
    global lst
    global pr_list

    # Load pr list
    file_path="./pr.xml"
    pr_tree = ET.ElementTree()
    pr_tree.parse(file_path)
    pr_root = pr_tree.getroot()


    # Search each FAM.
    for i_fam in troot.iter('REFFAM'):
        str_fam = i_fam.find('FAMNR').text

        # Get fam description for str_fam
        sv_fam_des = StringVar()
        for i_pr in pr_root.findall('fam'):
            if i_pr.get('name') == str_fam:
                #sv_fam_des.set(i_pr.get('des_de'))
                sv_fam_des.set(i_pr.get(lan_typ))
                break

        v = StringVar()
        v.set('')
        var.append(v)
        combo_current_value = StringVar()
        combo_list_value = []
        # print(v.get())

        #  lable
        lbl = Label(root, text=str_fam, borderwidth=1)
        lbl.grid(row=r,column=c)
        # print(lbl['text'])

        #Entery
        ent = Entry(root, textvariable=sv_fam_des, width=50, bg='yellow')
        # print(ent)
        c=c+1
        ent.grid(row=r, column=c)

        #append into list.
        lst_lbl.append(lbl)
        lst_ent.append(v)
        lst.append([lbl, v, combo_current_value])

        pr_des = ""
        for pr_nr in i_fam.iter('PRNR'):
            pr_des = ""
            for i_pr in pr_root.iter('pr'):
                if i_pr.get('name') == pr_nr.text:
                    #pr_des = i_pr.get('des_de')
                    pr_des = i_pr.get(lan_typ)
                    break

            combo_list_value.append(pr_nr.text + " " + pr_des)

        c += 1
        box = Combobox(root, textvariable=v, value=combo_list_value, width=80)
        box.bind('<<ComboboxSelected>>', select_change)
        box.grid(row=r, column=c)

        r += 1  # Next row
        c = 0   # Reset column

    r += 1  # Next row
    c = 0   # Reset column

    # Below is output of PR list.
    lbl = Label(root, text="PR List", borderwidth=1).grid(row=r, sticky=W)  # arrangement to left
    ent = Entry(root, width=100, textvariable=pr_list).grid(row=r, column=1, columnspan=30, sticky=W)

    r += 1  # Next row
    b1 = Button(root, text='Save', command=save_to_file).grid(row=r)

def PrnrIsValid(prnrs):
# PrnrIsValid: Check if this prnr line is inside the order.
    # L0L+1ZF/1ZE/1ZP
    print('this pr. nr. is valid')
    return True

def OpenFile():
    #File_Path="C:\ZDC\BCM.xml"
    global tree
    global troot
    global FileName

    #if(path == None):
    File_Path = askopenfilename()

    tree = ET.parse(File_Path)
    troot=tree.getroot()
    LoadZDC(tree,troot)

def choose_language_de():
    global lan_typ
    lan_typ = 'des_de'

def choose_language_cn():
    global lan_typ
    lan_typ = 'des_cn'

if __name__ == '__main__' :
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=OpenFile)
    menubar.add_cascade(label="File", menu=filemenu)

    menu_language = Menu(menubar, tearoff=0)
    menu_language.add_command(label="des_de", command=choose_language_de)
    menu_language.add_command(label="des_cn", command=choose_language_cn)
    menubar.add_cascade(label="Language", menu=menu_language)

    root.config(menu=menubar)
    lan_typ = 'des_de'
    var = []
    s = StringVar()
    pr_list = StringVar()

    root.mainloop()
