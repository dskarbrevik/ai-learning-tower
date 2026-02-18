"""Simple picograd demo: autograd with non-recursive backprop."""

from ai_tower.picograd.node_v2 import Node

# Define inputs
x, y = Node(value=2.0), Node(value=3.0)

# Build computation graph: f(x,y) = x*y + x² - y
f = x * y + x ** 2 - y

print(f"f(x,y) = x*y + x² - y")
print(f"f({x.value}, {y.value}) = {f.value}")

# Backprop
f.backward()

print(f"\n∂f/∂x = {x.grad}  (expected: y + 2x = 7)")
print(f"∂f/∂y = {y.grad}  (expected: x - 1 = 1)")
