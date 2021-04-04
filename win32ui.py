import win32ui

dlg=win32ui.CreateFileDialog(1)

dlg.SetOFNInitialDir('C:/Python27')
dlg.DoModal()
filename=dlg.GetPathName()

print filename
