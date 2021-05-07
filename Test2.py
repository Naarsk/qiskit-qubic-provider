# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""
#Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile
from qubic_provider import QUBICProvider
#from qubic_job import QUBICJob

#set the provider
provider = QUBICProvider()  

#set the backend
backend = provider.backends.qubic_backend

#create the circuit
qc = QuantumCircuit(2)   #create a new 2-qubit quantum circuit
qc.h(0)                  #add an hadamard gate on the 1st qubit
qc.cx(0,1)               #add a cnot gate on the 2 qubits
qc.measure_all()

#transpile
trans_qc = transpile(qc, backend)

#directly run the circuit (aka print the FakePut.txt) without need to assemble
job = backend.run(trans_qc)