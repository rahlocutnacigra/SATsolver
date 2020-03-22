# test cases
from boolean import Boolean

print("\nTask 1 is successfully implemented.")

x = Boolean("literal", "x")
y = Boolean("literal", "y")
# For example, the formula (¬¬x∧y)∨¬x has value ⊤ if x=⊥ and y=⊤
print("\n\tTask 2:")
formula = Boolean("or", [Boolean("and", [Boolean("neg", Boolean("neg", x)), y]), Boolean("neg", x)])
print(f"{formula} is {formula.evaluated({'y': 'T'})} for y=T")
print(f"{formula} is {formula.evaluated({'x': 'F', 'y': 'T'})} for x=F and y=T")
print(f"{formula} could be simplified to {formula.simplified()}")
print(formula.cnf())
# For example (x∧⊤)∨⊥ is simplified to x
print("\n\tTask 3:")
formula2 = Boolean("or", [Boolean("and", [x, Boolean("T")]), Boolean("F")])
print(f"{formula2} could be simplified to {formula2.simplified()}")

# Some testing expressions:
# p∨(q∧p)
# (¬p∨q)∧p
# (p∨q)∧(p∨r)
# (p∧q)∧(q∧r)∧(r∧p)
# (p∨q)∧(q∨r)∧(r∨p)∧¬(p∧q)∧¬(q∧r)∧¬(r∧p)

print("\n\tTask 4:")
p = Boolean("literal", "p")
q = Boolean("literal", "q")
r = Boolean("literal", "r")

formula3 = Boolean("or", [p, Boolean("and", [q, p])])
formula4 = Boolean("and", [Boolean("or", [Boolean("neg", p), q]), p])
formula5 = Boolean("and", [Boolean("or", [p, q]), Boolean("or", [p, r])])
formula6 = Boolean("and", [Boolean("and", [p, q]), Boolean("and", [q, r]), Boolean("and", [r, p])])
formula7 = Boolean("and", [Boolean("or", [p, q]), Boolean("or", [q, r]), Boolean("or", [r, p]),
                           Boolean("neg", Boolean("and", [p, q])), Boolean("neg", Boolean("and", [q, r])),
                           Boolean("neg", (Boolean("and", [r, p])))])

print(formula3.cnf())
print(formula4.cnf())
print(formula5.cnf())
print(formula6.cnf())
print(formula7.cnf())
