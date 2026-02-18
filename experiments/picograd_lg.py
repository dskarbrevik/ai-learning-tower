
from ai_tower.picograd.node import Node

w = Node(0.5)
x = Node(0.4)
b = Node(0.1)

y_hat = w*x+b

y = Node(1)

L = (y_hat - y)*(y_hat - y)

L.backward()

print(w.grad)

print(f"Updated w: {w.value-(0.1*w.grad)}")