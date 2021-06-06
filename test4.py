# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 10:37:52 2021

@author: Leonardo
"""
#!/usr/bin/env python3
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""
from qiskit import QuantumCircuit, transpile,assemble
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

def _experiment_to_qubic(experiment):
    ops = []
    meas = 0
    for inst in experiment.instructions:
        if inst.name == 'p':
            name = 'VZ'
            value = float(inst.params[0] )
        elif inst.name == 'delay':
            name = 'D'
            value = int(inst.params[0] )
        elif inst.name == 'sx':
            name = 'X90'
        elif inst.name == 'cx':
            name = 'CNOT'
        elif inst.name == 'measure':
            meas += 1
            continue
        elif inst.name == 'barrier':
            continue
        else:
            raise Exception("Operation '%s' outside of basis p,sx,cx" %inst.name)

        ops.append([[{'name':name,'qubitid' : inst.qubits, 'para':{value}}]])
        
    if not meas:
        raise ValueError('Circuit must have at least one measurements.')
    
    f=open('QubicPut.txt',"w")
    f.write(str(ops))
    f.close()

    return 




#=================================
#=================================
#  M A I N 
#=================================
#=================================

#set the provider
provider = QUBICProvider()  

#set the backend
backend = provider.backends.qubic_backend

qcV=circA();

trans_qc = transpile(qcV, backend, basis_gates=['p','sx','cx'], optimization_level=1)

###################################ASSEMBLE
qobj = assemble(trans_qc, shots=100, backend=backend)
job = QUBICJob(backend,'TEST1', qobj=qobj)

for experiment in job.qobj.experiments:
    _experiment_to_qubic(experiment)
