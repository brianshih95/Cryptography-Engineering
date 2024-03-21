import sympy as sp

x = sp.symbols('x')
polynomial = x**8 + x**4 + x**3 + x**2 + 1
dividend = x**255 - 1
remainder = sp.rem(dividend, polynomial, domain=sp.GF(2))
if remainder == 0:
    print("The polynomial is primitive.")
else:
    print("The polynomial is not primitive.")
