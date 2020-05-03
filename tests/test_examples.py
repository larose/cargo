import pytest  # type: ignore

import cargo


def test_circular_dependency():
    with pytest.raises(cargo.exceptions.CircularDependency) as exc:
        from examples import circular_dependency  # type: ignore # noqa: F401

    expected_cycle = (
        "<class 'examples.circular_dependency.B'>, "
        "<class 'examples.circular_dependency.C'>, "
        "<class 'examples.circular_dependency.D'>, "
        "<class 'examples.circular_dependency.B'>"
    )

    actual_cycle = str(", ".join(str(node) for node in exc.value.cycle))
    assert actual_cycle == expected_cycle


def test_dependency_not_found():
    with pytest.raises(cargo.exceptions.DependencyNotFound) as exc:
        from examples import dependency_not_found  # type: ignore # noqa: F401

    expected_exception = "DependencyNotFound(<class 'examples.dependency_not_found.B'>)"

    assert repr(exc.value) == expected_exception


def test_hello_dependencies():
    from examples import hello_dependencies  # type: ignore # noqa: F401

    assert isinstance(
        hello_dependencies.container[hello_dependencies.Hello], hello_dependencies.Hello
    )


def test_intro():
    from examples import intro  # type: ignore # noqa: F401

    assert isinstance(intro.container[intro.B], intro.B)


def test_my_container():
    from examples import my_container  # type: ignore # noqa: F401

    assert isinstance(my_container.container[my_container.B], my_container.B,)


def test_factory():
    from examples import factory_and_value  # type: ignore # noqa: F401

    assert isinstance(
        factory_and_value.container[factory_and_value.DatabaseClient],
        factory_and_value.MysqlClient,
    )
