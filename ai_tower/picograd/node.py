

class Node:
    def __init__(self, value):

        self.value = value
        self._parents = []
        self.grad = 0.0
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        out = Node(self.value + other.value)
        out._parents = [self, other]
        
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad

        out._backward = _backward
        return out


    def __mul__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        out = Node(self.value * other.value)
        out._parents = [self, other]

        def _backward():
            self.grad += other.value * out.grad
            other.grad += self.value * out.grad

        out._backward = _backward

        return out

    def backward(self):

        topo = []

        visited = set()

        def build(node):

            if node not in visited:
                visited.add(node)
                for parent in node._parents:
                    build(parent)

                topo.append(node)
        build(self)

        self.grad = 1.0 # dy/dy

        for v in reversed(topo):
            v._backward()

        