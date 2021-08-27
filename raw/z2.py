from z3 import *

x, y, z = Ints('x y z')
l1 = True == x < y 
l2 = Not(True == x < y)
l3 = True == x < z
l4 = True ==x < z 
ll = And(l1, And(l2, And(l3, l4)))
s = Solver()
s.add(ll)


print (s.check())
