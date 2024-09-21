from sympy import symbols, solve

# Define the variables
a, b, c = symbols('a b c')

# Given points
points = {
    'A': (0, 1, 0),
    'B': (1, 5, 1),
    'C': (3, 2, 1)
}

# Equations from the points
equations = []
for point, coords in points.items():
    x, y, z = coords
    equation = a*x**2 + b*x + c - y
    equations.append(equation)

# Solve the system of equations
solution = solve(equations, (a, b, c))

# Display the solution
print("Solution:")
print(solution)