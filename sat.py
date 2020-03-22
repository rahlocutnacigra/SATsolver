# 16-20 March: Translating problems to SAT
from boolean import Boolean
from itertools import combinations


# G = (V, E); V = [v0, v1, ..., vn], E = [(v_i, v_j), ...]
# {v: [u for u in V if (u,v) in E or (v,u) in E] for v in V}


# graph colouring
# k ... number of colours
# v_ic ... vertex i of colour c
# each vertex has exactly one colour (v_i1 , v_i2 , v_i3 ... ) & (-v_i1 , -v_i2) ...
# each neighbour has different colour (-v_ic , -v_jc)
# convert graph to residual graph where edges become vertices that have edge if one endpoint is common
# formula to compute number of variables and clauses in terms of len(V), len(E), k
def colouring(V, E, k, name="1"):
    """
    Make SAT formula for colouring in graph problem.
    :param V: list of vertices
    :param E: list of edges, edge is pair of vertices
    :param k: number of colours
    :param name: graph name
    :return: CNF formula
    """
    output_file = f"sat/colouring_{k}_{name}_n{len(V)}.txt"  # name of output file in dimac format to represent CNF
    # n*k is number of variables, n+(k**2-k)*n/2+m*k clauses
    # n = len(V), m = len(E)
    # v_ic = i*k + c + 1 ... i-th vertex has color c, i in {0,...,n-1}, c in {0,...,k-1}
    assert type(k) is int and k > 0
    n = len(V)
    E = sorted(list({tuple(sorted([V.index(i), V.index(j)])) for i, j in E}))
    strE = "c edges;" + ";".join([f"{x + 1},{y + 1}" for x, y in E])
    m = len(E)
    # each vertex hac colour
    clauses = [[i * k + c + 1 for c in range(k)] for i in range(n)]
    # each vertex has at most one colour
    clauses += [[x, y] for x, y in set(tuple(sorted([-i * k - c1 - 1, -i * k - c2 - 1])) for c1, c2 in
                                       {(min(p, r), max(p, r)) for p in range(k) for r in range(k) if p != r} for i in
                                       range(n))]
    # each neighbours have different colour
    clauses += [[x, y] for x, y in set(
        tuple(sorted([-i * k - c - 1, -j * k - c - 1])) for i, j in {(p, r) for p, r in E if p != r} for c in range(k))]
    with open(output_file, "w") as f:
        f.write("c Graph colouring\nc\n")
        f.write(strE + "\n")
        f.write(f"c n = number of vertices = {n}\n")
        f.write(f"c m = number of edges = {m}\n")
        f.write(f"c k = number of colours = {k}\n")
        f.write(f"c vertex i=0,...,n-1 has colour c=0,...,k-1 if variable i*k+c+1 True\nc\n")
        f.write(f"c We have nk={n * k} variables and n+(k^2-k)n/2+mk={n + (k ** 2 - k) * n // 2 + m * k} clauses.\nc\n")
        f.write(f"p cnf {n * k} {len(clauses)}\n")
        f.write("\n".join([" ".join([str(lit) for lit in clause]) + " 0" for clause in clauses]) + "\n")
    return Boolean("and", [Boolean("or", [Boolean("literal", lit) if lit > 0 else
                                          Boolean("neg", Boolean("literal", abs(lit))) for
                                          lit in clause]) for clause in clauses])


# Hamiltonian path/cycle
# e_ij ... edge i,j is on cycle
# each vertex has exactly 2 edges on cycle (needs at least two neighbours)
# if we want path make new vertex connected to all others and remove it after
def hamiltonian(V, E, cycle=True, name="1"):
    """
    Construct SAT formula for searching hamiltonian path or cycle in a graph
    :param V: list of vertices
    :param E: list of edges, edge is pair of vertices
    :param cycle: if we want hamiltonian cycle or path
    :param name: graph name
    :return: CNF formula
    """
    # https://www.csie.ntu.edu.tw/~lyuu/complexity/2011/20111018.pdf
    # v_ij = j*n + i + 1 ... j-th vertex on position i in path
    E = sorted(list({tuple(sorted([V.index(i), V.index(j)])) for i, j in E}))
    strE = "c edges;" + ";".join([f"{x + 1},{y + 1}" for x, y in E])
    m = len(E)
    output_file = f"sat/hamiltonian_{'cycle' if cycle else 'path'}_{name}_m{m}_n{len(V)}.txt"  # dimac format for CNF
    n = len(V)
    V = [*range(n)]
    # each vertex appears at least once on hamiltonian path
    clauses = [[j * n + i + 1 for i in V] for j in V]
    # each vertex appears at most once in path
    clauses += [[-j * n - i - 1, -j * n - k - 1] for i in V for j in V for k in V if i != k]
    # all vertices are in path
    clauses += [[j * n + i + 1 for j in V] for i in V]
    # only one vertex is on each position
    clauses += [[-j * n - i - 1, -k * n - i - 1] for j in V for k in V for i in V if j != k]
    # vertices are not neighbours on path if not neighbours in graph
    clauses += [[-i * n - k - 1, -j * n - k - 2] for i in V for j in V for k in V[:-1] if
                not tuple(sorted([i, j])) in E]
    if cycle:
        # first and last are connected
        clauses += [[-i * n - 1, -j * n - n] for i in V for j in V if
                    not tuple(sorted([i, j])) in E]
    with open(output_file, "w") as f:
        f.write(f"c Hamiltonian {'cycle' if cycle else 'path'}\nc\n")
        f.write(strE + "\n")
        f.write(f"c n = number of vertices = {n}\n")
        f.write(f"c m = number of edges = {m}\n")
        f.write(f"c vertex i=0,...,n-1 on position j on {'cycle' if cycle else 'path'} if variable i*n+j+1 True\nc\n")
        f.write(f"p cnf {len(E)} {len(clauses)}\n")
        f.write("\n".join([" ".join([str(lit) for lit in clause]) + " 0" for clause in clauses]) + "\n")
    return Boolean("and", [Boolean("or", [Boolean("literal", lit) if lit > 0 else
                                          Boolean("neg", Boolean("literal", abs(lit))) for
                                          lit in clause]) for clause in clauses])


