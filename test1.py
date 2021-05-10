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
import json

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
def fakeQubicMeasure(infile,outfile): #fake execution of crcits by QubiC
    f=open(infile,'r')
    j_load=json.load(f)
    out_dict=j_load[0]
    f.close()
    
    data=out_dict['data']
    del out_dict['data']
    
    samples= [3, 0, 0, 0, 0, 3, 3, 0, 2, 1, 0, 3, 0, 2, 3, 0, 3, 1, 3, 0, 1, 3,
              0, 3, 0, 1, 0, 0, 3, 3, 2, 0, 0, 0, 3, 2, 3, 3, 3, 0, 3, 0, 0, 3,
              3, 3, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 3, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 3, 0, 3, 3, 0, 3, 0, 0,
              3, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]
    
    out_dict['received']=data
    out_dict['samples']=samples
    out_dict['status']='finished'
    

    f=open(outfile,'w')
    json.dump(out_dict, f)
    f.close()
    

    ''' open inpF and generate outF:
      compute all possible labels based on 'no_qubits' in inpF
      assign random numbers to all possible labels for Nshots='repetitions'
      save outF
    '''
    #print('QubiC done, outF=',outF)
        

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
qc = circB()
print('qc0');print(qc)

#transpile
trans_qc = transpile(qc, backend, basis_gates=['p','sx','cx'], optimization_level=1)
print('qc1');print(trans_qc)

#assemble
qobj = assemble(trans_qc, shots=100, backend=backend)

#..... part-1 ....create a job instance
job = QUBICJob(backend,'TEST1', qobj=qobj)
job.submit()  # creates FakePut.txt

#..... part-2....ideally at this point we would run it
fakeQubicMeasure('FakePut.txt','FakeGet.txt')  # FakePut.txt --> FakeGet.txt

#..... parts-3 ... "retrieve the results" of the experiment (reading FakeGet.txt)
print('got job:',job.get_counts(circuit=qc))

fig=plt.figure(1,facecolor='white', figsize=(6, 4))
ax=plt.subplot(1,1,1)

plot_histogram(job.get_counts(), ax = ax)
plt.tight_layout()
fig.savefig('plot.png')
plt.show()  # this pops-up the canvas
