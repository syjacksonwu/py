# 
#   Dieses Makro ueberwacht den Ereignisspeicher des Bremsensteuergeraets
#   durch eine zyklische Abfrage und sendet ein akustisches Signal f¨¹r
#   jeden gefundenen Ereigniseintrag. Nach einer Stunde beendet sich das   #   Makro.
# zus?tzlich ab Offboard Diagnostic Information System Release 4.0 erforderliche Elemente in dieser Farbe
#
from de.volkswagen.Offboard Diagnostic Information System.vaudas.vehiclefunction.automation import IDiagnosticInterface
import time
#
# ein print ¡°\a¡± (ASCII-Bell) kann im Offboard Diagnostic Information System nicht verwendet werden, 
# daher:
from java.awt import Toolkit

ecu = 3 # Reizadresse des Bremsensteuergeraets

# Diagnoseinterface oeffnen, Fahrzeugprojekt waehlen und mit dem 
# Steuergeraet verbinden:

diagnosticInterface = IDiagnosticInterface.Factory.getInstance()
#diagnosticInterface.setVehicleProject('VWFLEET')
myEcu = diagnosticInterface.connectToEcu(ecu)
myEcuHandle = myEcu.getConnectionHandle()

running = 0

while 1:
	# Ereignisspeicher lesen
	eventMemories = diagnosticInterface.readEventMemory(myEcuHandle)
	
	# Anzahl der Ereignisse bestimmen
	size = eventMemories.getEventMemoryEntries().size()
	
	print size
	# Wenn mindestens ein Ereignis gelesen wurde 
	if (size > 0):
		# Ergebnisausgabe und <size> mal doppelt piepen
		print "SG %d hat %d Ereignis(se) gespeichert" % (ecu, size)
		for i in range(0,size):
			# Doppel-Piep
			Toolkit.getDefaultToolkit().beep()
			time.sleep(0.2)	# 0,2 s Pause
			Toolkit.getDefaultToolkit().beep()
			time.sleep(0.5)	# 0,5 s Pause zwischen den Signalen
	# nach 60 min. aus der Schleife heraus springen und Makro beenden
	if running >= 60:	break
	running = running + 1 
	# Wartezeit von 60 Sekunden
	time.sleep(60)
# diagnosticInterface.closeConnection(myEcuHandle)
#exit()
