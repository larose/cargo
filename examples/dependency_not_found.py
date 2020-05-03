from __future__ import annotations

import cargo


class A:
    def __init__(self, b: B):
        pass


class B:
    pass


container = cargo.containers.Standard()
container[A] = A
# Note: B has not been registered

# Raises cargo.exceptions.DependencyNotFound: <class '__main__.B'>
container[A]
