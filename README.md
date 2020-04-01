# SATsolver

## Running the program in the command-line
To run the program in the command line, use `python SAT_solver.py input.txt output.txt`, where the input file contains the SAT problem in the DIMACS format and the output file is the file in which the result should be saved.

## Generating new test cases
To make new test cases, to solve them and to represent results graphicaly use `test2.py`. 
* To add a new graph coloring test case, use function `colouring(V, E, k, name)` where
  * `V` is a list of vertices, 
  * `E` is a list of edges represented as tuples `(i,j)` where `i` and `j` are vertices, 
  * `k` is a number of colours 
* To add a new Hamiltonian cycle or Hamiltonian path test case, use function `hamiltonian(V, E, cycle, name)` where
  * `V` is a list of vertices, 
  * `E` is a list of edges represented as tuples `(i,j)` where `i` and `j` are vertices, 
  * `cycle=True` if we are searching for Hamiltonian cycle and `cycle=False` if we are searching for Hamiltonian path
* To add a new Erdős discrepancy test case, use function `erdos_discrepancy(C, n)` where
  * `C` is discrepancy parameter
  * `n` is length of the sequence
* To add a new Hadamard matrix test case, use function `hadamard(n)` where
  * `n` is matrix dimension
 
DIMACS format files of the generated problems will be saved in a folder `sat`. All the solutions will be in a folder `results`, visual representations of solutions for problems on graphs will be saved in a folder `fig`. 
 Those folders also contain our test cases and their solutions. 
 
When you run a file `test2.py` all of the files in folder `sat` are being solved. For solving a single problem, run it with `SAT_solver.py` or run `sat_solver.py` and use function `solve(input_file, output_file)` for visual representations of problems on graphs.

Our chosen CNF problem is `colouring_4_stiridelni_n40.txt` in the main folder.
