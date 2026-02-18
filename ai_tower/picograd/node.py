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

    def __sub__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        out = Node(self.value - other.value)
        out._parents = [self, other]
        
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += -1.0 * out.grad

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
        print([node.value for node in topo])
        self.grad = 1.0 # dy/dy

        for v in reversed(topo):
            print(f"before: {v.grad}")
            v._backward()
            print(f"after: {v.grad}")

    def _build_topo(self, node, visited, topo):
        if node not in visited:
            visited.add(node)
            for parent in node._parents:
                self._build_topo(parent, visited, topo)
            topo.append(node)