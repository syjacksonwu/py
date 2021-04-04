'''
Created on 2012-12-26

@author: huangjianzhong
'''
import _winreg
import ctypes, logging.config, os, shutil, time, wmi
from urllib2 import URLError
from suds import WebFault
from suds.client import Client
from win32api import Sleep
from win32process import CreateProcess, STARTUPINFO
import os.path as path


log = logging.getLogger(__name__)

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
        is64Bit = self.__checkOSArchitecture()
        r = wmi.WMI (namespace="DEFAULT").StdRegProv
        sSubKeyName = r"SOFTWARE\ej-technologies\install4j\installations"
        if (is64Bit):
            sSubKeyName = r"SOFTWARE\Wow6432Node\ej-technologies\install4j\installations"
                
        result, names, types = r.EnumValues (hDefKey=_winreg.HKEY_LOCAL_MACHINE,
                                             sSubKeyName=sSubKeyName)
        for name, type in zip(names, types):
            if(type == 1):
                result, value = r.GetStringValue(hDefKey=_winreg.HKEY_LOCAL_MACHINE,
                                    sSubKeyName=sSubKeyName,
                                    sValueName=name)
                if(name.startswith("instdir") and value.endswith('Offboard_Diagnostic_Information_System_Engineering')):
                    return value
        return None    
                  

    def __procExist(self):
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
        if text!=None:
            return text.encode('utf-8','replace')
        else:
            return ''

    def initTester(self, dConfig):
        log.debug("... initializing ODISInf")
        sErrorMessage = ''
        self.sInstDir = self.__getInstDir()
        log.debug("... checking ODIS process")      
        if not self.__procExist():
            log.debug("... ODIS websevice process not found, starting new")
            
            log.debug("... checking registry for ODIS home")
                            

            if self.sInstDir != None:
                sCommand = path.join(self.sInstDir, "OffboardDiagLauncher.exe")
            else:
                sErrorMessage = 'no ODIS installation found'
                return sErrorMessage

            sCommandAttribute = '-configuration configuration\\webservice.ini'
            log.debug("... executing command: %s %s", sCommand, sCommandAttribute)
            sCommandAttribute = '"' + sCommand + '"' + ' ' + sCommandAttribute
            hProcess, hThread, processId, threadId = CreateProcess(sCommand, sCommandAttribute, None, None, 0, 0, None, None, STARTUPINFO())
            Sleep(60000)
        
        i = 0
        while True:
            try:
                client = Client('http://localhost:8081/OdisAutomationService?wsdl')
                client.set_options(timeout=3600)
                self.aService = client.service
                
                break
            except URLError:
                if i < 20:
                    log.debug('failed to establish the ODIS webservice connection, try again in 10s')
                    i += 1
                    Sleep(5000)
                else:
                    sErrorMessage = 'failed to connect to ODIS webservice'
                    log.error(sErrorMessage)
                    return sErrorMessage
        
        log.debug('... set vehicle project to "%s"', dConfig['sVehicleProject'])
        try:
            self.aTraceState=client.factory.create('traceSTATE')           
            self.aService.setVehicleProject(dConfig['sVehicleProject'])
            sErrorMessage = self.switchECU(dConfig)
            if(sErrorMessage != ''):
                self.deInitTester()
            self.__backupOldProtocolAndTraceFiles()
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
        return sErrorMessage
    
    def deInitTester(self):
        log.debug('... deinitializing ODISInf')
        sErrorMessage = ''
        try:
            self.aService.unloadProject()
            self.aEcuConn = None
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
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
            log.error(sErrorMessage)
        return dVersions, sErrorMessage
    
    def openDiagnosticsConnection(self):
        log.debug('... open connection to ECU, address(Hex): %s', self.aEcuConn.ecuId)
        sErrorMessage = ''
        #=======================================================================
        # try:
        #     self.aService.openConnection(self.aEcuConn.connectionHandle)
        # except WebFault,e:
        #     sErrorMessage=e.fault.faultstring
        #     log.error(sErrorMessage)
        #=======================================================================
        return sErrorMessage

