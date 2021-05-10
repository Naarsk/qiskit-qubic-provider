# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import json

def _experiment_to_seq(circuit):
    count = 0
    qubit_map = {}
    for bit in circuit.qubits:
        qubit_map[bit] = count
        count += 1
    ops = []
    meas = 0

    # customized for QubiC basis gates
    for instruction in circuit.data:
        inst = instruction[0]
        qubits = [qubit_map[bit] for bit in instruction[1]]
        value = 0
        
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

        # (op name, exponent, [qubit index])
        ops.append((name, value, qubits))
    if not meas:
        raise ValueError('Circuit must have at least one measurements.')
    return json.dumps(ops)


def circuit_to_qubic(circuits, shots=100):
    """Return a list of json payload strings for each experiment in a qobj

    The output json format of an experiment is defined as follows:
    INCORRECT INFO:    [[op_string, gate_exponent, qubits]]

    which is a list of sequential quantum operations, each operation defined
    by:

    INCORRECT INFO: 
    op_string: str that specifies the operation type, either "X","Y","MS"
    gate_exponent: float that specifies the gate_exponent of the operation
    qubits: list of qubits where the operation acts on.
    """
    if isinstance(circuits, list):
        if len(circuits) > 1:
            raise Exception
        circuits = circuits[0]
    seqs = _experiment_to_seq(circuits)
    out_dict = {
        'data': seqs,
        'repetitions': shots,
        'no_qubits': circuits.num_qubits,
    }

    return out_dict
