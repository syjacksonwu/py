# coding: latin-1
#Macro started on: 2014-04-22 12:20:47:147
import sys
sys.setdefaultencoding( "latin-1")
from java.lang import Boolean
from java.util import HashMap
from java.util import ArrayList
from de.volkswagen.odis.vaudas.vehiclefunction.automation import IDiagnosticInterface
from de.volkswagen.odis.vaudas.vehiclefunction.automation.types import IDiagResultConnectEcu
from de.volkswagen.odis.vaudas.vehiclefunction.automation import IEcuStateInterface
diagnosticInterface = IDiagnosticInterface.Factory.getInstance()
diagnosticInterface.configureSetting("Multilink.MaxNumberOfLogicalLinks", "1")
#Macro has been recorded using the project: VW36X
print "Identifikation wird gelesen: Diagnoseinterface f�r Datenbus"
resultConnectToEcu = diagnosticInterface.connectToEcu(0x19)
diagnosticInterface.readIdentification(resultConnectToEcu.getConnectionHandle())
print "Wechsel der Diagnosesitzung wird durchgef�hrt: Diagnoseinterface f�r Datenbus"
diagnosticInterface.openConnection(resultConnectToEcu.getConnectionHandle())
diagnosticInterface.switchSession(resultConnectToEcu.getConnectionHandle(), "83")
print "Zugriffberechtigung wird durchgef�hrt: Diagnoseinterface f�r Datenbus"
diagnosticInterface.securityAccess(resultConnectToEcu.getConnectionHandle(), "20103", "automatic")
print "Hex-Services werden geschrieben: Diagnoseinterface f�r Datenbus"
diagnosticInterface.sendRawService(resultConnectToEcu.getConnectionHandle(), "35 00 20 00 00 00 00 0B")
print "Hex-Services werden geschrieben: Diagnoseinterface f�r Datenbus"
diagnosticInterface.sendRawService(resultConnectToEcu.getConnectionHandle(), "36")
print "Hex-Services werden geschrieben: Diagnoseinterface f�r Datenbus"
diagnosticInterface.sendRawService(resultConnectToEcu.getConnectionHandle(), "37")
#Macro finished on: 2014-04-22 12:22:42:155
