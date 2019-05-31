A simple mpi approach to the "Dining philosophers problem" using the mpi python module "MPI4PY"

requirements:
python 3.7 or above
MS-MPI(Microsoft mpi)		(on windows)
mpi4py

Instalation on windows: 

-MS-MPI:
	https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi

-MPI4PY
-in the commnand line: > pip install mpi4py

-in the commnand line: > set MSMPI
 or add to path "C:\Program File\Microsoft MPI\Benchmarks\"  and"C:\Program File\Microsoft MPI\Bin\"

Running on windows:

-in the command line: > mpiexec -n [Number of process] py [FileName.py] [Number of taks]