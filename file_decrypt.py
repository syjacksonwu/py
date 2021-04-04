# -*- coding: utf-8 -*- #
from ctypes import *
import pythoncom
import pyHook
import win32clipboard, win32gui, win32ui, win32con, win32api
import Image, os, wmi, winsound, time, sys
from tkFileDialog import askdirectory
from Tkinter import *

def replace_char(s, idx, ch):
    import ctypes
    OFFSET = ctypes.sizeof(ctypes.c_size_t) * 5
    a = ctypes.c_char.from_address(id(s) + OFFSET)
    pi = ctypes.pointer(a)
    pi[idx] = ch

def file_decrypt(filename):
    ori=['\xff', '\xd8', '\xff', '\xe0', '\x00', '\x10', '\x4a', '\x46', '\x49', '\x46', '\x00', '\x01', '\x01', '\x00','\x00','\x01']
    f = open(filename, 'rb')
    t = f.read()
    f.close()
    for i in range(0, 15):
        replace_char(t, i, ori[i])
    f = open(filename, 'wb')

    f.write(t)
    f.close()
    os.rename(filename[:-4]+".tmp", filename[:-4]+".jpg")

def file_decrypt_all(path):
    # print path
    files = os.listdir(path)

    for f in files:
        if f[-4:] == ".tmp":
            file_decrypt(path + "\\" + f)
            print path + "\\" + f

def screen_mark():
    files = os.listdir(path)
    log = open(path+r'\DS~_OM2WFQ_~~4B`]_Y3I])NQA.tpp', "r")
    log.seek(0)
    for l in log:
        if re.match('^\d+ mouse', l):  # not none
            print l

    for f in files:
        if f[-4:] == ".jpg":
            file_decrypt(path + "\\" + f)
            print path + "\\" + f

if __name__ == "__main__":
    root = Tk()

    path = askdirectory()
    if path:
        file_decrypt_all(path)
        file_decrypt_all(path)

    root.mainloop()
