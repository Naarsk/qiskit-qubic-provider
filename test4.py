#!/usr/bin/env python3

from qiskit import QuantumCircuit, transpile
from qiskit.converters import circuit_to_dag#, dag_to_circuit
from pprint import pprint
import sys,os
import numpy as np
sys.path.append(os.path.abspath("qubicProvider/"))
from qubic_provider import QUBICProvider
from qiskit_textbook.problems import grover_problem_oracle  #https://github.com/qiskit-community/qiskit-textbook

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

def circB1():
  qc = QuantumCircuit(3)
  for i in range(2):
    for iq in range(3):
      qc.sx(iq)
      qc.p(0.2,qubit=iq)
  qc.cx(0,1)
  for iq in range(3):
      qc.sx(iq)
  return qc


def circB2():
  qc = QuantumCircuit(3)
  qc.p(0.2,qubit=1) 
  for i in range(2):
    for iq in range(3):
      qc.sx(iq)
      qc.p(0.2,qubit=iq)
  qc.cx(0,1)
  for iq in range(3):
      qc.sx(iq)
  return qc



#...!...!....................
def circC():
  qc = QuantumCircuit(2)
  qc.p(0.33,qubit=1)
  for iq in range(2): qc.sx(iq)  
  for i in range(3): qc.p(0.1*i,qubit=0)
  for iq in range(2): qc.sx(iq)
  qc.sx(1)
  qc.p(0.22,qubit=0)
  qc.cx(0,1)
  qc.p(0.44,qubit=1)
  for iq in range(2): qc.sx(iq)
  return qc


#...!...!....................
def circD(): # a random non-trivial 2Q circuit
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.h(0)
    bell.t(1)
    bell.barrier()
    bell.cx(0,1)
    bell.barrier()
    bell.measure_all()
    return bell

#...!...!..................
def circE():
    qc = QuantumCircuit(3,3)
    qc.sx(0)
    qc.cx(0,1)
    qc.p(np.pi/3,qubit=2)
    qc.cx(1,2)
    qc.sx(0)
    qc.cx(0,1)
    qc.barrier([0, 1,2])
    for i in range(3): qc.measure(i,i)
    return qc


def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s

def Grover():
    n = 3
    qc = QuantumCircuit(n)

    for q in range(n):
        qc.h(q)

    oracle = grover_problem_oracle(n, variant=1)  # 0th variant of oracle, with n qubits
    qc.append(oracle, [0,1,2])
    qc.append(diffuser(n), [0,1,2])
    qc.measure_all()
    return transpile(qc, basis_gates=['p','sx','cx'], optimization_level=0)

def Toffoli():
    qc = QuantumCircuit(3)
    qc.ccx(0,1,2)
    return transpile(qc, basis_gates=['p','sx','cx'], optimization_level=0)

    
def Swap():
    qc = QuantumCircuit(2)
    qc.cx(1,0)
    qc.cx(0,1)
    qc.cx(1,0)
    return qc


#...!...!..................
def print_dag_layers(qdag):
  dagLay=qdag.layers()
  print('Show %d layers as lsist of gates, format: gateName qubits[] params[]; '%qdag.properties()['depth'])
  for k,lay in enumerate(dagLay):
    print('\n%d cycle: '%k,end='')
    for op in lay['graph'].op_nodes():
      qL=[qub._index for qub in  op.qargs]
      parV=[ float('%.6f'%v)  for v in op._op._params]      
      print('  ',op.name, 'q'+str(qL), parV,';', end='')

  print('\nend-of-cycles') 

def check_basis(qdag):
    for op in qdag.properties()['operations']:
       if op=='p':    
           continue            
       elif op == 'sx':
           continue
       elif op=='cx':
           continue
       elif  op=='measure':
           continue
       elif op == 'delay':
           continue            
       elif op=='barrier':
               pass
       else :
               raise Exception("Operation outside of basis p,sx,cx" )
    return 1


#...!...!..................
def _dag_to_qcref(qdag):
    
    dagLay=qdag.layers()
    qubic_circ=[]
    nqubit=qdag.properties()['qubits']
    prephases=np.zeros(nqubit)

    for k,lay in enumerate(dagLay):
        
        cycle=[]

        for op in lay['graph'].op_nodes(): 
               
            qL=[qub._index for qub in  op.qargs]
            parV=[ float('%.6f'%v)  for v in op._op._params]      
            
            if op.name=='p':    
                prephases[qL[0]]=prephases[qL[0]]+parV   #sums up consecutive phases
            
            elif op.name == 'sx':
                cycle.append({'name':'X90','qubitid' : qL, 'para':{'prephase': prephases[qL[0]]}})
                prephases[qL[0]]=0
   
            elif op.name=='cx':
                cycle.append({'name': 'CNOT','qubitid' : qL, 'para':[{'prephase': prephases[qL[0]]},{'prephase': prephases[qL[1]]}]})
                prephases[qL[0]]=0
                prephases[qL[1]]=0
                
            elif  op.name=='measure':
                cycle.append({'name':'MEAS','qubitid' :qL})

            elif op.name == 'delay':
                cycle.append({'name':'D','qubitid' : qL, 'para':{'delay': parV}})
            
            elif op.name=='barrier':
                pass
            
            else :
                raise Exception("Operation outside of basis p,sx,cx" )
                
        if len(cycle)!=0:
            qubic_circ.append({'gates':cycle})
        else:
            pass
    
    return qubic_circ


# =============================================================================
# def _qasm_to_qcref(in_file,out_file):  
# 
#     #CAN'T HANDLE MULTIPLE OPENQASM IN A SINGLE FILE
#     
#     qc= QuantumCircuit.from_qasm_file(in_file)    
#     qdag = circuit_to_dag(qc)
#     check_basis(qdag)             
#     qubic_circ=_dag_to_qcref(qdag)              #circuit in qubic format
# 
#     f=open(out_file,'w')
#     f.write(str(qubic_circ))
#     f.close()
# 
#     return
# =============================================================================


def one_qiskit_to_qcref(qc):
    qdag = circuit_to_dag(qc)           #convert the circuit into dag
    check_basis(qdag)                   #check if there is any alien gate
    qubic_circ=_dag_to_qcref(qdag)      #return the circuit in qcref format
    return qubic_circ

#=================================
#=================================
#  M A I N 
#=================================
#=================================

#set the provider
provider = QUBICProvider()  

#set the backend
backend = provider.backends.qubic_backend

#create the single circuit
qc = Grover()
print('qc from Qiskit')
print(qc)


qubic_qc=one_qiskit_to_qcref(qc)		
pprint(qubic_qc)

# =============================================================================
# qdag = circuit_to_dag(qc)
# #qdag.draw()  # pop-up persistent ImagViewer  (not from Matplotlib)
# 
# print('\nList DAG  properties:')
# pprint(qdag.properties())
# 
# print('\nDecomposition of circuit DAG into cycles')
# print_dag_layers(qdag)
# 
# #trans_qc = transpile(qcV, backend, basis_gates=['p','sx','cx'], optimization_level=1)
# print('\nOpenQASM format of circuit')
# qc.qasm(formatted=True, filename='QasmPut.txt')  	#write QasmPut
# 
# print('\nGrover')
# 
# print('\nqc from OpenQASM file')
# new_qc=QuantumCircuit.from_qasm_file('QasmPut.txt')
# print(new_qc)
# =============================================================================


