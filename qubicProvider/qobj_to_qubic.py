# -*- coding: utf-8 -*-

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

#from numpy import pi

#qubic basis
def _experiment_to_seq(experiment):
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


        ops.append((name, value, inst.qubits))
        
    if not meas:
        raise ValueError('Circuit must have at least one measurements.')
    return json.dumps(ops)


def qobj_to_qubic(qobj):
    """Return a list of json payload strings for each experiment in a qobj

    The output json format of an experiment is defined as follows:
        [[op_string, gate_exponent, qubits]]

    which is a list of sequential quantum operations, each operation defined
    by:

    op_string: str that specifies the operation type, either "X","Y","MS"
    gate_exponent: float that specifies the gate_exponent of the operation
    qubits: list of qubits where the operation acts on.
    """

    if len(qobj.experiments) > 1:
        raise Exception
    for experiment in qobj.experiments:
        seqs = _experiment_to_seq(experiment)
        out_dict = {
            'data': seqs,
            'repetitions': qobj.config.shots,
            'no_qubits': qobj.config.n_qubits,
        }
        
    return out_dict
