import os
os.chdir('D:\\test')
os.listdir('d:\\test')
from fussroom import *
odis = ODISInf()
odis.runOdis()
dConfig={'sVehicleProject':'VW37XCS', 'sEcuId':'09'}
odis.initProject(dConfig)
odis.initECU(dConfig)
odis.readIdentification()