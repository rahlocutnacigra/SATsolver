import re, sys, copy, time, os.path
import itertools
from collections import Counter
import functools

def input_read(input_file):
    '''Parse CNF files in dimac format. Function returns a list of clauses and a dict
    of variables with None values'''
    clauses = []     # List for clauses
    vars = set()    # Set for variables
    with open(input_file) as f: 
        for line in f:
            if line.startswith("c"):   # comment
                continue
            elif line.startswith("p"):     # Data with the number of literals and clauses
                continue
            elif line.strip() == '':
                continue
            else:
                clause = list(map(lambda x: int(x), line.strip("\n| ").split(" ")))   # strips and splits
                clause.pop()    # As last element is a 0, therefore has to be removed
                vars = vars.union(set([abs(x) for x in clause]))    # To store used variables
                clauses.append(clause) 
    f.close()
    return clauses, dict.fromkeys(vars, None)

def propagate(formula, valuations, add = None):
    ''' Performs the unit propagation and simplification step. If add is not None, add the literal add to the first place. \n
        Check if there are any unit clauses. If there are, simplify: \n
            * Set the unit clause value to True \n
            * Remove all clauses that include this literal \n
            * Remove the literal from all clauses that include its negation \n
                * If we get an an empty clause: return formula, valuation \n
            * Back from the top, if we have any new unit clauses
            '''
    if add is not None:
        formula.insert(0, add)      # Adds a literal "add" at the beginning
    clause_num = 0  # Clause id number
    while clause_num < len(formula): # identify all the unit clauses
        if len(formula[clause_num]) == 1:       # If there exist a unit clause
            lit = formula[clause_num][0]    # The unit clause
            valuations[abs(lit)] = lit > 0 # the unit clause has to be True
            i = 0        # We move through all clauses
            while i < len(formula): # take care of clauses with val literal
                if lit in formula[i]:     # If the val literal appears in the clause, remove the clause
                    formula.remove(formula[i])    # As it is always true by definition
                    i -= 1    # As the length of the formula shortened
                elif -lit in formula[i]:    # If the negation of val literal appears
                    formula[i].remove(-lit)   # We remove the negation of val
                    if(len(formula[i]) == 0):     # If there are no other literals left in the clause
                        return formula, valuations  # Return the formula till now and its valuations
                i += 1
            clause_num = 0      # We have simplified the formula, back to step one
        else:
            clause_num += 1 # Clause on the clause_num-th place has at least two literals
    return formula, valuations

def findMostCommon(formula):
    '''Find the variable that has occured the most (negations count as the same var).'''
    occuranceNumber = Counter(i for i in map(abs, list(itertools.chain.from_iterable(formula))))
    return sorted(occuranceNumber, key=occuranceNumber.get, reverse=True)[0]

def DPLL_max(formula, valuations, add = None):
    '''Solves the SAT using the basic version of DPLL, a recursive algorithm. The formula input is the current 
    formula and valuations are the T/F valuations until this point. The add parameter represents a literal, that
    is when there are no unit clauses left.'''
    formula, valuations = propagate(formula, valuations, add)    # Simplifies the formula
    if formula == []: # If we managed to empty the list, the formula is satisfied
        return valuations
    elif [] in formula: # If there is an empty clause in the formula, the formula is not satisfied
        raise Exception("Contradiction!")
    literal_max = findMostCommon(formula)   # Finds the most common literal
    try:
        return DPLL_max(copy.deepcopy(formula), copy.deepcopy(valuations), [literal_max])
    except Exception:
        try:
            return DPLL_max(list(formula), dict(valuations), [-literal_max])
        except Exception:
            raise Exception("No match found!")

def test_sol(formula, valuation):
    '''Tests if the solution, given by valuation, satisfies the formula. \n
        Returns True or False'''
    for clause in formula:
        new_clause = []
        for literal in clause:
            val = valuation[abs(literal)]
            if (literal < 0 and val is not None):
                val = not val
            new_clause.append(False if val is None else val)
        if any(new_clause) == False:
            return False
    return True

def obtainSolution(formula, variables, solver, output_file):
    '''The function obtains the solution and writes it to the output_file. \n
        Inputs:\n
            * The formula\n
            * Dictionary of variables and their status\n
            * The solver function\n
            * Name of the output file\n
        The return of the function is a tuple of whether the solution was found
        and the solution.'''
    try:
        start_time = time.time()
        solution = solver(copy.deepcopy(formula), copy.deepcopy(variables))
        end_time = time.time()
        check = test_sol(formula, solution) # Safeguard if the solution is correct!
        if check:
            print("The solution was found and it holds! Time taken: {}".format(end_time-start_time))
    except:
        check = False
    solution = solution if check else None
    with open(output_file, "w") as file:
        if solution is None:
            print('The solution could not be found!')
            file.write("0");
        else:
            for lit, val in solution.items():
                file.write('{} '.format(lit if val else -lit))
    return (check, solution)

def main():
    '''Main function that translates the terminal input to python.'''
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    if not os.path.exists(inFile):
        print("The input file does not exist!")
        return
    formula, variables = input_read(inFile)
    check_DPLL, solution_DPLL = obtainSolution(formula, variables, DPLL_max, outFile)
    

if __name__ == '__main__':
    main()