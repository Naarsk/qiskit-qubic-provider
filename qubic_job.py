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

# pylint: disable=protected-access

import json

from qiskit.providers import JobV1
from qiskit.providers.jobstatus import JobStatus
from qiskit.qobj import QasmQobj
from qiskit.result import Result
from qobj_to_qubic import qobj_to_qubic


class QUBICJob(JobV1):
    def __init__(self, backend, job_id, qobj=None):
        """Initialize a job instance.

        Parameters:
            backend (BaseBackend): Backend that job was executed on.
            job_id (str): The unique job ID.
            qobj (Qobj): Quantum object, if any.
        """
        super().__init__(backend, job_id)
        self._backend = backend
        self.qobj = qobj
        self._job_id = job_id
        self.memory_mapping = self._build_memory_mapping()

    def _build_memory_mapping(self):
        qu2cl = {}
        if isinstance(self.qobj, QasmQobj):
            for instruction in self.qobj.experiments[0].instructions:
                if instruction.name == 'measure':
                    qu2cl[instruction.qubits[0]] = instruction.memory[0]
            return qu2cl
        qubit_map = {}
        count = 0
        for bit in self.qobj.qubits:
            qubit_map[bit] = count
            count += 1
        clbit_map = {}
        count = 0
        for bit in self.qobj.clbits:
            clbit_map[bit] = count
            count += 1
        for instruction in self.qobj.data:
            if instruction[0].name == 'measure':
                for index, qubit in enumerate(instruction[1]):
                    qu2cl[qubit_map[qubit]] = clbit_map[instruction[2][index]]
        return qu2cl

    def _rearrange_result(self, input):
        if isinstance(self.qobj, QasmQobj):
            length = self.qobj.experiments[0].header.memory_slots
        else:
            length = self.qobj.num_clbits
        bin_output = list('0' * length)
        bin_input = list(bin(input)[2:].rjust(length, '0'))
        bin_input.reverse()
        for qu, cl in self.memory_mapping.items():
            bin_output[cl] = bin_input[qu]
        bin_output.reverse()
        return hex(int(''.join(bin_output), 2))

    def _format_counts(self, samples):
        counts = {}        
        for result in samples:
            h_result = self._rearrange_result(result)
            if h_result not in counts:
                counts[h_result] = 1
            else:
                counts[h_result] += 1
        return counts

    def result(self):
        """Get the result data of a circuit.

        Parameters: none

        Returns:
            Result: Result object.
        """
        
        result = None
        f=open("./FakeGet.txt","r")
        result =json.loads(f.read())
        f.close()        
        if isinstance(self.qobj, QasmQobj):
            results = [
                {
                    'success': True,
                    'shots': len(result['samples']),
                    'data': {'counts': self._format_counts(result['samples'])},
                    'header': {'memory_slots': self.qobj.config.memory_slots,
                               'name': self.qobj.experiments[0].header.name}
                }]
            qobj_id = self.qobj.qobj_id
        else:
            results = [
                {
                    'success': True,
                    'shots': len(result['samples']),
                    'data': {'counts': self._format_counts(result['samples'])},
                    'header': {'memory_slots': self.qobj.num_clbits,
                               'name': self.qobj.name}
                }]
            qobj_id = id(self.qobj)

        return Result.from_dict({
            'results': results,
            'backend_name': self._backend._configuration.backend_name,
            'backend_version': self._backend._configuration.backend_version,
            'qobj_id': qobj_id,
            'success': True,
            'job_id': self._job_id,
        })

    def get_counts(self, circuit=None, timeout=None, wait=5):
        """Get the histogram data of a measured circuit.

        Parameters:
            circuit (str or QuantumCircuit or int or None): The index of the circuit.
            timeout (float): A timeout for trying to get the counts.
            wait (float): A specified wait time between counts retrival
                          attempts.

        Returns:
            dict: Dictionary of string : int key-value pairs.
        """
        return self.result().get_counts(circuit)

    def cancel(self):
        pass

    def status(self):
        """read the job status.
        """
        f=open('FakeStatus.txt',"r")
        code = f.read()
        f.close()

        if code == 'RUNNING':
            status = JobStatus.RUNNING
        elif code == 'DONE':
            status = JobStatus.DONE
        elif code == 'INITIALIZING':
            status = JobStatus.INITIALIZING
        else:
            status = JobStatus.ERROR
        return status

    def submit(self):
        """Submits a job for execution.
        """
        if not self.qobj or not self._job_id:
            raise Exception
            
        header = {"JobId": self._job_id, "SDK": "qiskit"}
        
        qubic_json = qobj_to_qubic(self.qobj)  
        f=open('FakePut.txt',"w")
        f.write('{}\n {}\n'.format(header, qubic_json))
        f.close()
