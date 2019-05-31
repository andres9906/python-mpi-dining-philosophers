from mpi4py import MPI 
import numpy as np 
import random
import time
import threading
import sys



comm = MPI.COMM_WORLD   
tam = comm.Get_size()  
rank = comm.Get_rank()


n = tam - 1
amig = tam - 2		#Se puede borrar
ambi = 2		#Se puede borrar
k = int(sys.argv[1])  #TAREAS
workTime = 5 #In seconds
waitReleaseTime = 2 #waiting time to drop the left fork

#ESTADOS
has0 = 1
hasIzq = 2
has2 = 3


# create a shared array of size 1000 elements of type double
size = tam * 2  
itemsize = MPI.DOUBLE.Get_size() 
if rank == 0: 
    nbytes = size * itemsize 
else: 
    nbytes = 0


def PRUEBA():  #Cambiar nombre a "printit" y cambiar el nombre de la funcion "printit" por otro
	t = threading.Timer(1, printit)
	t.start()
	print(forks, flush = True)
	print("\n \n")
	if forks[0] == n:
		t.cancel()

def printit():
	t = threading.Timer(1, printit)
	t.start()
	i = 1
	while i <= n:
		print("filosofo", i, flush = True)
		state = forks[i+tam]
		if state == has0:
			print("Libre ", flush = True)
		elif state == hasIzq:
			print("Tiene tenedor izquierdo", flush = True)
		elif state == has2:
			print("Tiene los dos tenedores, Comiendo", flush = True)
		i += 1
	print("\n \n")
	if forks[0] == n:
		t.cancel()

def getRFork(rank):  #get right fork
	i = (rank % n) + 1
	 
	#checks if the fork is available and if it is, sets it busy
	if forks[i] == 0 :		#TODO revisar segunda condicion
		forks[i] = 1
		#update state
		forks[rank+tam] = has2
		return 1
	else:
		#fork's not available
		return 0

def getLFork(rank):  #get left fork
	
	#checks if the fork is available and if it is, sets it busy
	if forks[rank] == 0 :
		forks[rank] = 1
		#update state
		forks[rank+tam] = hasIzq
		return 1
	else:
		#fork's not available
		return 0

def releaseLeft(rank):
	forks[rank] = 0
	forks[rank+tam] = has0
def releaseRight(rank):
	i = (rank % n) + 1
	forks[i] = 0
	forks[rank+tam] = hasIzq
def releaseAll(rank):
	releaseRight(rank)
	releaseLeft(rank)
	

win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm) 

buf, itemsize = win.Shared_query(0) 
assert itemsize == MPI.DOUBLE.Get_size() 
forks = np.ndarray(buffer=buf, dtype='d', shape=(size,)) 


if comm.rank == 0: 
	forks[0] = 0
	forks[n+1:] = 1
	ambi1 = random.randint(1, n)
	forks[ambi1] = ambi
	while True:
		ambi2 = random.randint(1, n)
		if ambi2 != ambi1:
			forks[ambi2] = ambi
			break
	printit()	#Start checker
	
# wait in process rank 0 until process 1 has written to the array
comm.Barrier() 


if rank != 0 : 
	amb = 0
	if forks[rank] == 2:
		forks[rank] = 0
		amb = 1  
		

	tasksCounter = 0
	while tasksCounter < k :
		#getting left fork
		lf = 0
		while(lf == 0):
			lf = getLFork(rank)

		#getting right fork
		releaseR = 0
		rf = 0	
		if amb == 0:
			waitReleaseTime = random.randint(5, 15)  #random waiting time 5-15 seconds
			timeout = time.time() + waitReleaseTime 
			while(rf == 0 and time.time() < timeout):
				rf = getRFork(rank)
			
			if rf != 0 :
				#Comer
				workTime = random.randint(2, 5) #Working time 2-5 seconds
				time.sleep(workTime)
				tasksCounter += 1
				#release forks
				releaseAll(rank)
				#Pensar
				ThinkTime = random.randint(7, 10) #Thinking time 7-10 seconds
				time.sleep(ThinkTime)	
			else:
				#Entrega izquierdo, filo amable no pudo obtener el derecho
				releaseLeft(rank)	
		else:
			while rf == 0:
				rf = getRFork(rank)

			#Comer
			workTime = random.randint(2, 5) #Working time 2-5 seconds
			time.sleep(workTime)
			tasksCounter += 1
			#release forks
			releaseAll(rank)
			#Pensar
			ThinkTime = random.randint(7, 10) #Thinking time 7-10 seconds
			time.sleep(ThinkTime)
	forks[0] += 1

comm.Barrier()
if rank == 0:	
	print("done")

    