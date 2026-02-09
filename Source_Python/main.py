from automate import *

a0 = automate("a")
a1 = automate("b")
a2 = union(a0, a1)
a3 = etoile(a2)
a4 = automate("c")
a5 = concatenation(a3, a4)
a6 = tout_faire(a5)

a7 = automate("a")
a8 = etoile(a7)
a9 = automate("c")
a10 = concatenation(a8, a9)
a11 = automate("b")
a12 = etoile(a11)
a13 = automate("c")
a14 = concatenation(a12, a13)
a15 = union(a10, a14)
a16 = tout_faire(a15)

if egal(a6, a16):
    print("EGAL")
else:
    print("NON EGAL")
