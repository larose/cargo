import pytest  # type: ignore

import cargo


def test_not_found_root():
    class A:
        pass

    container = cargo.containers.Standard()

    with pytest.raises(cargo.exceptions.DependencyNotFound) as exc_info:
        container[A]

    assert exc_info.value.args[0] == A


def test_not_found_recursive():
    class A:
        pass

    class B:
        def __init__(self, a: A):
            pass

    class C:
        def __init__(self, b: B):
            pass

    container = cargo.containers.Standard()

    container[B] = B
    container[C] = C

    with pytest.raises(cargo.exceptions.DependencyNotFound) as exc_info:
        container[C]

    assert exc_info.value.args[0] == A


def test_circular_dependency():
    class A:
        pass

    class B:
        pass

    def a_factory(b: B):
        pass

    def b_factory(a: A):
        pass

    container = cargo.containers.Standard()
    container[A] = a_factory
    container[B] = b_factory

    with pytest.raises(cargo.exceptions.CircularDependency) as exc:
        container[A]

    assert exc.value.cycle == [A, B, A]
