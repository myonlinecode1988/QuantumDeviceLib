from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from QuantumDeviceLib.app import *
import sqlalchemy.exc as sqlalchemy_exc

 
# Create DeviceTable objects 
createDeviceTable("7-qbit-prototype","A 7 qbit prototype chip")
createDeviceTable("test-device-1","Test Device v1")
 
# List DeviceTable objects 
devices=ListDeviceTable()

#create QbitVersionedTable Object
createQbitVersionedTable(2.3,1.2,1.4,device=devices[0])
createQbitVersionedTable(2.4,1.3,1.5,device=devices[0])
createQbitVersionedTable(2.5,1.4,1.6,device=devices[1])

# Read QbitVersionedTable Object
qbits=ListQbitVersionedTable()
print qbits[0].qbit_counter,qbits[1].qbit_counter,qbits[2].qbit_counter

createGateVersionedTable("+X/2",1,1.2,3.14,qbit=qbits[0])
createGateVersionedTable("-Y/2",1,1.2,3.14,qbit=qbits[0])
createGateVersionedTable("+X/2",2,1.3,1.2,qbit=qbits[1])
gates=ListGateVersionedTable()
print gates

updateQbitVersionedTable(2,2.45,1.33,1.55)
updateQbitVersionedTable(4,2.455,1.333,1.555)

qbits=ListQbitVersionedTable()
updateGateVersionedTable(1,"-Y/2",2,1.3,3.14,qbit=qbits[-1])
