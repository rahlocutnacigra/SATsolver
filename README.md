# SATsolver

## Running the program in the command-line
To run the program in the command line, use `python SAT_solver.py input.txt output.txt`, where the input file contains the SAT problem in the DIMACS format and the output file is the file in which the result should be saved.

## Generating new test cases
To make new test cases, to solve them and to represent results graphicaly use `test2.py`. 
* To add a new graph coloring test case use `colouring(V, E, k, name)` where
  * `V` is a list of vertices, 
  * `E` is a list of edges represented as tuples `(i,j)` where `i` and `j` are verices, 
  * `k` is a number of colours 
* To add a new Hamiltonian cycle or Hamiltonian path test case use `hamiltonian(V, E, cycle, name)` where
  * `V` is a list of vertices, 
  * `E` is a list of edges represented as tuples `(i,j)` where `i` and `j` are verices, 
  * `cycle=True` if we are searching for Hamiltonian cycle and `cycle=False` if we are searching for Hamiltonian path
 * To add a new Erdős discrepancy test case use `erdos_discrepancy(C, n)` where
  * `C` is discrepancy parameter
  * `n` is length of the sequence
 
