import os
# import sys
import copy
import time
import networkx as nx
import matplotlib.pyplot as plt


def input_read(input_file):  # Parse CNF file in dimac format
    edges = []
    clauses = []
    with open(input_file) as f:
        for line in f:
            if "c edges" in line:
                edges = [tuple([int(i) for i in li.split(",")]) for li in line.split(";")[1:]]
            elif line[0] not in "cp":
                clauses.append([int(p) for p in line.split() if p not in "0"])
    return clauses, {abs(x): None for c in clauses for x in c}, edges


def findMostCommon(formula):  # Find the variable that has occured the most
    occurance = [abs(item) for sublist in formula for item in sublist]
    return max(occurance, key=occurance.count)


def propagate(formula, valuations, add=None):  # Performs the unit propagation and simplification step
    if add is not None:  # If add is not None, add the literal add to the first place
        formula.insert(0, add)  # Adds a literal "add" at the beginning
    clause_num = 0  # Clause id number
    while clause_num < len(formula):  # identify all the unit clauses
        if len(formula[clause_num]) == 1:  # If there exist a unit clause
            lit = formula[clause_num][0]  # The unit clause
            valuations[abs(lit)] = lit > 0  # the unit clause has to be True
            i = 0  # We move through all clauses
            while i < len(formula):  # take care of clauses with val literal
                if lit in formula[i]:  # If the val literal appears in the clause, remove the clause
                    formula.remove(formula[i])  # As it is always true by definition
                    i -= 1  # As the length of the formula shortened
                elif -lit in formula[i]:  # If the negation of val literal appears
                    formula[i].remove(-lit)  # We remove the negation of val
                    if len(formula[i]) == 0:  # If there are no other literals left in the clause
                        return formula, valuations  # Return the formula till now and its valuations
                i += 1
            clause_num = 0  # We have simplified the formula, back to step one
        else:
            clause_num += 1  # Clause on the clause_num-th place has at least two literals
    return formula, valuations


def DPLL_max(formula, valuations, add=None):
    """Solves the SAT using the basic version of DPLL, a recursive algorithm. The add parameter represents a literal,
    that is when there are no unit clauses left."""
    formula, valuations = propagate(formula, valuations, add)  # Simplifies the formula
    if not formula:  # If we managed to empty the list, the formula is satisfied
        return valuations
    elif [] in formula:  # If there is an empty clause in the formula, the formula is not satisfied
        return False
    literal_max = findMostCommon(formula)  # Finds the most common literal
    pos = DPLL_max(copy.deepcopy(formula), copy.deepcopy(valuations), [literal_max])
    if pos:
        return pos
    pos = DPLL_max(list(formula), dict(valuations), [-literal_max])
    if pos:
        return pos
    return False


def test_sol(formula, valuation):  # Tests if the solution, given by valuation, satisfies the formula
    for clause in formula:
        t_clause = False
        for literal in clause:
            val = valuation[abs(literal)]
            if val is not None:
                t_clause = t_clause or (not val if literal < 0 else val)
        if not t_clause:
            return False
    return True


def obtainSolution(formula, variables, solver, out_f):  # obtains the solution and writes it to the output_file
    start_time = time.time()
    solution = solver(copy.deepcopy(formula), copy.deepcopy(variables))
    end_time = time.time()
    if solution:
        check = test_sol(formula, solution)  # Safeguard if the solution is correct!
    else:
        check = False
    if check:
        print(f"The solution was found and it holds! Time taken: {end_time - start_time}")
    else:
        print(f'The solution could not be found! Time taken: {end_time - start_time}')
        solution = None
    open(out_f, "w").write(" ".join([f"{lit if val else -lit}" for lit, val in solution.items()]) if solution else "0")
    return check, solution  # whether the solution was found and the solution


def solve(input_file, output_file):
    formula_in, variables_in, edges = input_read(input_file)
    check_in, solution_in = obtainSolution(formula_in, variables_in, DPLL_max, output_file)
    if check_in:
        problem = input_file.split(".")[0].split("_")
        if "colouring" in problem[0]:
            k = int(problem[1])
            n = int(problem[-1][1:])
            name = " ".join(problem[2:-1])
            G = nx.Graph()
            G.add_nodes_from(range(1, n+1))
            G.add_edges_from(edges)
            pos = nx.spring_layout(G)  # positions for all nodes
            colours = [(x-1) % k+1 for x, v in sorted(solution_in.items()) if v and x <= k*n]
            nx.draw_networkx_nodes(G, pos, nodelist=range(1, n+1), node_color=colours, cmap=plt.get_cmap("jet"),
                                   node_size=500, alpha=0.8)
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
            plt.savefig("fig/" + "_".join(problem)[4:]+"solution.png")
            plt.axis('off')
            plt.show()
            print(f"Colouring of {name}: n={n}, k={k}\n\t" + ";   ".join([f"v{a}: {b}" for a, b in sorted([((x-1)//k+1,
                  (x-1) % k+1) for x, v in solution_in.items() if v and x <= k*n])]))
        elif "discrepancy" in problem[0]:
            C = int(problem[1])
            n = int(problem[2])
            result = ["1" if solution_in.get(a+1, True) else "-1" for a in range(n)]
            print(f"{C}-discrepancy of sequence with n={n}:\n\t" + ", ".join(result))
        elif "hamiltonian" in problem[0]:
            typ = problem[1]
            m = int(problem[-2][1:])
            n = int(problem[-1][1:])
            name = " ".join(problem[2:-2])
            G = nx.Graph()
            G.add_nodes_from(range(1, n + 1))
            G.add_edges_from(edges)
            pos = nx.spring_layout(G)  # positions for all nodes
            nx.draw_networkx_nodes(G, pos, nodelist=G.nodes, node_color='b', node_size=500, alpha=0.8)
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
            order = [b for a, b in sorted([((x-1) % n, (x-1) // n+1) for x, v in solution_in.items() if v])]
            edg = [(order[i], order[i+1]) for i in range(n-1)]
            if "cycle" in typ:
                edg += [(order[-1], order[0])]
            nx.draw_networkx_edges(G, pos, edgelist=edg, width=8, alpha=0.5, edge_color='b')
            plt.savefig("fig/" + "_".join(problem)[4:] + "solution.png")
            plt.axis('off')
            plt.show()
            print(f"Hamiltonian {typ} in graph {name}: n={n}, m={m}\n\t" + ", ".join([str(e) for e in edg]))
        elif "hadamard" in problem[0]:
            n = int(problem[-1])
            mat = [str(b) for a, b in sorted([(x, " 1" if v else "-1") for x, v in sorted(solution_in.items()) if
                                              x <= n**2])]
            mat = " 1 " * n + "\n\t" + "\n\t".join([" ".join([" 1"] + mat[(n-1)*i:(n-1)*(i+1)]) for i in range(n-1)])
            print(f"Hadamard matrix: n={n}\n\t" + mat)
        else:
            print(" ".join(problem) + "\nTrue: " + " ".join(sorted([str(x) for x, v in solution_in.items() if v])) +
                  "; False: otherwise")


# inFile = sys.argv[1]
# outFile = sys.argv[2]
# solve(inFile, outFile)
