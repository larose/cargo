import typing

import pytest  # type: ignore

import cargo


class TestCase(typing.NamedTuple):
    key: typing.Type
    factory: typing.Any
    check: typing.Callable[[typing.Callable[[], typing.Any]], None]


# Prevents pytest warning "cannot collect test class 'TestCase' because it has a __new__ constructor"
TestCase.__test__ = False  # type: ignore


def class_factory() -> TestCase:
    class A:
        pass

    def check(get_actual_value):
        first = get_actual_value()
        assert isinstance(first, A)

        second = get_actual_value()
        assert first == second

    return TestCase(key=A, factory=A, check=check)


def dependency_spec_factory() -> TestCase:
    class A:
        pass

    class B(A):
        pass

    def check(get_actual_value):
        assert get_actual_value() == B

    dependency_spec = cargo.types.DependencySpec(
        dependency_types=[], instantiate=lambda: B
    )

    return TestCase(key=A, factory=dependency_spec, check=check)


def function_factory() -> TestCase:
    MyStr = typing.NewType("MyStr", str)

    def factory():
        return "my str"

    def check(get_actual_value):
        assert get_actual_value() == "my str"

    return TestCase(key=MyStr, factory=factory, check=check)


def method_factory() -> TestCase:
    class A:
        pass

    def factory():
        return A()

    def check(get_actual_value):
        first = get_actual_value()
        assert isinstance(first, A)

        second = get_actual_value()
        assert first == second

    return TestCase(key=A, factory=factory, check=check)


test_cases = (
    class_factory(),
    dependency_spec_factory(),
    function_factory(),
    method_factory(),
)


@pytest.mark.parametrize("test_case", test_cases)
def test_base_cases(test_case: TestCase):
    container = cargo.containers.Standard()
    container[test_case.key] = test_case.factory
    test_case.check(lambda: container[test_case.key])
