from __future__ import annotations

import cargo

# Dependencies:
#   - A depends on B
#   - B depends on C
#   - C depends on D
#   - D depends on B
#
# Circular dependency cycle is: B -> C -> D -> B


class A:
    def __init__(self, b: B):
        pass


class B:
    def __init__(self, c: C):
        pass


class C:
    def __init__(self, d: D):
        pass


class D:
    def __init__(self, b: B):
        pass


container = cargo.containers.Standard()
container[A] = A
container[B] = B
container[C] = C
container[D] = D

# Raises cargo.exceptions.CircularDependency:
#   [<class '__main__.B'>, <class '__main__.C'>, <class '__main__.D'>, <class '__main__.B'>]
container[A]
