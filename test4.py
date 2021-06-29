#!/usr/bin/env python3
"""
Created on Wed Apr 21 12:05:36 2021

@author: Leonardo
"""

from qiskit import QuantumCircuit, transpile
from qiskit.assembler.assemble_circuits import _assemble_circuit
from qiskit.assembler import RunConfig
import sys,os
sys.path.append(os.path.abspath("qubicProvider/"))
from qubic_provider import QUBICProvider
#from qubic_job import QUBICJob
#from qiskit.converters import circuit_to_instruction

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
    #bell.delay(4) # unit is dt
    bell.cx(0,1)
    #bell.delay(4) # unit is dt
    bell.x(0)
    bell.h(1)
    bell.measure_all()
    return bell


def _qasm_to_qubic(in_file,out_file):  

    #CAN'T HANDLE CYCLES, NOR MULTIPLE OPENQASM IN A SINGLE FILE, NOR DELAYS
    #FIRST TURNS QASM INTO EXPERIMENT AND THEN EXPERIMENT INTO QUBIC
    
    new_qc= QuantumCircuit.from_qasm_file(in_file)    
    run_config=RunConfig()                                  #empty run configuration
    experiment=_assemble_circuit(new_qc,run_config)[0]      #experiment is a list of gates
    qubic_inst=_experiment_to_qubic(experiment)

    print(qubic_inst)

    f=open(out_file,'w')
    f.write(str(qubic_inst))
    f.close()

    return

def _experiment_to_qubic(experiment):
        
    list2=[]				#list2 is A CYCLE
    prephase=0
    for inst in experiment.instructions:
        
        if inst.name == 'p':
            name = 'VZ'
            prephase = float(inst.params[0] )
        elif inst.name == 'barrier':
            pass
        elif inst.name == 'delay':
            pass
        else:
            if inst.name == 'sx':
                name = 'X90'
            elif inst.name == 'cx':
                name = 'CNOT'
            elif inst.name == 'measure':
                name = 'MEAS'
# =============================================================================
#             elif inst.name == 'delay':
#                 name = 'D'
#                 value = int(inst.params[0] )
# =============================================================================
            else:
                raise Exception("Operation '%s' outside of basis p,sx,cx" %inst.name)
				
            dict1={'name':name,'qubitid' : inst.qubits, 'para':{'prephase': prephase}}
            prephase=0
            list1=[]				#max number of elements: n_qubit #still i dont know how many to put 
            list1.append(dict1)
				
            dict2={'gates': list1}
            list2.append(dict2)

    return list2

#=================================
#=================================
#  M A I N 
#=================================
#=================================

#set the provider
provider = QUBICProvider()  

#set the backend
backend = provider.backends.qubic_backend

#create the list of circuits
qcV=circC();
print(qcV)



trans_qc = transpile(qcV, backend, basis_gates=['p','sx','cx'], optimization_level=1)
trans_qc.qasm(formatted=True, filename='QasmPut.txt')  	#write QasmPut
new_qc= QuantumCircuit.from_qasm_file('QasmPut.txt')    #read QasmPut, print circuit
print(new_qc)
_qasm_to_qubic('QasmPut.txt','QubicPut.txt')			#read QasmPut, write QubicPut
