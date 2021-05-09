# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""
#Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, assemble, IBMQ
#from qubic_provider import QUBICProvider
from qubic_job import QUBICJob


#provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
provider = IBMQ.load_account()   #set my account at IBMQ as provider
#backName='ibmq_armonk'
backName='ibmq_qasm_simulator'
backend = provider.get_backend(backName)


#create the circuit
qc = QuantumCircuit(2)   #create a new 2-qubit quantum circuit
qc.h(0)                  #add an hadamard gate on the 1st qubit
qc.cx(0,1)               #add a cnot gate on the 2 qubits
qc.measure_all()
print('circuit'); print(qc)

#transpile
trans_qc = transpile(qc, backend,basis_gates=['u1','u2','u3','cx'], optimization_level=1)
print('trans circuit'); print(trans_qc)

#assemble
qobj = assemble(trans_qc, shots=100, backend=backend)

#create a job instance
job = QUBICJob(backend,'TESTJ', qobj=qobj)
#submit the job for execution (aka print the FakePut.txt)
job.submit()
