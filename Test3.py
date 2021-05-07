# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""
#Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, assemble
from qubic_provider import QUBICProvider
from qubic_job import QUBICJob
from qiskit.visualization import plot_histogram
#1 part: same as Test1
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
#assemble
qobj = assemble(trans_qc, shots=100, backend=backend)

#create a job instance
job = QUBICJob(backend,'TEST3', qobj=qobj)

#ideally at this point we would run it

#2 part: we "retrieve the results" of the experiment (reading FakeGet.txt)
print(job.get_counts(circuit=qc)) 
plot_histogram(job.get_counts())