#######################################    
def closeDiagnosticsConnection(self):
        log.debug('... close connection to ECU, address(Hex): %s', self.aEcuConn.ecuId)
        sErrorMessage = ''
        #=======================================================================
        # try:
        #     self.aService.closeConnection(self.aEcuConn.connectionHandle)
        # except WebFault,e:
        #     sErrorMessage=e.fault.faultstring
        #     log.error(sErrorMessage)
        #=======================================================================
        return sErrorMessage
    
    def readIdentification(self):
        sErrorMessage = ''
        dIdentDataResult = {}
        log.debug('... reading identification of connected ECU')
        try:
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
                    
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            log.error(sErrorMessage)
                            
        return dIdentDataResult, sErrorMessage

    def readIdentificationData(self, identifier):
        log.debug('...reading identification data with short name: %s', identifier)
        return self.aService.readIdentificationData(self.aEcuConn.connectionHandle, identifier)
                    
    def readEventMemory(self):
        eventMemory = self.aService.readEventMemory(self.aEcuConn.connectionHandle)
        entries = eventMemory.eventMemoryEntries
        return entries;
            
    def getShortNamesOfIdentificationDatas(self):
        log.debug('... getting short names of identification datas')
        names = self.aService.getShortNamesOfIdentificationDatas(self.aEcuConn.connectionHandle)
        return names
        
    def setCommunicationTrace(self, traceState):
        log.debug('... switching trace state to: %s', traceState)
        if("ON"==traceState):
            self.aService.setCommunicationTrace(self.aTraceState.ON)
        elif("OFF"==traceState):
            self.aService.setCommunicationTrace(self.aTraceState.OFF)  
        else:
            print('error trace state')  
        
    def updateProgramming(self, sLabelPath, sContainerPath, sParam=''):
        sErrorMessage = ''
        if not (path.lexists(sContainerPath) and path.isfile(sContainerPath)):
            sErrorMessage = 'flash file path does not exist or is not a valid file'
            log.error(sErrorMessage)
            return sErrorMessage
        try:
            sessionNames = self.aService.getFlashSessions(self.aEcuConn.connectionHandle, sContainerPath, False)
            log.debug('%d sessions found in the flash file', len(sessionNames))
            descriptors = [self.aService.createFlashSessionDescriptor(int(self.aEcuConn.ecuId, 16), sContainerPath, n, False) for n in sessionNames]
            log.debug('... starting flash programming')
            self.aService.setCommunicationTrace('ON')
            self.readIdentification()
            resultList = self.aService.flashProgrammingParallel(descriptors).sessionResultList
            self.aService.setCommunicationTrace('OFF')
            hasError = False
            for result in resultList:
                hasError = hasError or result.errorOccurred
                log.debug('Session: %s, Duration: %s, Error: %s', result.sessionName, result.duration, str(result.errorOccurred))
            if hasError: 
                sErrorMessage = "ErrorOccurred set TRUE by server during programming"
                log.debug(sErrorMessage)   
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
        except Exception, e:
            sErrorMessage = str(e)
            log.error(sErrorMessage)
        return sErrorMessage
    
    def __updateProgrammingAsync(self, sLabelPath, sContainerPath, sParam=''):
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

        t = MyThread(self.updateProgramming, [sLabelPath, sContainerPath, sParam])
        t.start()
        t.join()
        print t.getResult()
    
    def eraseAllFaultMemories(self):
        sErrorMessage = ''
        log.debug('... cleaning all event memories')
        try:
            self.aService.resetAllEventMemories(True, True, 4)
#             name=self.aService.createProtocolBZD(None, None, True, None)
#             print "BZD Protocol created: "+ name
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.debug(sErrorMessage)
        
        return sErrorMessage
    
    def switchECU(self, dConfig):
        sErrorMessage = ''
        log.debug('... switch to ECU, address(Hex): %s', dConfig['sEcuId'])
        ecuIdInDec = int(dConfig['sEcuId'], 16)
        try:
            self.aEcuConn = self.aService.connectToEcu(ecuIdInDec)
            self.aEcuConn.ecuName=self.__encodeStr(self.aEcuConn.ecuName)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
        return sErrorMessage
    
    def checkUpdateProgramming(self, sLabelPath, sContainerPath, sParam=''):
        log.debug('... checking flash container: %s', sContainerPath)
        sErrorMessage = ''
        iResult = 0
        
        if not (path.lexists(sContainerPath) and path.isfile(sContainerPath)):
            sErrorMessage = 'flash file path does not exist or is not a valid file'
            log.error(sErrorMessage)
            return iResult, sErrorMessage         
        try:
            sessionNames = self.aService.getFlashSessions(self.aEcuConn.connectionHandle, sContainerPath, False)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
            return iResult, sErrorMessage
        
        log.debug('session: %s', sessionNames)
        valid = True
        try:
            for sessionName in sessionNames:
                valid = valid and self.aService.checkFlashProgrammingWithFlashContainer(self.aEcuConn.connectionHandle, sContainerPath, sessionName)
        except WebFault, e:
            sErrorMessage = self.__encodeStr(e.fault.faultstring)
            log.error(sErrorMessage)
        
        if(valid and sErrorMessage == ''):
            iResult = 1
        return iResult, sErrorMessage
    
    
        
    def exit(self):
        log.debug('... exit')
        self.aService.exit()

instance = ODISInf()

if __name__ == "__main__":
    logging.config.fileConfig("odisinf_logging.setting")
    log = logging.getLogger()
    
    odis = instance
    odis.initTester({'sVehicleProject':'SK37XCS', 'sEcuId':'19'})
    dVersions, msg = odis.getSystemInfomation()
    print dVersions
    odis.openDiagnosticsConnection()
    # odis.eraseAllFaultMemories()
    dIdentDataResult,msg=odis.readIdentification()
    print dIdentDataResult
    iResult,sErrorMessage=odis.checkUpdateProgramming('', r'C:\Program Files (x86)\Offboard_Diagnostic_Information_System_Engineering\datflash\FL_5Q0907530N__2162_S.odx', '')
    print iResult
    #sErrorMessage = odis.updateProgramming('', r'C:\Program Files (x86)\Offboard_Diagnostic_Information_System_Engineering\datflash\FL_5Q0907530N__2163_S.odx', '')
    odis.setCommunicationTrace("ON")
    odis.setCommunicationTrace("OFF")
    odis.closeDiagnosticsConnection()
    odis.deInitTester()
     
        
