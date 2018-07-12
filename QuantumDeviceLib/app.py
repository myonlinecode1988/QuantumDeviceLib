from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Integer, String,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///QuantumDB.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session() 
########################################################################
class DeviceTable(Base):
    """"""
    __tablename__ = "devicetable"
 
    id = Column(Integer, primary_key=True)
    device_id = Column(String,nullable=False)
    device_desc = Column(String)
    qbits = relationship("QbitVersionedTable", back_populates="device")

    #__table_args__ = (UniqueConstraint('device_id','device_desc'),)

 
    #----------------------------------------------------------------------
    def __init__(self, device_id, device_desc):
        """"""
        self.device_id = device_id
        self.device_desc = device_desc
        #self.qbits = qbits


class QbitVersionedTable(Base):
    """"""
    __tablename__ = "qbitversionedtable"
 
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, nullable=False,default=1)
    device_id = Column(Integer, ForeignKey('devicetable.id'))
    qbit_counter = Column(Integer)
    resonance_freq = Column(Float)
    t1 = Column(Float)
    t2 = Column(Float)

    #__mapper_args__ = {"version_id_col": version_id}

    device = relationship("DeviceTable", back_populates="qbits")
    gates = relationship("GateVersionedTable", back_populates="qbit")
    #----------------------------------------------------------------------
    def __init__(self,qbit_counter,resonance_freq,t1,t2,device):
        """"""
        self.qbit_counter = qbit_counter
        self.resonance_freq = resonance_freq
        self.t1 = t1
        self.t2 = t2
        self.device = device


class GateVersionedTable(Base):
    """"""
    __tablename__ = "gateversionedtable"
 
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, nullable=False,default=1)
    gate_id = Column(String)
    qbit_id = Column(String, ForeignKey('qbitversionedtable.id'))
    amp = Column(Float)
    width = Column(Float)
    phase = Column(Float)
    #__mapper_args__ = {"version_id_col": version_id}
 
    qbit = relationship("QbitVersionedTable", back_populates="gates")
    #----------------------------------------------------------------------
    def __init__(self, gate_id,amp, width, phase,qbit):
        """"""
        self.gate_id = gate_id
        self.amp = amp
        self.width = width
        self.phase = phase
        self.qbit = qbit

# Create DeviceTable Object
def createDeviceTable(device_id,device_desc):
    device_data=DeviceTable(device_id,device_desc)
    session.add(device_data)
    attempt_commit()

# Read DeviceTable Object
def ListDeviceTable():
    return session.query(DeviceTable).all()

# Create QbitVersionedTable Object
def createQbitVersionedTable(resonance_freq,t1,t2,device):
    #Check whether device id exists in QbitVersionedTable
    #If yes increment the qbit_counter else set qbit_counter=0
    #Checking if device_id exists
    qbitspresent=session.query(QbitVersionedTable).filter(QbitVersionedTable.device_id==device.id).all()
    qbit_data=QbitVersionedTable(len(qbitspresent),resonance_freq,t1,t2,device)
    session.add(qbit_data)
    attempt_commit() 

# Read QbitVersionedTable Object
def ListQbitVersionedTable():
    return session.query(QbitVersionedTable).all()

# Create GateVersionedTable Object
def createGateVersionedTable(gate_id,amp, width, phase,qbit):
    gate_data=GateVersionedTable(gate_id,amp, width, phase,qbit)
    session.add(gate_data)
    attempt_commit()

# Read GateVersionedTable Object
def ListGateVersionedTable():
    return session.query(GateVersionedTable).all()

# Update QbitVersionedTable Object TRIGGERS VERSIONING !
def updateQbitVersionedTable(row_num,resonance_freq,t1,t2):
    #Checking if device_id exists
    qbitspresent=session.query(QbitVersionedTable).filter(QbitVersionedTable.id==row_num).all()
    old_version_id=qbitspresent[0].version_id
    qbit_data=QbitVersionedTable(qbitspresent[0].qbit_counter,resonance_freq,t1,t2,qbitspresent[0].device)
    session.add(qbit_data)
    attempt_commit()
    last_row=session.query(QbitVersionedTable).order_by(QbitVersionedTable.id.desc()).first() 
    last_row.version_id=old_version_id+1
    attempt_commit()


# Update GateVersionedTable Object TRIGGERS VERSIONING !
def updateGateVersionedTable(row_num,gate_id,amp, width, phase,qbit):
    #Checking if device_id exists
    gatespresent=session.query(GateVersionedTable).filter(GateVersionedTable.id==row_num).all()
    old_version_id=gatespresent[0].version_id
    gate_data=GateVersionedTable(gate_id,amp, width, phase,qbit)
    session.add(gate_data)
    attempt_commit()
    last_row=session.query(GateVersionedTable).order_by(GateVersionedTable.id.desc()).first() 
    last_row.version_id=old_version_id+1
    attempt_commit()


def attempt_commit():
    # commit the record the database
    try:
        session.commit()
    except:
        import sys
        print("ERROR",sys.exc_info())

def deleteALL():
    Base.metadata.drop_all(bind=engine)
    session.commit()


# create tables
Base.metadata.create_all(engine)
