#Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile
from qubic_provider import QUBICProvider

#set the provider
provider = QUBICProvider()  

#set the backend
backend = provider.backends.qubic_simulator

#create the circuit
qc = QuantumCircuit(2)   #create a new 2-qubit quantum circuit
qc.h(0)                  #add an hadamard gate on the 1st qubit
qc.cx(0,1)               #add a cnot gate on the 2 qubits
qc.measure_all()

#double transpile
qc2 = transpile(qc, basis_gates=['u1','u2','u3','cx'], optimization_level=1)
qc3 = transpile(qc2, basis_gates=['p','sx','cx'], optimization_level=1)

#directly run the circuit (aka print the FakePut.txt) without need to assemble
job = backend.run(qc3)
