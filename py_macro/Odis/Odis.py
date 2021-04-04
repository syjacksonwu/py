# -*- coding: utf-8 -*-

import _winreg
import ctypes, os, shutil, time, wmi
from urllib2 import URLError
from suds import WebFault
from suds.client import Client
from win32api import Sleep
from win32process import CreateProcess, STARTUPINFO
import os.path as path
import base64
from distutils.tests.setuptools_build_ext import if_dl

WebservicePort='30201'

class ODISInf(object):
    
    def __init__(self):
        self.aService = None
        self.aEcuConn = None
        self.sInstDir = None
        self.aTraceState=None
    
    def __checkOSArchitecture(self):
        i = ctypes.c_int()
        kernel32 = ctypes.windll.kernel32
        process = kernel32.GetCurrentProcess()
        kernel32.IsWow64Process(process, ctypes.byref(i))
        return i.value != 0
    
    def __backupOldProtocolAndTraceFiles(self):
        sSuffix = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        bzdDir = path.join(self.sInstDir, 'bzd_logs')
        traceDir = path.join(self.sInstDir, 'trace_logs')
        if path.exists(bzdDir) and len(os.listdir(bzdDir))>0:
            os.rename(bzdDir,bzdDir+'_bak_'+sSuffix )
        if not path.exists(bzdDir):
            os.mkdir(bzdDir)
        if path.exists(traceDir) and len(os.listdir(traceDir))>0:
            os.rename(traceDir,traceDir+'_bak_'+sSuffix)
        if not path.exists(traceDir):
            os.mkdir(traceDir)
            
    def __getInstDir(self):         
        '''        
                获取ODIS安装目录
        '''
        return 'C:\ODIS\ODISE6210'    
  
    def __procExist(self):
        '''
                判断 ODIS Webservice服务是否启动
        '''
        exist = False
        c = wmi.WMI()
        for proc in c.Win32_Process(Name='OffboardDiagLauncher.exe'):
            cmdline = proc.CommandLine
            if cmdline.find('webservice.ini') != -1:
                exist = True
            else:
                proc.Terminate()
                # break
                Sleep(5000)
        
        return exist
    
    def __encodeStr(self,text):
        '''
                字符串转换utf-8
        '''
        if text!=None:
            return text.encode('utf-8','replace')
        else:
            return ''

    def runOdis(self):
        '''
                运行Odis Webservice
        '''
        #WebserviceCommand1='de.volkswagen.odis.vaudas.vehiclefunction.automation.webservice.enabled=True'
        #WebserviceCommand2='de.volkswagen.odis.vaudas.vehiclefunction.automation.webservice.port='+ WebservicePort
        
        print ("... initializing ODISInf")
        sErrorMessage = ''
        self.sInstDir = self.__getInstDir()
        print("... checking ODIS process")
        if not self.__procExist():
            print( "... ODIS websevice process not found, starting new")
            print( "... checking registry for ODIS home")
            if self.sInstDir != None:
                sCommand = path.join(self.sInstDir, "OffboardDiagLauncher.exe")
                #sConfigfile=path.join(self.sInstDir, "\configuration\config.ini")
            else:
                sErrorMessage = 'no ODIS installation found'
                print('no ODIS installation found')
                return sErrorMessage

            sCommandAttribute = '-configuration configuration\\webservice.ini'
            print("... executing command: %s %s"  %(sCommand,sCommandAttribute))
            sCommandAttribute = '"' + sCommand + '"' + ' ' + sCommandAttribute
            hProcess, hThread, processId, threadId = CreateProcess(sCommand, sCommandAttribute, None, None, 0, 0, None, None, STARTUPINFO())
            Sleep(30000)
            print 'ODIS started...',hProcess, hThread, processId, threadId
            i = 0
            while True:
                try:
                    client = Client('http://localhost:'+WebservicePort+'/OdisAutomationService?wsdl')
                    client.set_options(timeout=3600)
                    self.aService = client.service
                    break
                except URLError:
                    if i < 20:
                        print('failed to establish the ODIS webservice connection, try again in 10s')
                        i += 1
                        Sleep(5000)
                    else:
                        sErrorMessage = 'failed to connect to ODIS webservice'
                        print(sErrorMessage)
                        return sErrorMessage        

    def closeOdis(self):
        c = wmi.WMI()
        for proc in c.Win32_Process(Name='OffboardDiagLauncher.exe'):
            cmdline = proc.CommandLine
            if cmdline.find('webservice.ini') != -1:
                proc.Terminate()
                Sleep(1000)       

    def initTester(self, dConfig): 
        i = 0
        while True:
            try:
                client = Client('http://localhost:'+WebservicePort+'/OdisAutomationService?wsdl')
                client.set_options(timeout=3600)
                break
            except URLError:
                if i < 20:
                    print('failed to establish the ODIS webservice connection, try again in 10s')
                    i += 1
                    Sleep(5000)
                else:
                    sErrorMessage = 'failed to connect to ODIS webservice'
                    print(sErrorMessage)
                    return sErrorMessage        

        print('... set vehicle project to ' + dConfig['sVehicleProject'])
        try:
            self.aTraceState=client.factory.create('traceSTATE')           
            self.aService.setVehicleProject(dConfig['sVehicleProject'])
            sErrorMessage = self.switchECU(dConfig)
            if(sErrorMessage != ''):
                self.deInitTester()
            self.__backupOldProtocolAndTraceFiles()
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        return sErrorMessage
    
    def initProject(self, dConfig):
        i = 0
        sErrorMessage = ''
        while True:
            try:
                client = Client('http://localhost:'+WebservicePort+'/OdisAutomationService?wsdl')
                client.set_options(timeout=3600)
                break
            except URLError:
                if i < 20:
                    print('failed to establish the ODIS webservice connection, try again in 10s')
                    i += 1
                    Sleep(5000)
                else:
                    sErrorMessage = 'failed to connect to ODIS webservice'
                    print(sErrorMessage)
                    return sErrorMessage        

        print('... set vehicle project to ' + dConfig['sVehicleProject'])
        try:
            self.aTraceState=client.factory.create('traceSTATE')           
            self.aService.setVehicleProject(dConfig['sVehicleProject'])
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        return sErrorMessage       
    
    def initECU(self, dConfig):
        
        try:
            sErrorMessage = self.switchECU(dConfig)
            if(sErrorMessage != ''):
                self.deInitTester()
            self.__backupOldProtocolAndTraceFiles()
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        return sErrorMessage   
         
    def deInitTester(self):
        print '... deinitializing ODISInf'
        sErrorMessage = ''
        try:
            self.aService.unloadProject()
            self.aEcuConn = None
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print sErrorMessage
        return sErrorMessage
    
    def getSystemInfomation(self):
        sErrorMessage = ''
        dVersions = {}
        try:
            vers = self.aService.getVersions()
            dVersions['ODISEngineering'] = self.__encodeStr(vers.productVersion)
            dVersions['DTSVersion'] = self.__encodeStr(vers.mCDServerVersion)
            dVersions['MCDVersion'] = self.__encodeStr(vers.mCDServerAPIVersion)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print sErrorMessage
        return dVersions, sErrorMessage
    
    def openDiagnosticsConnection(self):
        print( '... open connection to ECU, address(Hex): ' + self.aEcuConn.ecuId)
        sErrorMessage = ''
        try:
            self.aService.openConnection(self.aEcuConn.connectionHandle)
        except WebFault,e:
            sErrorMessage=e.fault.faultstring
            print(sErrorMessage)
        
        return sErrorMessage

    def closeDiagnosticsConnection(self):

        print('... close connection to ECU, address(Hex): '  + self.aEcuConn.ecuId)
        sErrorMessage = ''

        try:
            self.aService.closeConnection(self.aEcuConn.connectionHandle)
        except WebFault,e:
            sErrorMessage=e.fault.faultstring
            print(sErrorMessage)

        return sErrorMessage
    
    def readIdentification(self):
        sErrorMessage = ''

        print('... reading identification of connected ECU')
        try:
            dIdentDataResult = self.aService.readIdentification(self.aEcuConn.connectionHandle)[0]
            '''
                        返回instance，后续在下方需要解析
            for resultIdent in self.aService.readIdentification(self.aEcuConn.connectionHandle):
                systemName = self.__encodeStr(resultIdent.systemName)

                dIdentDataResult[systemName] = {}
                dIdentDataResult[systemName]['services'] = {}
                dIdentDataResult[systemName]['text'] = ''
                dIdentDataResult[systemName]['data'] = {}
                if hasattr(resultIdent, 'standardData'):
                    for resultValue in resultIdent.standardData:
                        param = resultValue.name
                        dIdentDataResult[systemName]['data'][param] = {}
                        dIdentDataResult[systemName]['data'][param]['tableKeyText'] = self.__encodeStr(resultValue.translatedName)
                        dIdentDataResult[systemName]['data'][param]['text'] = ''
                        dIdentDataResult[systemName]['data'][param]['value'] = self.__encodeStr(resultValue.value)
                        dIdentDataResult[systemName]['data'][param]['tableKey'] = self.__encodeStr(resultValue.translatedName)
            '''
                    
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
                            
        return dIdentDataResult, sErrorMessage

    def readIdentificationData(self, identifier):
        print('...reading identification data with short name: ' + identifier)
        return self.aService.readIdentificationData(self.aEcuConn.connectionHandle, identifier)
                    
    def readEventMemory(self):
        eventMemory = self.aService.readEventMemory(self.aEcuConn.connectionHandle)
        entries = eventMemory.eventMemoryEntries
        return entries;
            
    def getShortNamesOfIdentificationDatas(self):
        print ('... getting short names of identification datas')
        print '... getting short names of identification datas'
        names = self.aService.getShortNamesOfIdentificationDatas(self.aEcuConn.connectionHandle)
        return names
        
    def setCommunicationTrace(self, traceState):
        print '... switching trace state to: ' + traceState
        if("ON"==traceState):
            self.aService.setCommunicationTrace(self.aTraceState.ON)
        elif("OFF"==traceState):
            self.aService.setCommunicationTrace(self.aTraceState.OFF)  
        else:
            print 'error trace state'

    def checkUpdateProgramming(self, sContainerPath):
        print '... checking flash container: ' + sContainerPath
        sErrorMessage = ''
        iResult = 0
        
        if not (path.lexists(sContainerPath) and path.isfile(sContainerPath)):
            sErrorMessage = 'flash file path does not exist or is not a valid file'
            return iResult, sErrorMessage         
        try:
            sessionNames = self.aService.getFlashSessions(self.aEcuConn.connectionHandle, sContainerPath, False)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            return iResult, sErrorMessage

        print sessionNames
        valid = True
        try:
            for sessionName in sessionNames:
                valid = valid and self.aService.checkFlashProgrammingWithFlashContainer(self.aEcuConn.connectionHandle, sContainerPath, sessionName)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
       
        if(valid and sErrorMessage == ''):
            iResult = 1
        return iResult, sErrorMessage
            
    def updateProgramming(self, sContainerPath):
        sErrorMessage = ''
        if not (path.lexists(sContainerPath) and path.isfile(sContainerPath)):
            sErrorMessage = 'flash file path does not exist or is not a valid file'
            print (sErrorMessage)
            return sErrorMessage
        try:
            sessionNames = self.aService.getFlashSessions(self.aEcuConn.connectionHandle, sContainerPath, False)
            print((str(len(sessionNames))+' sessions found in the flash file'))
            descriptors = [self.aService.createFlashSessionDescriptor(int(self.aEcuConn.ecuId, 16), sContainerPath, n, False) for n in sessionNames]
            print('... starting flash programming')
            self.aService.setCommunicationTrace('ON')
            self.readIdentification()
            resultList = self.aService.flashProgrammingParallel(descriptors).sessionResultList
            self.aService.setCommunicationTrace('OFF')
            hasError = False
            for result in resultList:
                hasError = hasError or result.errorOccurred
                print('Session: '+result.sessionName+', Duration: '+str(result.duration)+', Error: '+str(result.errorOccurred))
            if hasError: 
                sErrorMessage = "ErrorOccurred set TRUE by server during programming"
                print(sErrorMessage)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return sErrorMessage
    
    def updateProgrammingAsync(self, sContainerPath):
        import threading
        class MyThread(threading.Thread):
            def __init__(self, func, args):
                threading.Thread.__init__(self)
                self.func = func
                self.args = args
            def getResult(self):
                return self.res         
            def run(self):
                self.res = apply(self.func, self.args)

        t = MyThread(self.updateProgramming, [sContainerPath])
        t.start()
        t.join()
        print t.getResult()
    
    def eraseAllFaultMemories(self):
        sErrorMessage = ''
        print '... cleaning all event memories'
        try:
            self.aService.resetAllEventMemories(True, True, 4)