# Hadamard matrix
def hadamard(n):
    """
    Construct SAT formula for searching Hadamard matrix of dimension n
    :param n: dimension of matrix
    :return: CNF formula
    """
    output_file = f"sat/hadamard_{n}.txt"  # name of output file in dimac format for CNF
    if n % 2 != 0:
        print("Hadamard matrix is not possible for odd dimensions!")
        return 0
    # columns are pairwise orthogonal (exactly one subset of size = n/2 agrees else disagrees by elements)
    clauses = Boolean("and", [Boolean("or",
                                      [Boolean("and",
                                               [Boolean("literal", i * n + e).equivalent(Boolean("literal", j * n + e))
                                                if e in list(subset) else Boolean("neg", Boolean("literal",
                                                                                                 i * n + e)).equivalent(
                                                   Boolean("literal", j * n + e)) for e in range(1, n + 1)]) for subset
                                       in
                                       combinations(range(1, n + 1), n // 2)]) for j in range(1, n) for i in range(j)])
    clauses = clauses.evaluated({i: "T" for i in range(1, n + 1)}). \
        evaluated({i * n + 1: "T" for i in range(1, n + 1)}).simplified().cnf()
    variables = set(str(clauses).replace("(", "").replace(")", "").replace("]", "").
                    replace("[", "").replace("v", "").replace("&", "").replace("-", "").split(" "))
    variables = sorted([v for v in variables if "p" in v])
    aux = [[(-1 if "-" in str(c) else 1) * (n ** 2 + 1 + variables.index(str(c).replace("-", ""))) if
            "p" in str(c) else int(str(c)) for c in clause.pars] for
           clause in clauses.pars]
    with open(output_file, "w") as f:
        f.write(f"c Hadamard matrix of dimension {n}\nc\n")
        f.write(f"c n = rows and columns = {n}\n")
        f.write(f"c element i,j=0,...,n-1 is 1 if variable i*n+j+1-2*n True else -1\nc\n")
        f.write(f"p cnf {len(variables) + n ** 2 - 2 * n + 1} {len(aux)}\n")
        f.write("\n".join([" ".join([str(lit) for lit in clause]) + " 0" for clause in aux]) + "\n")
    return clauses


def erdos_discrepancy(C, n):
    """
    Construct SAT formula for searching a sequence of ones and minus ones that doesn't
    sum in C for any step d from d to k
    :param C: C-discrepancy parameter
    :param n: length of sequence
    :return: CNF formula
    """
    output_file = f"sat/discrepancy_{C}_{n}.txt"  # name of output file in dimac format for CNF
    if C < 0 or n < 0:
        print("Such sequence doesn't exist!")
        return 0
    # it is enough to check for sequences with more positive than negative elements
    clauses = Boolean("and", [Boolean("or", [Boolean("neg", Boolean("literal", c * d + 1)) if c in list(comb) else
                                             Boolean("literal", c * d + 1) for c in range(k // d)]) for k in
                              range(C, n + 1) for d
                              in range(1, n // k + 1) for comb in combinations(range(k // d), (C + k // d) // 2) if
                              (C + k // d) % 2 == 0])
    with open(output_file, "w") as f:
        f.write(f"c Erdos discrepancy\nc\n")
        f.write(f"c n = length of sequence = {n}\n")
        f.write(f"c C = discrepancy parameter = {C}\n")
        f.write(f"c element i=0,...,n-1 is 1 if variable i+1 True else -1\nc\n")
        f.write(f"p cnf {n} {len(clauses.pars)}\n")
        f.write("\n".join([" ".join([str(lit) for lit in clause.pars]) + " 0" for clause in clauses.pars]) + "\n")
    return clauses
