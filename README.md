# qiskit-qubic-provider
https://arxiv.org/abs/2101.00071

This is a prototype for a Qiskit provider for the open-source qubit controller Qiskit.


How to use it:
1) to generate FakePut.txt execute
./test2.py
By deflat it creates a bell-state. You can have more complex  circuit by changing hardcoded qc=circA() to qc=circB()

2) to read fake measurements results (from fakeget ) and display histogram with yileds per bit string execute
./test3.py  (broken & incomplete now)


----------------------------------------------------------------
OLD
I included 3 examples that would hopefully clarify how to use it.
To run the code you run one of the three Test.py or you can write a similar one and run it. 
This is the logic:
-in Test1 you can run the circuit by creating a job and then submitting it (using the submit function by the QUBICJob class) 
-in Test2 you can run the circuit directly with the run function of the backend.

Test1 and Test2 are equivalent, because both of them write the FakePut.txt, by using two different functions from different classes. 
-in Test3 you can retrieve the results from the (FakeGet.txt)  
----------------------------------------------------------------
