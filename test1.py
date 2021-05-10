#!/usr/bin/env python3
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""
#Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, assemble
from qubic_provider import QUBICProvider
from qubic_job import QUBICJob
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

#...!...!....................
def circA():
    qc = QuantumCircuit(2)   #create a new 2-qubit quantum circuit
    qc.h(0)                  #add an hadamard gate on the 1st qubit
    qc.cx(0,1)               #add a cnot gate on the 2 qubits
    qc.measure_all()
    return qc

#...!...!....................
def circB(): # a random non-trivial 2Q circuit
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.t(1)
    bell.delay(4) # unit is dt
    bell.cx(0,1)
    bell.delay(4) # unit is dt
    bell.x(0)
    bell.h(1)
    bell.measure_all()
    return bell

#...!...!....................
def fakeQubicMeasure(inpF='FakePut.txt', outF='FakeGet.txt'): #fake execution of crcits by QubiC
    ''' open inpF and generate outF:
      compute all possible labels based on 'no_qubits' in inpF
      assign random numbers to all possible labels for Nshots='repetitions'
      save outF
    '''
    print('QubiC done, outF=',outF)
        

#=================================
#=================================
#  M A I N 
#=================================
#=================================

#set the provider
provider = QUBICProvider()  

#set the backend
backend = provider.backends.qubic_backend

#create the circuit
qc = circA()
trans_qc = transpile(qc, backend, basis_gates=['p','sx','cx'], optimization_level=1)

#assemble
qobj = assemble(trans_qc, shots=100, backend=backend)

#..... part-1 ....create a job instance
job = QUBICJob(backend,'TEST1', qobj=qobj)
job.submit()  # creates FakePut.txt

#..... part-2....ideally at this point we would run it
fakeQubicMeasure()  # FakePut.txt --> FakeGet.txt

#..... parts-3 ... "retrieve the results" of the experiment (reading FakeGet.txt)
print(job.get_counts(circuit=qc))

fig=plt.figure(1,facecolor='white', figsize=(6, 4))
ax=plt.subplot(1,1,1)

plot_histogram(job.get_counts(), ax = ax)
fig.savefig('plot.png')
plt.tight_layout()
plt.show()

