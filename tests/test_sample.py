#import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from QuantumDeviceLib.app import *
import sqlalchemy.exc as sqlalchemy_exc


def test_create_devices():
   
    # Create DeviceTable objects
    createDeviceTable("7-qbit-prototype","A 7 qbit prototype chip")
    createDeviceTable("test-device-1","Test Device v1")

    #Checking wheher two rows are created
    assert(len(session.query(DeviceTable).all())==2) 


def test_list_devices():
    
    #Listing  all devices
    devices=ListDeviceTable()
    
    #Listing device and checking the content of 1st row of device
    assert(session.query(DeviceTable).first().device_id=="7-qbit-prototype") 

def test_create_qbits():

    devices=ListDeviceTable() 

    #Assigning new qbits to device[0] 
    createQbitVersionedTable(2.3,1.2,1.4,device=devices[0])
    createQbitVersionedTable(2.4,1.3,1.5,device=devices[0])

    #Assigning new qbits to device[1] 
    createQbitVersionedTable(2.5,1.4,1.6,device=devices[1])

    #Assigning Checking qbit_counter
    assert(devices[0].qbits[0].qbit_counter==0) 
    assert(devices[0].qbits[0].resonance_freq==2.3) 
    assert(devices[0].qbits[0].t1==1.2) 
    assert(devices[0].qbits[0].t2==1.4) 
    assert(devices[0].qbits[1].qbit_counter==1) 
    assert(devices[0].qbits[1].resonance_freq==2.4) 
    assert(devices[0].qbits[1].t1==1.3) 
    assert(devices[0].qbits[1].t2==1.5) 
    assert(devices[1].qbits[0].qbit_counter==0) 
    assert(devices[1].qbits[0].resonance_freq==2.5) 
    assert(devices[1].qbits[0].t1==1.4) 
    assert(devices[1].qbits[0].t2==1.6) 


def test_create_gates():
    
    devices=ListDeviceTable()
    qbits=ListQbitVersionedTable() 
    createGateVersionedTable("+X/2",1,1.2,3.14,qbit=qbits[0])
    createGateVersionedTable("-Y/2",1,1.2,3.14,qbit=qbits[0])
    createGateVersionedTable("+X/2",2,1.3,1.2,qbit=qbits[1])
    assert(len(session.query(GateVersionedTable).all())==3) 
    assert(devices[0].qbits[0].gates[0].gate_id=="+X/2") 
    assert(devices[0].qbits[0].gates[1].gate_id=="-Y/2")



def test_versioning():
    updateQbitVersionedTable(2,2.45,1.33,1.55)
    assert(session.query(QbitVersionedTable).order_by(QbitVersionedTable.id.desc()).first().version_id==2)
    updateQbitVersionedTable(4,2.455,1.333,1.555)
    assert(session.query(QbitVersionedTable).order_by(QbitVersionedTable.id.desc()).first().version_id==3)
    qbits=ListQbitVersionedTable()
    updateGateVersionedTable(1,"-Y/2",2,1.3,3.14,qbit=qbits[-1])
    assert(session.query(GateVersionedTable).order_by(GateVersionedTable.id.desc()).first().version_id==2)

def test_delete_all():
    deleteALL()
    assert(True)