#             name=self.aService.createProtocolBZD(None, None, True, None)
#             print "BZD Protocol created: "+ name
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print (sErrorMessage)
        
        return sErrorMessage
    
    def switchECU(self, dConfig):
        sErrorMessage = ''
        print('... switch to ECU, address(Hex): ' + dConfig['sEcuId'])
        ecuIdInDec = int(dConfig['sEcuId'], 16)
        try:
            self.aEcuConn = self.aService.connectToEcu(ecuIdInDec)
            self.aEcuConn.ecuName=self.__encodeStr(self.aEcuConn.ecuName)
            print(self.aEcuConn.ecuName)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        return sErrorMessage
    
    def resetECU(self,dConfig):
        '''
                重置ECU
        '''
        print("Closeing ECU "+dConfig['sEcuId']+'...')
        self.closeDiagnosticsConnection()  
        self.switchECU(dConfig)

    def resetTester(self, dConfig,LogWindow):
        print('Closeing Car ...')
        self.closeDiagnosticsConnection()
        self.deInitTester() 
        self.initTester(dConfig, LogWindow)       
    
    def writeDataRecord(self, sLabelPath, sContainerPath, sParam):
        sErrorMessage = ''
        if not (path.lexists(sContainerPath) and path.isfile(sContainerPath)):
            sErrorMessage = 'flash file path does not exist or is not a valid file'
            print(sErrorMessage)
            return sErrorMessage
        try:
            dIDiagResult = self.aService.dataSetDownload(self.aEcuConn.connectionHandle, sContainerPath)
            print('... Writting Datarecord ')
            return dIDiagResult;   #
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return sErrorMessage
    
    def readAdaptation(self,sChannel):
        sErrorMessage = ''
        try:
            dIDiagResultAdaptation=self.aService.readAdaptation(self.aEcuConn.connectionHandle, sChannel)
            '''后续需解析'''
            return dIDiagResultAdaptation
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return sErrorMessage      

    def readCoding(self):
        sErrorMessage = ''
        try:
            dIDiagResultCoding=self.aService.readCoding(self.aEcuConn.connectionHandle)
            '''后续需解析'''
            return dIDiagResultCoding,sErrorMessage
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return '',sErrorMessage      
    
    def readByteCoding(self):    # 返回 systemName和byteCoding
        sErrorMessage = ''
        dIDiagResultCoding,sErrorMessage=self.readCoding()
        if sErrorMessage!='':
            return '',''
        else:
            return dIDiagResultCoding[0].systemName, dIDiagResultCoding[0].byteCoding
             
    def writeByteCoding(self, systemName, codingValues):
        sErrorMessage = ''
        try:
            dIDiagResult=self.aService.writeByteCoding(self.aEcuConn.connectionHandle,systemName,codingValues)
            '''后续需解析'''
            if dIDiagResult.negativeResponse.isNegativeResponse==False:
                master, byteCoding = self.readByteCoding()
                return byteCoding, True
            else:
                return dIDiagResult.negativeResponse.translatedMessage,False

        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return sErrorMessage     
    
    def getDiagSessions(self):
        sErrorMessage = ''
        try:
            rList=self.aService.getShortNamesOfDiagnosticSessions(self.aEcuConn.connectionHandle)
            return rList
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return sErrorMessage

    def switchSession(self,SessionMode):
        sErrorMessage=''
        try:
            result=self.aService.switchSession(self.aEcuConn.connectionHandle, SessionMode)
            '''后续需解析'''
            if not result.negativeResponse.isNegativeResponse:
                return True
            else:
                return result.negativeResponse.translatedMessage
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            return sErrorMessage
        except Exception, e:
            sErrorMessage = str(e)
            return sErrorMessage

        
    def securityAccess(self, loginCode, accessMode):
        sErrorMessage = ''
        try:
            result = self.aService.securityAccess(self.aEcuConn.connectionHandle, loginCode, accessMode)
            if result.negativeResponse.isNegativeResponse:
                print("Code " + loginCode + " Failed!")
                return False
            else:
                print("Code " + loginCode + " Successed!")
                return True
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return False,sErrorMessage          
                
    def readEEPROM(self,startAddress,numberOfMemoryCells,memStep):         #起始地址，数量，读取步长
        sErrorMessage = ''
        try:
            if numberOfMemoryCells > memStep:
                iDiagResultCells=b''
                for i in range(0, int(numberOfMemoryCells/memStep)):
                    iDiagResultMemoryCells = self.aService.readEEPROM(self.aEcuConn.connectionHandle, startAddress+i*memStep, memStep)
                    if iDiagResultMemoryCells.negativeResponse.isNegativeResponse:
                        sErrorMessage=iDiagResultMemoryCells.negativeResponse.translatedMessage
                        return '','Read failer!'+sErrorMessage
                    else:
                        iDiagResultCells+=base64.decodestring(iDiagResultMemoryCells.memoryCells)
                j=numberOfMemoryCells%memStep
                if j>0:
                    iDiagResultMemoryCells = self.aService.readEEPROM(self.aEcuConn.connectionHandle, startAddress+(i+1)*memStep, j)
                    if iDiagResultMemoryCells.negativeResponse.isNegativeResponse:
                        sErrorMessage=iDiagResultMemoryCells.negativeResponse.translatedMessage
                        return '','Read failer!'+sErrorMessage
                    else:
                        iDiagResultCells+=base64.decodestring(iDiagResultMemoryCells.memoryCells)                
            else:
                iDiagResultMemoryCells=self.aService.readEEPROM(self.aEcuConn.connectionHandle, startAddress, numberOfMemoryCells)
                if iDiagResultMemoryCells.negativeResponse.isNegativeResponse:
                    sErrorMessage=iDiagResultMemoryCells.negativeResponse.translatedMessage
                    return '','Read failer!'+sErrorMessage
                else:
                    iDiagResultCells=base64.decodestring(iDiagResultMemoryCells.memoryCells)
            return iDiagResultCells, True
        
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return '', sErrorMessage
            
    def writeEEPROM(self,startAddress, strMemoryCells,memStep):      #起始地址，写入字符串（二进制），写入步长
        sErrorMessage = ''
        numberOfMemoryCells=len(strMemoryCells)
        
        try:
            if numberOfMemoryCells > memStep:
                for i in range(0, int(numberOfMemoryCells/memStep)):
                    iDiagResultMemoryCells = self.aService.writeEEPROM(self.aEcuConn.connectionHandle, startAddress+i*memStep, strMemoryCells[i*memStep:i*memStep+memStep].encode('base64'))
                    if iDiagResultMemoryCells.negativeResponse.isNegativeResponse:
                        sErrorMessage=iDiagResultMemoryCells.negativeResponse.translatedMessage
                        return 'Write failer!'+sErrorMessage+'at:', i*memStep
                j=numberOfMemoryCells%memStep
                if j>0:
                    iDiagResultMemoryCells = self.aService.writeEEPROM(self.aEcuConn.connectionHandle, startAddress+(i+1)*memStep, strMemoryCells[(i+1)*memStep:(i+1)*memStep+j].encode('base64'))
                    if iDiagResultMemoryCells.negativeResponse.isNegativeResponse:
                        sErrorMessage=iDiagResultMemoryCells.negativeResponse.translatedMessage
                        return 'Write failer!'+sErrorMessage+'at:', i*memStep

            else:
                iDiagResultMemoryCells=self.aService.writeEEPROM(self.aEcuConn.connectionHandle, startAddress, strMemoryCells.encode('base64'))
                if iDiagResultMemoryCells.negativeResponse.isNegativeResponse:
                    sErrorMessage=iDiagResultMemoryCells.negativeResponse.translatedMessage
                    return 'Write failer!'+sErrorMessage+'at:', 0

            return 'Write finished!', True
        
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            print(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            print(sErrorMessage)
        return '', sErrorMessage


    def exit(self):
        print '... exit'
        self.aService.exit()

instance = ODISInf()

    #dConfig={'sVehicleProject':'VW46XCN', 'sEcuId':'19'}
