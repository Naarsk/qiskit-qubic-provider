#!/usr/bin/env python3
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""
import numpy as np
from qiskit import QuantumCircuit, transpile, assemble
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import json
import sys,os
sys.path.append(os.path.abspath("qubicProvider/"))
from qubic_provider import QUBICProvider
from qubic_job import QUBICJob

#...!...!....................
def circA():
    qc = QuantumCircuit(2)   #create a new 2-qubit quantum circuit
    qc.h(0)                  #add an hadamard gate on the 1st qubit
    qc.cx(0,1)               #add a cnot gate on the 2 qubits
    qc.measure_all()
    return qc

#...!...!....................
def circB():
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    return qc

#...!...!....................
def circC(): # a random non-trivial 2Q circuit
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
    ''' open inpF and generate outF:
      compute all possible labels (NS)  based on 'no_qubits' in inpF
      assign random numbers to all possible labels for Nshots='repetitions'
      save outF
    '''

    f=open(infile,'r')
    j_load=json.load(f)
    f.close()
    j_out=[]
    
    for out_dict in j_load:
        circ_data=out_dict['data'] # can be used to define QubiC circuit
        del out_dict['data']
        NQ=out_dict["no_qubits"]
        NS=1<<NQ  # um of unique bit-strings
        shots=out_dict["repetitions"]
        
        print('fake QubicMeasure NQ=%d, NS=%d shots=%d'%(NQ,NS,shots))
    
        # random measurements
        
        samples=np.random.randint(NS,size=shots).tolist()
        #print('ss',samples,type(samples[0]))
         
        out_dict['received']=circ_data
        out_dict['samples']=samples
        out_dict['status']='finished'
        
        j_out.append(out_dict)

    f=open(outfile,'w')
    json.dump(j_out, f)
    f.close()
    

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

#create 1 circuit
#qc = circA();print('qc0');print(qc)

#create many circuits
qcV=[circA(),circB(),circC()];
for circ in qcV:
    print(circ)

###################################TRANSPILE
#trans_qc = transpile(qc, backend, basis_gates=['p','sx','cx'], optimization_level=1)
#print('qc1');print(trans_qc)

trans_qc = transpile(qcV, backend, basis_gates=['p','sx','cx'], optimization_level=1)
print('qcV');print(trans_qc)

###################################ASSEMBLE
qobj = assemble(trans_qc, shots=100, backend=backend)

#..... part-1 ....create a job instance
job = QUBICJob(backend,'TEST1', qobj=qobj)
job.submit()  # creates FakePut.txt

#..... part-2....ideally at this point we would run it
fakeQubicMeasure('FakePut.txt','FakeGet.txt')  # FakePut.txt --> FakeGet.txt

#..... parts-3 ... "retrieve the results" of the experiment (reading FakeGet.txt)
#print('got job:',job.get_counts(circuit=qc))
data=[job.get_counts(circuit=0),job.get_counts(circuit=1),job.get_counts(circuit=2)]

print('got job:',data)

fig=plt.figure(1,facecolor='white', figsize=(6, 4))
ax=plt.subplot(1,1,1)

plot_histogram(data, ax = ax)
plt.tight_layout()
fig.savefig('plot.png')
plt.show()  # this pops-up the canvas
