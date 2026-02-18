"""Minimal autograd engine with Pydantic and non-recursive backprop."""

from typing import Callable
from pydantic import BaseModel, ConfigDict, PrivateAttr


class Node(BaseModel):
    value: float
    grad: float = 0.0
    
    _parents: list["Node"] = PrivateAttr(default_factory=list)
    _backward: Callable[[], None] = PrivateAttr(default_factory=lambda: lambda: None)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def __hash__(self): return id(self)
    def __eq__(self, other): return self is other
    
    def _wrap(self, v): return v if isinstance(v, Node) else Node(value=v)
    
    def __add__(self, other):
        other = self._wrap(other)
        out = Node(value=self.value + other.value)
        out._parents = [self, other]
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out
    
    def __mul__(self, other):
        other = self._wrap(other)
        out = Node(value=self.value * other.value)
        out._parents = [self, other]
        def _backward():
            self.grad += other.value * out.grad
            other.grad += self.value * out.grad
        out._backward = _backward
        return out
    
    def __pow__(self, n):
        out = Node(value=self.value ** n)
        out._parents = [self]
        def _backward():
            self.grad += n * (self.value ** (n - 1)) * out.grad
        out._backward = _backward
        return out
    
    def __neg__(self): return self * -1
    def __sub__(self, other): return self + (-other)
    def __truediv__(self, other): return self * (other ** -1)
    def __radd__(self, other): return self + other
    def __rsub__(self, other): return (-self) + other
    def __rmul__(self, other): return self * other
    def __rtruediv__(self, other): return other * (self ** -1)
    
    def backward(self):
        # Non-recursive topological sort
        topo, visited, stack = [], set(), [(self, False)]
        while stack:
            node, done = stack.pop()
            if done:
                topo.append(node)
            elif node not in visited:
                visited.add(node)
                stack.append((node, True))
                stack.extend((p, False) for p in node._parents if p not in visited)
        
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()
