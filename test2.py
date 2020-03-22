import os
import sat_solver
from sat import *

# test cases
name1, V1, E1 = "poln_graf", [*range(10)], [(i, j) for j in range(10) for i in range(j)]
name2, V2, E2 = "star", [*range(10)], [(i, 9) for i in range(9)]
name3, V3, E3 = "cube", [*range(8)], [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 6),
                                      (6, 7), (7, 4)]
print(colouring(V1, E1, 10, name1))
print(colouring(V1, E1, 9, name1))
print(hamiltonian(V1, E1, False, name1))
print(hamiltonian(V1, E1, True, name1))

print(colouring(V2, E2, 3, name2))
print(colouring(V2, E2, 2, name2))
print(hamiltonian(V2, E2, False, name2))
print(hamiltonian(V2, E2, True, name2))

print(colouring(V3, E3, 2, name3))
print(colouring(V3, E3, 1, name3))
print(hamiltonian(V3, E3, False, name3))
print(hamiltonian(V3, E3, True, name3))

print(hadamard(4))
print(hadamard(5))
print(hadamard(6))

print(erdos_discrepancy(4, 10))
print(erdos_discrepancy(3, 15))
print(erdos_discrepancy(1, 10))
print(erdos_discrepancy(6, 10))

# compute solutions
for file in sorted(os.listdir("sat")):
    print()
    print("\t" + file)
    sat_solver.solve("sat/"+file, "results/"+"_solution.".join(file.split(".")))
