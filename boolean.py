# 9-13 March: Boolean formulas


# Build classes representing Boolean formulas (which may contain variables).
# Take 'T', 'F', 'and', 'or', 'neg' as basic logical connectives. Implication is translated to this connectives.
class Boolean:
    def __init__(self, typ, pars=None):
        self.typ = typ if typ in ["T", "F", "and", "or", "literal", "neg"] else None
        self.pars = pars

    def __repr__(self):
        if self.typ in ["T", "F"]:
            return self.typ
        elif self.typ in "literal":
            return str(self.pars)
        elif self.typ == "neg":
            return "-" + str(self.pars)
        elif self.typ == "and":
            return "[ " + " & ".join([str(literal) for literal in self.pars]) + " ]"
        elif self.typ == "or":
            return "( " + " v ".join([str(literal) for literal in self.pars]) + " )"

    # function or method that returns the value of a Boolean formula given the values of variables.
    def evaluate(self, values):
        if self.typ in "T":
            return Boolean("T")
        elif self.typ in "F":
            return Boolean("F")
        elif self.typ in "literal":
            value = values.get(self.pars, self.pars)
            if value in ["T", "F", "T/F"]:
                return Boolean("T" if "T" in value else "F")
            return Boolean("literal", self.pars)
        elif self.typ in "neg":
            value = self.pars.evaluate(values)
            return Boolean("T") if value.typ in "F" else Boolean("F") if value.typ in "T" else Boolean("neg", value)
        elif self.typ in ["and", "or"]:
            return Boolean(self.typ, [par.evaluate(values) for par in self.pars])

    def evaluated(self, values):
        return self.evaluate(values).simplified()

    def implies(self, other):
        return Boolean("or", [Boolean("neg", self), other])

    def equivalent(self, other):
        return Boolean("and", [self.implies(other), other.implies(self)])

    # a method for simplifying Boolean expressions
    def simplify(self):  # we cannot simplify T, F or literals
        # recursively simplify subexpressions, then simplify the resulting expression
        if self.typ in "neg":
            if self.pars.typ in "neg":  # cancel out double negations
                (self.typ, self.pars) = self.pars.pars.simplify()
            elif self.pars.typ in ["T", "F"]:  # push all negations towards the variables and constants
                self.typ = "F" if self.pars.typ in "T" else "T"
                self.pars = None
            elif self.pars.typ in ["and", "or"]:
                self.typ = "and" if self.pars.typ in "or" else "or"
                parameters = []
                for par in self.pars.pars:
                    new = Boolean("neg", par).simplify()
                    if new[0] in "T" and self.typ in "and":
                        pass
                    elif new[0] in "F" and self.typ in "or":
                        pass
                    elif new[0] in "T" and self.typ in "or":
                        self.typ = "T"
                        self.pars = None
                        return self.typ, self.pars
                    elif new[0] in "F" and self.typ in "and":
                        self.typ = "F"
                        self.pars = None
                        return self.typ, self.pars
                    else:
                        parameters.append(Boolean(new[0], new[1]))
                if len(parameters) == 0:
                    self.typ = "T" if self.typ in "and" else "F"
                    self.pars = None
                elif len(parameters) == 1:
                    self.typ = parameters[0].typ
                    self.pars = parameters[0].pars
                else:
                    self.pars = parameters
        elif self.typ in ["and", "or"]:
            parameters = []
            for par in self.pars:
                new = par.simplify()
                if new[0] in "T" and self.typ in "and":
                    pass
                elif new[0] in "F" and self.typ in "or":
                    pass
                elif new[0] in "T" and self.typ in "or":
                    self.typ = "T"
                    self.pars = None
                    return self.typ, self.pars
                elif new[0] in "F" and self.typ in "and":
                    self.typ = "F"
                    self.pars = None
                    return self.typ, self.pars
                else:
                    parameters.append(Boolean(new[0], new[1]))
            if len(parameters) == 0:
                self.typ = "T" if self.typ in "and" else "F"
                self.pars = None
            elif len(parameters) == 1:
                self.typ = parameters[0].typ
                self.pars = parameters[0].pars
            else:
                self.pars = parameters
        return self.typ, self.pars

    def simplified(self):
        s = self.simplify()
        return Boolean(s[0], s[1])

    def tseytin(self, name):  # convert logical formula to cnf form by tseytin transformation
        # name means (ordered number of parent among brothers)
        a = Boolean("literal", name)
        if self.typ in "neg":
            if self.pars.typ in ["literal", "T", "F"]:
                b = self.pars
            else:
                name = name + f"_0"
                b = Boolean("literal", name)
            return [Boolean("or", [Boolean("neg", a), Boolean("neg", b)]),
                    Boolean("or", [a, b])] + self.pars.tseytin(name)
        elif self.typ in "and":
            clauses = []
            sub_formulas = []
            for i in range(len(self.pars)):
                name_i = name + f"_{i}"
                clauses += self.pars[i].tseytin(name_i)
                if self.pars[i].typ in ["literal", "T", "F"]:
                    b = self.pars[i]
                else:
                    b = Boolean("literal", name_i)
                sub_formulas.append(b)
                clauses.append(Boolean("or", [Boolean("neg", a), Boolean("literal", b)]))
            clauses.append(Boolean("or", [a] + [Boolean("neg", b) for b in sub_formulas]))
            return clauses
        elif self.typ in "or":
            clauses = []
            sub_formulas = []
            for i in range(len(self.pars)):
                name_i = name + f"_{i}"
                clauses += self.pars[i].tseytin(name_i)
                if self.pars[i].typ in ["literal", "T", "F"]:
                    b = self.pars[i]
                else:
                    b = Boolean("literal", name_i)
                sub_formulas.append(b)
                clauses.append(Boolean("or", [Boolean("neg", b), a]))
            clauses.append(Boolean("or", [Boolean("neg", a)] + sub_formulas))
            return clauses
        return []

    # Write a method which performs the Tseytin transform (https://en.wikipedia.org/wiki/Tseytin_transformation)
    # https://profs.info.uaic.ro/~stefan.ciobaca/logic-2018-2019/notes7.pdf
    def cnf(self):
        for ch in "pxact":
            if ch not in str(self):
                name = ch
                break
            name = "node"
        return Boolean("and", [Boolean("literal", name)] + self.simplified().tseytin(name)).simplified()


def read_cnf(file):
    # Parse CNF files in dimac format
    clauses = []     # List for clauses
    names = set()    # Set for variables
    with open(file) as f:
        for line in f.readlines():
            if line[0] in "cp" or line.strip() == '':   # comment and data with the number of literals and clauses
                continue
            else:
                clause = [int(p) for p in line[:-2].split(" ") if abs(int(p)) > 0]
                names = names.union({abs(x) for x in clause})    # To store used variables
                clauses.append(Boolean("or", [Boolean("neg", Boolean("literal", -c)) if c < 0 else Boolean("literal", c)
                                              for c in clause]))
    return Boolean("and", clauses), list(names)
