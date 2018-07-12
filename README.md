# QuantumDeviceLib: An API for superconducting integrated circuit
.
A superconducting circuit can be broken downs into three components with the following hierarchy. These objects form a simple heirarchy of one-to-many relationships.

```sh
device -> qubit -> gate
```
These are the goals
a) Implement an software API for CRUD 
b) Ability to move up/down the hierarchy 
c) Implement a versioning system

We need to install sqlalchemy and pytest. All test should pass 
before we proceed.
```sh
$ py.test
```


# Data Structure
We have 3 class which also corresponds to three SQL tables that has 
been designed to represent the hierarchy with bi-directional connections
for easy object traversal. 

DeviceTable ⇄ QbitVersionedTable ⇄
GateVersionedTable

Let us run an example of device creation. I shall create a device, add qubits,
add gates for each qubit, update a qubit and delete the table. I shall be displaying the results as seen on a python shell (object addresses will differ from system to system). Please see example.py for reference.

#### Step 1: Create DeviceTable

We create a Device called "7-qbit-prototype" with an attached description.
```sh
>>> from QuantumDeviceLib.app import *
>>> createDeviceTable("7-qbit-prototype","A 7 qbit prototype chip")
```
The devicetable database will show this

| id        | device\_id | device\_desc  |
| ----------- |:--------------:|-------|
| 1 | 7-qbit-prototype | A 7 qbit prototype chip |
