import os
import sat_solver
from sat import *

# test cases
name1, V1, E1 = "poln_graf", [*range(10)], [(i, j) for j in range(10) for i in range(j)]
name2, V2, E2 = "star", [*range(10)], [(i, 9) for i in range(9)]
name3, V3, E3 = "cube", [*range(8)], [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 6),
                                      (6, 7), (7, 4)]                                     
name4, V4, E4 = "dvodelni_polni12", [*range(12)], [(i,j) for i in range(6) for j in range(6,12)]
name5, V5, E5 = "dvodelni_polni10", [*range(10)], [(i,j) for i in range(5) for j in range(5,10)]
name6, V6, E6 = "tridelni_polni", [*range(10)], [(i,j)for i in range(3) for j in range(3,10)]+[(i,j) for i in range(3,6) for j in range(4,10)]
name7, V7, E7 = "velik_dvodelni", [*range(100)], [(i,j) for i in range(50) for j in range(50,100)]
name8, V8, E8 = "veliki_tridelni2", [*range(70)], [(i,j)for i in range(30) for j in range(30,60)]+[(i,j) for i in range(30, 60) for j in range(60,70)]
name9, V9, E9 = "stiridelni",[*range(40)],[(i,j) for i in range (10) for j in range(10,40)]+[(i,j) for i in range (10,20) for j in range(20,40)]+[(i,j) for i  in range(20,30) for j in range(30,40)]
name10, V10, E10 =  "stiridelni_manjsi", [*range(100)], [(i,j) for i in range(25) for j in range(25,50)]+[(i,j) for i in range(25,50) for j in range(50,75)]+[(i,j) for i in range(50, 75) for j in range (75,100)]+[(i,j) for i in range(75,100) for j in range(25)]
name11, V11, E11 = "petdelni_velik", [*range(50)], [(i,j) for i in range(10) for j in range(10,20)]+[(i,j) for i in range(10,20) for j in range(20, 50)]+[(i,j) for i in range(20,30) for j in range(30,50)]+[(i,j) for i in range(30,40) for j in range(40,50)]
name12, V12, E12 = "stiridelni2",[*range(16)],[(i,j) for i in range (4) for j in range(4,16)]+[(i,j) for i in range (4,8) for j in range(8,16)]+[(i,j) for i  in range(8,12) for j in range(12,16)]

### Generate Dimacs-format file
##
###Colouring
##colouring(V3, E3, 2, name3)
##colouring(V4, E4, 2, name4)
##colouring(V2, E2, 2, name2)
##colouring(V10, E10, 2, name10)
##colouring(V7, E7, 2, name7)
##colouring(V2, E2, 3, name2)
##colouring(V10, E10, 3, name10)
##colouring(V8, E8, 3, name8)
##colouring(V9, E9, 4, name9)
##colouring(V11, E11, 5, name11)
##
###Erdos discrepancy
##erdos_discrepancy(1, 10)
##erdos_discrepancy(4, 14)
##erdos_discrepancy(4, 15)
##erdos_discrepancy(6, 10)
##erdos_discrepancy(8, 16)
##
###Hadamard matrix
##hadamard(4)
##
###Hamiltonian paths and cycles
##
##hamiltonian(V3, E3, True, name3)
##hamiltonian(V5, E5, True, name5)
##hamiltonian(V1, E1, True, name1)
##hamiltonian(V12, E12, True, name12)
##hamiltonian(V6, E6, True, name6)
##
##hamiltonian(V3, E3, False, name3)
##hamiltonian(V1, E1, False, name1)
##hamiltonian(V12, E12, False, name12)

# compute solutions
for file in sorted(os.listdir("sat")):
    print()
    print("\t" + file)
    sat_solver.solve("sat/"+file, "results/"+"_solution.".join(file.split(".")))
