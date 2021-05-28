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

import warnings

from qiskit import assemble
from qiskit.providers import BackendV1 as Backend
from qiskit.providers import Options
from qiskit.providers.models import BackendConfiguration
from qiskit.util import deprecate_arguments

import qubic_job


class QUBICDevice(Backend):

    def __init__(self, provider):
        configuration = {
            'backend_name': 'qubic_backend',
            'backend_version': '1.0',
            'simulator': False,
            'local': True,
            'coupling_map': None,
            'description': 'Qubic device',
            'basis_gates': ['p', 'sx', 'cnot'],
            'memory': False,
            'n_qubits': 16,
            'conditional': False,
            'max_shots': 200,
            'max_experiments': 1,
            'open_pulse': False,
            'gates': [
                {
                    'name': 'TODO',
                    'parameters': [],
                    'qasm_def': 'TODO'
                }
            ]
        }
        super().__init__(
            configuration=BackendConfiguration.from_dict(configuration),
            provider=provider)

    @classmethod
    def _default_options(cls):
        return Options(shots=100,ids='DefaultId')

    @deprecate_arguments({'qobj': 'circuit'})
    def run(self, circuit, **kwargs):
        for kwarg in kwargs:
            if kwarg != 'shots' or kwarg != 'job_id':
                warnings.warn(
                    "Option %s is not used by this backend" % kwarg,
                    UserWarning, stacklevel=2)
            
        out_shots = kwargs.get('shots', self.options.shots)            
        job_id= kwargs.get('job_id', self.options.ids)
        
        qobj = assemble(circuit, shots=out_shots, backend=self)

        job = qubic_job.QUBICJob(self, job_id, qobj)
                
        job.submit()
        
        return job
