# QuantumDeviceLib: An API for superconducting integrated circuit

The main design goals of this project are:
a) Implement an software API for CRUD 
b) Ability to move up/down the hierarchy 
c) Implement a versioning system


We need to install sqlalchemy and pytest. All unit tests should pass 
before we proceed.
```sh
$ py.test
```

## Introductions
A superconducting circuit comprises of qbits and gates which forms the following one-to-many hierarchy.
```sh
device -> qubit -> gate
```

## Data Structure
To represent such a hierarchy we need three  classes which also corresponds to three SQL tables that has 
been designed to represent the relationship with bi-directional connections for easy object traversal. 

```sh
DeviceTable ⇄ QbitVersionedTable ⇄  GateVersionedTable
```
Let us run an example of device creation. I shall create a device, add qubits,
add gates for each qubit, update a qubit and delete the table. I shall be displaying the results as seen on a python shell (object addresses will differ from system to system). Please see example.py for reference.

## Step 1: Create DeviceTable

We create a device called `7-qbit-prototype` with an attached description. Although the name contains seven qubits; we shall attach two qubits to this device. The first qubit shall contain two gates and the second qubit shall contain one gate.
 
```sh
>>> from QuantumDeviceLib.app import *
>>> createDeviceTable("7-qbit-prototype","A 7 qbit prototype chip")
```
The rows of `devicetable` become:

| id        | device\_id | device\_desc  |
| ----------- |:--------------:|-------|
| 1 | 7-qbit-prototype | A 7 qbit prototype chip |

## Step 2: Read DeviceTable

We shall now use `ListDeviceTable()` which returns the list of all devices in the table.

```sh
>>> devices=ListDeviceTable()
>>> devices
[<QuantumDeviceLib.app.DeviceTable object at 0x10df474d0>]
```

## Step 3: Add Qbits
We add two qbits with different parameters to the first device.
```sh
>>> createQbitVersionedTable(2.3,1.2,1.4,device=devices[0])
>>> createQbitVersionedTable(2.4,1.3,1.5,device=devices[0])
```

This creates the following rows in `qbitversionedtable` table

| id        | version\_id | device\_id  |qbit\_counter |resonance\_freq  |t1  |t2  |
| ----------- |:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|-------|
| 1 | 1| 1 | 0 |2.3|1.2|1.4|
| 2 | 1| 1 | 1 |2.4|1.3|1.5|

The `qbit_counter` is a proxy for "qubit IDs that have per-device-scope".
This if we add a new device ; then it's first qubit will have `qbit_counter`=0

The `version_id` is always 1 unless we choose an update for a particular row.
This is when it appends a new row (doesn't delete the old row) and marks the new row
as old `version_id` plus one.

## Step 4: Read QbitVersionedTable
We shall now use `ListQbitVersionedTable()` which returns the list of all qbits in the table.

```sh
>>> qbits=ListQbitVersionedTable()
>>> qbits
[<QuantumDeviceLib.app.QbitVersionedTable object at 0x10df5b850>, <QuantumDeviceLib.app.QbitVersionedTable object at 0x10df5bbd0>]
>>>
```
Clearly we see the two qbits that have been added to the table.

## Step 5: Add Gates
We now add two gates to the first qbit and one gate to second qbit.
```sh
>>> createGateVersionedTable("+X/2",1,1.2,3.14,qbit=qbits[0])
>>> createGateVersionedTable("-Y/2",1,1.2,3.14,qbit=qbits[0])
>>> createGateVersionedTable("+X/2",2,1.3,1.2,qbit=qbits[1])
```
Thus the rows of `gateversionedtable` becomes:

| id | version\_id | gate\_id | qbit\_id | amp | width | phase |
|---|---|------|---|-----|-----|------|
| 1 | 1 | +X/2 | 1 | 1.0 | 1.2 | 3.14 |
| 2 | 1 | -Y/2 | 1 | 1.0 | 1.2 | 3.14 |
| 3 | 1 | +X/2 | 2 | 2.0 | 1.3 | 1.2  |

The `version_id` is always 1 unless we choose an update for a particular row.
This is when it appends a new row (doesn't delete the old row) and marks the new row
as old `version_id` plus one.

## Step 6: Read GateVersionedTable

```sh
>>> gates=ListGateVersionedTable()
>>> gates
[<QuantumDeviceLib.app.GateVersionedTable object at 0x10df47b90>, <QuantumDeviceLib.app.GateVersionedTable object at 0x10df74c10>, <QuantumDeviceLib.app.GateVersionedTable object at 0x10df74650>]
```

## Step 6: Traverse up and down
It  is easy to move up and down the one-to-many hierarchy as shown below.
Traversing device -> qubit -> gate
```sh
>>> devices[0].qbits[0].gates[0].gate_id
u'+X/2'
```

Traversing device <- qubit <- gate
```sh
>>> gates[0].qbit.device.device_id
u'7-qbit-prototype'
```
## Step 6: Versioning and Updating
Let's try to update row no.2. This will trigger the versioning system
and a new row will be appended to `qbitversionedtable` table
```sh
>>>updateQbitVersionedTable(2,2.45,1.33,1.55)
```

The `qbitversionedtable` table now becomes:

| id        | version\_id | device\_id  |qbit\_counter |resonance\_freq  |t1  |t2  |
| ----------- |:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|-------|
| 1 | 1| 1 | 0 |2.3|1.2|1.4|
| 2 | 1| 1 | 1 |2.4|1.3|1.5|
| 3 | 2| 1 | 1 |2.45|1.33|1.55|

Note that this new row has no connection to gates and it is the resposnibility of the user to add gates and in general maintain the data sanity.
I shall be adding gates to this qbit by triggering new version for the gates too
```sh
>>> qbits_new=ListQbitVersionedTable()
>>> updateGateVersionedTable(1,"-Y/2",2,1.3,3.14,qbit=qbits_new[-1])
```
Thus the rows of `gateversionedtable` now becomes:

| id | version\_id | gate\_id | qbit\_id | amp | width | phase |
|---|---|------|---|-----|-----|------|
| 1 | 1 | +X/2 | 1 | 1.0 | 1.2 | 3.14 |
| 2 | 1 | -Y/2 | 1 | 1.0 | 1.2 | 3.14 |
| 3 | 1 | +X/2 | 2 | 2.0 | 1.3 | 1.2  |
| 4 | 2 | -Y/2| 3 | 2.0 | 1.3 | 3.14  |

## Step 7: Delete Tables
The following command is used to delete all tables
```sh
>>> deleteALL()
```
## Step 8: Future Improvements:
  - Data quality checks to be provides
  - More robust versioning system
  - More CRUD functions.
